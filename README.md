# Markdown4Zhihu

这是一个可以将您的 Markdown 文件一键转换为知乎编辑器支持模式的仓库。

它会自动处理图片、行内公式、多行公式，以及对表格的部分支持。当图片过大时，您可以选择加上 `--compress` 选项，对超过大小阈值（这里约为 500K）的图片进行自动压缩。如果您的 md 文件和其图片文件夹在 Data 文件夹下，您本地的图片会自动转换为可直接在知乎中使用的图片链接。
上传知乎后一切都是那么美好。

## 依赖安装

先安装依赖：

`python -m pip install -r requirements.txt`

其中 `Pillow` 是图片处理必需依赖，`chardet` 用于更准确地自动检测输入文件编码。即使没有 `chardet`，脚本现在也可以运行，但仍然推荐安装。

如果您准备使用 `sh scripts/publish-zip.sh` 这个 zip 包入口，还需要系统里有 `unzip` 命令。macOS 和大多数 Linux 发行版通常默认自带；如果没有，脚本会直接提示缺少该命令。

## 使用方法

1. 首先，您应当仿照本仓库建立一个类似的您自己的仓库，它包括一个 `Data` 文件夹与根目录下的 `zhihu-publisher.py`。当然，您也可以选择直接 fork 本仓库到您自己的账号下。

2. 现在脚本会优先自动从当前仓库的 `git remote` 推断图片前缀，默认使用 `jsDelivr` CDN 加速；如果您希望切回 GitHub 原始链接，可以传：

   `--cdn-provider=github-raw`

   如果您希望手动指定完整前缀，也可以直接传：

   `--repo-prefix="https://raw.githubusercontent.com/<用户名>/<仓库名>/<分支名>/Data/"`

3. 如果您的原始材料已经打成 zip 包并放在 `Resource/` 目录下，推荐使用 zip 发布脚本：

   `sh scripts/publish-zip.sh AlexNet`

   这条命令会自动：
   - 找到 `Resource/AlexNet.zip`
   - 按 zip 内容重建 `Resource/AlexNet/`
   - 读取 `Resource/AlexNet/AlexNet.md`
   - 调用 `zhihu-publisher.py` 完成发布转换

   为了避免旧解压内容残留影响发布结果，`publish-zip.sh` 每次都会以 zip 包为准，重新生成同名解压目录。

   您也可以直接传 zip 路径：

   `sh scripts/publish-zip.sh Resource/AlexNet.zip`

   其他参数会继续透传给 `zhihu-publisher.py`，例如：

   `sh scripts/publish-zip.sh AlexNet --compress`

   `sh scripts/publish-zip.sh AlexNet --git-mode=push`

4. 如果您已经有一个现成的 Markdown 文件路径，可以使用专门的 Markdown 发布脚本：

   `sh scripts/publish-md.sh "C:\Users\xxx\Downloads\一个测试文档.md"`

   其他参数同样会透传给 `zhihu-publisher.py`，例如：

   `sh scripts/publish-md.sh "C:\Users\xxx\Downloads\一个测试文档.md" --compress`

   `sh scripts/publish-md.sh "C:\Users\xxx\Downloads\一个测试文档.md" --git-mode=push`

   如果您更希望直接调用主脚本，也仍然可以继续这样使用：

   `python zhihu-publisher.py --input="C:\Users\xxx\Downloads\一个测试文档.md"`

5. OK，all set。在 `./Data` 目录下，你可以看到一个 `一个测试文档_for_zhihu.md` 文件，以及一个 `一个测试文档_for_zhihu/` 图片目录，将生成后的 Markdown 上传至知乎编辑器即可。

## 测试样例

- 当前测试用例是自包含的，会在临时目录里构造中文路径、长文件名、图片压缩和 Git 提交场景，不依赖额外样例文件。
- 如果您只是想临时试跑，不希望把生成结果直接写回仓库里的 `Data/`，可以额外指定：

  `python zhihu-publisher.py --input="..." --data-dir="/tmp/markdown4zhihu-output"`

- 如果您忘了 zip 发布脚本的参数，也可以随时查看帮助：

  `sh scripts/publish-zip.sh --help`

- Markdown 路径发布脚本也支持帮助：

  `sh scripts/publish-md.sh --help`

- 当前回归测试可以直接运行：

  `python -m unittest tests.test_zhihu_publisher`

- 如果您想把常用检查收成一条命令，也可以直接运行：

  `sh scripts/check.sh`

## 新版补充

- 脚本现在支持 `![](<images/example with space.png>)` 这种带尖括号的 Markdown 图片写法。
- 当前默认会把拷贝后的图片放到 `<文章名>_for_zhihu/` 目录下；如果您想自定义目录名，也可以传 `--asset-dir-name=...`。
- 生成的链接会尽量保留中文目录名的可读性，只对空格等必要字符做编码。
- 类似 `截屏2026-04-07 15.10.15.png` 的文件名会自动规范成 `screenshot_20260407_151015.png`。
- 默认只生成文件，不会自动 `git add/commit/push`。
- 如果您希望顺手提交或推送，可以额外指定。默认 commit message 是 `update file <文章名>`，也可以用 `--commit-message="..."` 自定义：

  `python zhihu-publisher.py --input="..." --git-mode=commit`

  `python zhihu-publisher.py --input="..." --git-mode=push`

  `python zhihu-publisher.py --input="..." --git-mode=commit --commit-message="publish article"`
