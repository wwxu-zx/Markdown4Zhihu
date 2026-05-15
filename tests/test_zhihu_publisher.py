import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "zhihu-publisher.py"
PUBLISH_SCRIPT_PATH = REPO_ROOT / "scripts" / "publish.sh"


def run_command(command, cwd):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        command,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    result.stdout = result.stdout.decode("utf-8", "replace")
    return result


class ZhihuPublisherIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="markdown4zhihu-test-"))
        self.repo = self.temp_dir / "repo"
        self.repo.mkdir()
        (self.repo / "Data").mkdir()
        (self.repo / "scripts").mkdir()
        shutil.copy(str(SCRIPT_PATH), str(self.repo / "zhihu-publisher.py"))
        shutil.copy(str(PUBLISH_SCRIPT_PATH), str(self.repo / "scripts" / "publish.sh"))

        init_result = run_command(["git", "init"], self.repo)
        self.assertEqual(init_result.returncode, 0, init_result.stdout)

        remote_result = run_command(
            ["git", "remote", "add", "origin", "https://github.com/example/test.git"],
            self.repo,
        )
        self.assertEqual(remote_result.returncode, 0, remote_result.stdout)

    def tearDown(self):
        shutil.rmtree(str(self.temp_dir), ignore_errors=True)

    def create_noise_image(self, image_path, size, fmt, **save_kwargs):
        pixel_count = size[0] * size[1] * 3
        image = Image.frombytes("RGB", size, os.urandom(pixel_count))
        image.save(str(image_path), format=fmt, **save_kwargs)
        self.assertGreater(image_path.stat().st_size, int(5e5))

    def create_article_zip(self, article_name, markdown_text, images=None):
        resource_dir = self.repo / "Resource"
        resource_dir.mkdir(exist_ok=True)

        build_dir = self.temp_dir / ("build-" + article_name)
        shutil.rmtree(str(build_dir), ignore_errors=True)
        build_dir.mkdir()

        (build_dir / (article_name + ".md")).write_text(markdown_text, encoding="utf-8")

        for relative_path, color in (images or {}).items():
            image_path = build_dir / relative_path
            image_path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", (80, 80), color).save(str(image_path))

        zip_path = resource_dir / (article_name + ".zip")
        with zipfile.ZipFile(str(zip_path), "w") as archive:
            for file_path in sorted(build_dir.rglob("*")):
                if file_path.is_file():
                    archive.write(
                        str(file_path),
                        arcname=str(file_path.relative_to(build_dir)),
                    )

        return zip_path

    def test_compress_keeps_distinct_names_for_same_stem(self):
        article_dir = self.repo / "article"
        article_dir.mkdir()
        self.create_noise_image(article_dir / "same.png", (1200, 1200), "PNG")
        self.create_noise_image(article_dir / "same.jpg", (1200, 1200), "JPEG", quality=98)

        (self.repo / "article.md").write_text(
            "![one](article/same.png)\n![two](article/same.jpg)\n",
            encoding="utf-8",
        )

        result = run_command(
            [sys.executable, "zhihu-publisher.py", "--input", "article.md", "--compress"],
            self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

        output_dir = self.repo / "Data" / "article_for_zhihu"
        self.assertEqual(
            sorted(path.name for path in output_dir.iterdir() if path.is_file()),
            ["same.jpg", "same_1.jpg"],
        )

        output_text = (self.repo / "Data" / "article_for_zhihu.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("article_for_zhihu/same.jpg", output_text)
        self.assertIn("article_for_zhihu/same_1.jpg", output_text)

    def test_git_mode_commit_only_commits_generated_files(self):
        (self.repo / "README.md").write_text("base\n", encoding="utf-8")

        config_email = run_command(
            ["git", "config", "user.email", "test@example.com"],
            self.repo,
        )
        self.assertEqual(config_email.returncode, 0, config_email.stdout)

        config_name = run_command(
            ["git", "config", "user.name", "Tester"],
            self.repo,
        )
        self.assertEqual(config_name.returncode, 0, config_name.stdout)

        initial_add = run_command(["git", "add", "."], self.repo)
        self.assertEqual(initial_add.returncode, 0, initial_add.stdout)
        initial_commit = run_command(["git", "commit", "-m", "init"], self.repo)
        self.assertEqual(initial_commit.returncode, 0, initial_commit.stdout)

        article_dir = self.repo / "article"
        article_dir.mkdir()
        Image.new("RGB", (80, 80), "red").save(str(article_dir / "pic.png"))
        (self.repo / "article.md").write_text("![x](article/pic.png)\n", encoding="utf-8")

        (self.repo / "unrelated.txt").write_text("before\n", encoding="utf-8")
        unrelated_add = run_command(["git", "add", "unrelated.txt"], self.repo)
        self.assertEqual(unrelated_add.returncode, 0, unrelated_add.stdout)

        result = run_command(
            [sys.executable, "zhihu-publisher.py", "--input", "article.md", "--git-mode=commit"],
            self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

        show_result = run_command(["git", "show", "--stat", "--oneline", "HEAD"], self.repo)
        self.assertEqual(show_result.returncode, 0, show_result.stdout)
        self.assertIn("Data/article_for_zhihu.md", show_result.stdout)
        self.assertIn("Data/article_for_zhihu/pic.png", show_result.stdout)
        self.assertNotIn("unrelated.txt", show_result.stdout)

        cached_result = run_command(["git", "diff", "--cached", "--name-only"], self.repo)
        self.assertEqual(cached_result.returncode, 0, cached_result.stdout)
        self.assertEqual(cached_result.stdout.strip(), "unrelated.txt")

    def test_runs_without_chardet_module(self):
        (self.repo / "article.md").write_text("# hello\n", encoding="utf-8")
        (self.repo / "chardet.py").write_text(
            'raise ImportError("simulated missing chardet")\n',
            encoding="utf-8",
        )

        result = run_command(
            [sys.executable, "zhihu-publisher.py", "--input", "article.md"],
            self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue((self.repo / "Data" / "article_for_zhihu.md").exists())

    def test_nested_unicode_input_path_converts_successfully(self):
        article_dir = self.repo / "Data" / "中文目录" / "一个很长的文章目录名"
        article_dir.mkdir(parents=True)

        image_dir = article_dir / "配图"
        image_dir.mkdir()
        Image.new("RGB", (80, 80), "green").save(str(image_dir / "题图.png"))

        article_path = article_dir / "一篇很长的中文文章标题.md"
        article_path.write_text(
            "# 标题\n\n"
            "这里有一张图。\n\n"
            "![封面](<配图/题图.png>)\n",
            encoding="utf-8",
        )

        result = run_command(
            [sys.executable, "zhihu-publisher.py", "--input", str(article_path)],
            self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

        output_path = self.repo / "Data" / "一篇很长的中文文章标题_for_zhihu.md"
        self.assertTrue(output_path.exists())
        output_text = output_path.read_text(encoding="utf-8")
        self.assertIn("一篇很长的中文文章标题_for_zhihu/题图.png", output_text)

    def test_unescapes_square_brackets_outside_code_fences(self):
        (self.repo / "article.md").write_text(
            "Intervals: \\[0, 10], \\[11, 20]\n\n"
            "[Reference \\[J\\]](https://example.com/paper.pdf)\n\n"
            "```text\n"
            "literal \\[J\\]\n"
            "```\n",
            encoding="utf-8",
        )

        result = run_command(
            [sys.executable, "zhihu-publisher.py", "--input", "article.md"],
            self.repo,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

        output_text = (self.repo / "Data" / "article_for_zhihu.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Intervals: [0, 10], [11, 20]", output_text)
        self.assertIn("[Reference [J]](https://example.com/paper.pdf)", output_text)
        self.assertIn("literal \\[J\\]", output_text)
        self.assertNotIn("\\[0, 10]", output_text)

    def test_publish_script_rebuilds_extract_dir_before_running(self):
        if shutil.which("unzip") is None:
            self.skipTest("unzip command not available")

        self.create_article_zip(
            "Article",
            "![x](images/pic.png)\n",
            images={"images/pic.png": "red"},
        )

        first_result = run_command(
            ["sh", "scripts/publish.sh", "Article"],
            self.repo,
        )
        self.assertEqual(first_result.returncode, 0, first_result.stdout)
        self.assertTrue((self.repo / "Resource" / "Article" / "images" / "pic.png").exists())

        self.create_article_zip(
            "Article",
            "![x](images/pic.png)\n",
            images={},
        )

        second_result = run_command(
            ["sh", "scripts/publish.sh", "Article"],
            self.repo,
        )
        self.assertEqual(second_result.returncode, 0, second_result.stdout)

        extracted_image_path = self.repo / "Resource" / "Article" / "images" / "pic.png"
        self.assertFalse(extracted_image_path.exists())

        output_text = (self.repo / "Data" / "Article_for_zhihu.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("![x](images/pic.png)", output_text)
        self.assertNotIn("Article_for_zhihu/pic.png", output_text)

        output_image_path = self.repo / "Data" / "Article_for_zhihu" / "pic.png"
        self.assertFalse(output_image_path.exists())


if __name__ == "__main__":
    unittest.main()
