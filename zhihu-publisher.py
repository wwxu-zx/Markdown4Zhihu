import argparse
import locale
import os
import os.path as op
import re
import subprocess
import sys

from pathlib import Path
from shutil import copyfile
from urllib.parse import quote, urlparse

from PIL import Image

try:
    import chardet
except ImportError:
    chardet = None


# Usage: This program transfers a markdown file into a format Zhihu can render.
# It mainly deals with local images, formulas, and a lightweight table workaround.

DEFAULT_GITHUB_REPO_PREFIX = (
    "https://raw.githubusercontent.com/wwxu-zx/Markdown4Zhihu/master/Data/"
)
DEFAULT_JSDELIVR_REPO_PREFIX = (
    "https://cdn.jsdmirror.com/gh/wwxu-zx/Markdown4Zhihu@master/Data/"
)
DEFAULT_CDN_PROVIDER = "jsdelivr"
COMPRESS_THRESHOLD = int(5e5)
DEFAULT_REMOTE_NAME = "origin"
SCRIPT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = SCRIPT_ROOT / "Data"

MARKDOWN_IMAGE_PATTERN = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\((?P<target>[^\n]*?)\)"
)
HTML_IMAGE_PATTERN = re.compile(
    r'(?P<prefix><img[^>]*?\ssrc\s*=\s*)(?P<quote>["\'])(?P<src>.*?)(?P=quote)',
    re.IGNORECASE,
)
CODE_FENCE_PATTERN = re.compile(r"```[\s\S]*?```")
ESCAPED_SQUARE_BRACKET_PATTERN = re.compile(r"\\([\[\]])")

RESAMPLE_FILTER = getattr(
    getattr(Image, "Resampling", Image),
    "LANCZOS",
    getattr(Image, "ANTIALIAS", Image.BICUBIC),
)


def normalize_repo_prefix(prefix):
    prefix = prefix.strip()
    if prefix and not prefix.endswith("/"):
        prefix += "/"
    return prefix


def encode_url_path_for_display(path_text):
    replacements = {
        "%": "%25",
        " ": "%20",
        "#": "%23",
        "?": "%3F",
        '"': "%22",
        "<": "%3C",
        ">": "%3E",
    }
    normalized_path = path_text.replace("\\", "/")
    return "".join(replacements.get(char, char) for char in normalized_path)


def safe_print(*parts):
    message = " ".join(str(part) for part in parts)
    try:
        print(message)
    except UnicodeEncodeError:
        buffer = getattr(sys.stdout, "buffer", None)
        if buffer is not None:
            buffer.write((message + "\n").encode("utf-8"))
            buffer.flush()
        else:
            sys.stdout.write((message + "\n").encode("utf-8", "replace").decode("utf-8"))


def run_git_command(command):
    return subprocess.run(
        command,
        cwd=str(SCRIPT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def git_stdout(command):
    result = run_git_command(command)
    if result.returncode == 0:
        return result.stdout.strip()
    return ""


def infer_git_branch(remote_name):
    upstream = git_stdout(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]
    )
    if upstream.startswith(remote_name + "/"):
        return upstream[len(remote_name) + 1 :]

    remote_head = git_stdout(
        ["git", "symbolic-ref", "refs/remotes/{}/HEAD".format(remote_name)]
    )
    if remote_head.startswith("refs/remotes/{}/".format(remote_name)):
        return remote_head.rsplit("/", 1)[-1]

    current_branch = git_stdout(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if current_branch and current_branch != "HEAD":
        return current_branch

    return "master"


def parse_github_remote(remote_url):
    remote_url = remote_url.strip()
    patterns = [
        r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$",
        r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$",
        r"^ssh://git@github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$",
    ]

    for pattern in patterns:
        match = re.match(pattern, remote_url)
        if match:
            return match.group("owner"), match.group("repo")

    return None


def infer_repo_prefix(remote_name, branch_name, cdn_provider):
    remote_url = git_stdout(["git", "remote", "get-url", remote_name])
    owner_repo = parse_github_remote(remote_url)
    if not owner_repo:
        if cdn_provider == "github-raw":
            return normalize_repo_prefix(DEFAULT_GITHUB_REPO_PREFIX)
        return normalize_repo_prefix(DEFAULT_JSDELIVR_REPO_PREFIX)

    owner, repo = owner_repo
    encoded_branch = quote(branch_name, safe="")
    if cdn_provider == "github-raw":
        return normalize_repo_prefix(
            "https://raw.githubusercontent.com/{}/{}/{}/Data".format(
                owner,
                repo,
                encoded_branch,
            )
        )

    return normalize_repo_prefix(
        "https://cdn.jsdmirror.com/gh/{}{}{}".format(
            owner,
            "/{}".format(repo),
            "@{}/Data".format(encoded_branch),
        )
    )


def detect_encoding(file_path):
    with open(str(file_path), "rb") as handle:
        sample = handle.read()
        if chardet is not None:
            detected = chardet.detect(sample)
            safe_print(detected)
            return detected.get("encoding") or "utf-8"

    fallbacks = []
    for encoding in ("utf-8", locale.getpreferredencoding(False), "gb18030"):
        if encoding and encoding not in fallbacks:
            fallbacks.append(encoding)

    for encoding in fallbacks:
        try:
            sample.decode(encoding)
            safe_print(
                {
                    "encoding": encoding,
                    "confidence": "fallback",
                    "language": "",
                }
            )
            return encoding
        except UnicodeDecodeError:
            continue

    safe_print(
        {
            "encoding": "utf-8",
            "confidence": "fallback-replace",
            "language": "",
        }
    )
    return "utf-8"


def apply_outside_code_fences(text, transform):
    pieces = []
    last_index = 0

    for match in CODE_FENCE_PATTERN.finditer(text):
        pieces.append(transform(text[last_index : match.start()]))
        pieces.append(match.group(0))
        last_index = match.end()

    pieces.append(transform(text[last_index:]))
    return "".join(pieces)


def unescape_square_brackets(lines):
    return ESCAPED_SQUARE_BRACKET_PATTERN.sub(r"\1", lines)


def formula_ops(lines):
    lines = re.sub(
        r"((.*?)\$\$)(\s*)?([\s\S]*?)(\$\$)\n",
        (
            '\n<img src="https://www.zhihu.com/equation?tex=\\4" alt="\\4" '
            'class="ee_img tr_noresize" eeimg="1">\n'
        ),
        lines,
    )
    lines = re.sub(
        r"(\$)(?!\$)(.*?)(\$)",
        (
            ' <img src="https://www.zhihu.com/equation?tex=\\2" alt="\\2" '
            'class="ee_img tr_noresize" eeimg="1"> '
        ),
        lines,
    )
    return lines


def strip_optional_angle_brackets(value):
    value = value.strip()
    if value.startswith("<") and value.endswith(">"):
        return value[1:-1].strip()
    return value


def split_markdown_destination(destination):
    destination = destination.strip()
    if not destination:
        return "", ""

    if destination.startswith("<"):
        closing_index = destination.find(">")
        if closing_index != -1:
            path = destination[1:closing_index].strip()
            title = destination[closing_index + 1 :].strip()
            return path, title

    match = re.match(
        r"""^(?P<path>.+?)(?:\s+(?P<title>"[^"]*"|'[^']*'|\([^)]*\)))?$""",
        destination,
    )
    if not match:
        return destination, ""

    return match.group("path").strip(), (match.group("title") or "").strip()


def is_remote_image_path(path_text):
    scheme = urlparse(path_text).scheme.lower()
    return scheme in {"http", "https", "data"}


def resolve_local_image_path(path_text):
    if not path_text or is_remote_image_path(path_text):
        return None

    expanded_path = Path(path_text).expanduser()
    candidates = []

    if expanded_path.is_absolute():
        candidates.append(expanded_path)
    else:
        candidates.append(Path(args.file_parent) / expanded_path)
        candidates.append(expanded_path)

    for candidate in candidates:
        try:
            if candidate.exists() and candidate.is_file():
                return candidate.resolve()
        except OSError:
            continue

    return None


def strip_known_prefix(file_name, prefix):
    if file_name.startswith(prefix):
        stripped_name = file_name[len(prefix) :].lstrip(" _-")
        if stripped_name:
            return stripped_name
    return file_name


def strip_known_prefixes(file_name, prefixes):
    stripped_name = file_name

    while True:
        updated_name = stripped_name
        for prefix in prefixes:
            updated_name = strip_known_prefix(updated_name, prefix)

        if updated_name == stripped_name:
            return stripped_name

        stripped_name = updated_name


def normalize_screenshot_name(file_name):
    path_obj = Path(file_name)
    stem = path_obj.stem.strip()
    suffix = path_obj.suffix or ""

    patterns = [
        re.compile(
            (
                r"^(?:截图|截屏|屏幕截图|屏幕快照|screenshot|screen[\s_-]?shot)"
                r"[\s_-]*(?P<year>\d{4})[-_.](?P<month>\d{1,2})[-_.](?P<day>\d{1,2})"
                r"(?:[\s_-]+(?:at[\s_-]+)?)?"
                r"(?:(?P<ampm>上午|下午|AM|PM|am|pm)[\s_-]*)?"
                r"(?P<hour>\d{1,2})[.:](?P<minute>\d{1,2})[.:](?P<second>\d{1,2})"
                r"(?:[\s_-]+(?P<copy_index>\d+))?$"
            ),
            re.IGNORECASE,
        ),
        re.compile(
            (
                r"^(?:截图|截屏|屏幕截图|屏幕快照|screenshot|screen[\s_-]?shot)"
                r"[\s_-]*(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})"
                r"[\s_-]+(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})"
                r"(?:[\s_-]+(?P<copy_index>\d+))?$"
            ),
            re.IGNORECASE,
        ),
    ]

    match = None
    for pattern in patterns:
        match = pattern.match(stem)
        if match:
            break

    if match is None:
        return file_name

    hour = int(match.group("hour"))
    ampm = (match.groupdict().get("ampm") or "").lower()
    if ampm in {"pm", "下午"} and hour < 12:
        hour += 12
    if ampm in {"am", "上午"} and hour == 12:
        hour = 0

    normalized_stem = "screenshot-{year}{month:02d}{day:02d}-{hour:02d}{minute:02d}{second:02d}".format(
        year=match.group("year"),
        month=int(match.group("month")),
        day=int(match.group("day")),
        hour=hour,
        minute=int(match.group("minute")),
        second=int(match.group("second")),
    )
    if match.group("copy_index"):
        normalized_stem += "-{}".format(int(match.group("copy_index")))
    return normalized_stem + suffix.lower()


def simplify_image_name(source_path):
    base_name = strip_known_prefixes(
        source_path.name,
        (
        args.input.stem,
        args.input.stem + "_for_zhihu",
        args.asset_dir_name,
        ),
    )

    return normalize_screenshot_name(base_name)


def should_compress_image(source_path):
    if not args.compress:
        return False

    try:
        return source_path.stat().st_size > COMPRESS_THRESHOLD
    except OSError:
        return False


def reserve_target_image_name(source_path):
    source_key = str(source_path)
    base_name = simplify_image_name(source_path)
    candidate_stem = Path(base_name).stem
    candidate_suffix = Path(base_name).suffix or source_path.suffix
    if should_compress_image(source_path):
        candidate_suffix = ".jpg"

    base_name = candidate_stem + candidate_suffix

    existing_source = args.reserved_image_names.get(base_name)
    if existing_source in (None, source_key):
        args.reserved_image_names[base_name] = source_key
        return base_name

    index = 1
    while True:
        candidate_name = "{}_{}{}".format(candidate_stem, index, candidate_suffix)
        existing_source = args.reserved_image_names.get(candidate_name)
        if existing_source in (None, source_key):
            args.reserved_image_names[candidate_name] = source_key
            return candidate_name
        index += 1


def reduce_single_image_size(image_path):
    image_path = Path(image_path)
    output_path = image_path.parent / (image_path.stem + ".jpg")

    if not image_path.exists():
        return image_path

    with Image.open(str(image_path)) as image:
        width, height = image.size
        if width > height and width > 1920:
            image = image.resize(
                (1920, int(1920 * height / width)),
                RESAMPLE_FILTER,
            )
        elif height >= width and height > 1080:
            image = image.resize(
                (int(1080 * width / height), 1080),
                RESAMPLE_FILTER,
            )
        image.convert("RGB").save(
            str(output_path),
            optimize=True,
            quality=85,
        )

    return output_path


def publish_local_image(local_image_path):
    source_key = str(local_image_path)
    if source_key in args.copied_images:
        published_path = args.copied_images[source_key]
    else:
        image_name = reserve_target_image_name(local_image_path)
        published_path = Path(args.image_folder_path) / image_name

        same_location = False
        try:
            same_location = published_path.exists() and local_image_path.samefile(published_path)
        except (FileNotFoundError, OSError):
            same_location = False

        if not same_location:
            copyfile(str(local_image_path), str(published_path))

        args.copied_images[source_key] = published_path

    if should_compress_image(local_image_path):
        published_path = reduce_single_image_size(published_path)
        args.copied_images[source_key] = published_path

    args.used_images.add(published_path.name)
    return published_path


def build_remote_image_url(image_name):
    relative_path = "{}/{}".format(args.asset_dir_name, image_name)
    return args.repo_prefix + encode_url_path_for_display(relative_path)


def rewrite_image_path(path_text):
    normalized_path = strip_optional_angle_brackets(path_text)
    local_image_path = resolve_local_image_path(normalized_path)
    if local_image_path is None:
        return None

    published_path = publish_local_image(local_image_path)
    remote_url = build_remote_image_url(published_path.name)
    safe_print("publish image:", local_image_path)
    safe_print("remote image :", remote_url)
    return published_path, remote_url


def replace_markdown_image(match):
    original_text = match.group(0)
    alt_text = match.group("alt")
    destination = match.group("target")
    path_text, title = split_markdown_destination(destination)
    rewritten = rewrite_image_path(path_text)

    if rewritten is None:
        return original_text

    published_path, rewritten_path = rewritten
    if not alt_text:
        alt_text = Path(published_path).stem

    title_suffix = " " + title if title else ""
    return "![{}]({}{})".format(alt_text, rewritten_path, title_suffix)


def replace_html_image(match):
    rewritten = rewrite_image_path(match.group("src"))
    if rewritten is None:
        return match.group(0)

    _, rewritten_path = rewritten
    quote_char = match.group("quote")
    return "{prefix}{quote}{path}{quote}".format(
        prefix=match.group("prefix"),
        quote=quote_char,
        path=rewritten_path,
    )


def image_ops(lines):
    lines = MARKDOWN_IMAGE_PATTERN.sub(replace_markdown_image, lines)
    lines = HTML_IMAGE_PATTERN.sub(replace_html_image, lines)
    return lines


def table_ops(lines):
    return re.sub(r"\|\n", r"|\n\n", lines)


def cleanup_image_folder():
    image_folder = Path(args.image_folder_path)
    if not image_folder.exists():
        return

    for image_path in image_folder.iterdir():
        if image_path.is_file() and image_path.name not in args.used_images:
            safe_print(
                "File {} is not used in the markdown file, so it will be deleted.".format(
                    image_path
                )
            )
            image_path.unlink()


def run_generation():
    if args.encoding is None:
        args.encoding = detect_encoding(args.input)

    with open(str(args.input), "r", encoding=args.encoding) as reader:
        lines = reader.read()

    lines = apply_outside_code_fences(lines, image_ops)
    lines = apply_outside_code_fences(lines, unescape_square_brackets)
    lines = apply_outside_code_fences(lines, formula_ops)
    lines = apply_outside_code_fences(lines, table_ops)

    with open(str(args.output_path), "w+", encoding=args.encoding) as writer:
        writer.write(lines)

    cleanup_image_folder()


def stage_generated_files():
    paths_to_stage = [
        op.relpath(str(args.output_path), str(SCRIPT_ROOT)),
        op.relpath(str(args.image_folder_path), str(SCRIPT_ROOT)),
    ]
    result = run_git_command(["git", "add", "--all"] + paths_to_stage)
    if result.returncode != 0:
        safe_print(result.stderr.strip() or result.stdout.strip())
        return []
    return paths_to_stage


def has_staged_changes(paths_to_stage):
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet", "--"] + paths_to_stage,
        cwd=str(SCRIPT_ROOT),
    )
    return result.returncode == 1


def perform_git_ops():
    if args.git_mode == "none":
        return

    paths_to_stage = stage_generated_files()
    if not paths_to_stage:
        return

    if not has_staged_changes(paths_to_stage):
        safe_print("No generated file changes to commit.")
        return

    commit_result = run_git_command(
        ["git", "commit", "-m", args.commit_message, "--only", "--"] + paths_to_stage
    )
    if commit_result.returncode != 0:
        safe_print(commit_result.stderr.strip() or commit_result.stdout.strip())
        return
    safe_print(commit_result.stdout.strip())

    if args.git_mode != "push":
        return

    push_result = run_git_command(
        ["git", "push", "-u", args.remote_name, args.current_branch]
    )
    if push_result.returncode != 0:
        safe_print("git push failed.")
        safe_print(push_result.stderr.strip() or push_result.stdout.strip())
        if "Permission to" in push_result.stderr and "denied" in push_result.stderr:
            safe_print(
                "The current GitHub credential does not have push permission for the remote repository."
            )
        return

    safe_print(push_result.stdout.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        'Please input the file path you want to transfer using --input=""'
    )
    parser.add_argument(
        "--compress",
        action="store_true",
        help="Compress images that are larger than the size threshold.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Path to the markdown file you want to transfer.",
    )
    parser.add_argument(
        "-e",
        "--encoding",
        type=str,
        help="Encoding of the input file.",
    )
    parser.add_argument(
        "--repo-prefix",
        type=str,
        help="Full asset URL prefix override. When set, it takes precedence over --cdn-provider.",
    )
    parser.add_argument(
        "--cdn-provider",
        choices=["jsdelivr", "github-raw"],
        default=DEFAULT_CDN_PROVIDER,
        help="Default asset host when --repo-prefix is not provided.",
    )
    parser.add_argument(
        "--branch",
        type=str,
        help="Git branch name used when auto-generating asset URLs.",
    )
    parser.add_argument(
        "--asset-dir-name",
        type=str,
        help="Directory name used for copied images under --data-dir. Defaults to <input_stem>_for_zhihu.",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=str(DEFAULT_DATA_DIR),
        help="Directory used to store generated markdown files and copied images.",
    )
    parser.add_argument(
        "--git-mode",
        choices=["none", "commit", "push"],
        default="none",
        help="Whether to commit or push generated files after conversion.",
    )
    parser.add_argument(
        "--remote-name",
        type=str,
        default=DEFAULT_REMOTE_NAME,
        help="Git remote name used for URL inference and push.",
    )
    parser.add_argument(
        "--commit-message",
        type=str,
        help="Commit message used when --git-mode is commit or push.",
    )

    args = parser.parse_args()
    args.used_images = set()
    args.copied_images = {}
    args.reserved_image_names = {}

    if args.input is None:
        raise FileNotFoundError("Please input the file's path to start!")

    args.input = Path(args.input).expanduser()
    args.file_parent = str(args.input.parent)
    args.current_branch = git_stdout(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or "master"
    if args.current_branch == "HEAD":
        args.current_branch = infer_git_branch(args.remote_name)

    args.branch = args.branch or infer_git_branch(args.remote_name)
    args.asset_dir_name = args.asset_dir_name or (args.input.stem + "_for_zhihu")
    args.repo_prefix = normalize_repo_prefix(
        args.repo_prefix or infer_repo_prefix(args.remote_name, args.branch, args.cdn_provider)
    )
    args.current_script_data_path = str(Path(args.data_dir).expanduser())
    args.image_folder_path = op.join(args.current_script_data_path, args.asset_dir_name)
    args.output_path = Path(args.current_script_data_path) / (args.input.stem + "_for_zhihu.md")
    args.commit_message = args.commit_message or "update file {}".format(args.input.stem)

    os.makedirs(args.image_folder_path, exist_ok=True)

    safe_print(args.image_folder_path)
    safe_print("Using asset prefix:", args.repo_prefix)

    run_generation()
    perform_git_ops()
