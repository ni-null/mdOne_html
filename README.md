# MDOne HTML

A lightweight Markdown bundler that compiles multiple files into a single, self-contained HTML document.

一款輕量的 Markdown 打包工具，可將多個檔案編譯成一個獨立的 HTML 文件。

<img width="1365" height="831" alt="Preview" src="https://github.com/user-attachments/assets/1fb774d6-0554-43ef-89e2-433f241df411" />

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-repo/mdone-html.git
cd mdone-html

# 2. Install dependencies
pip install python-dotenv markdown

# 3. Run
python main.py --template minimal --output output.html --source ./docs
```

Done. Open `output.html` in your browser.

## Options

| Option | Description |
|--------|-------------|
| `--source` | Markdown source directory |
| `--output` | Output HTML filename |
| `--template` | Template name (`normal`, `minimal`) |
| `--locale` | Language (`en`, `zh-TW`) |

## `.env` (Optional)

```ini
MARKDOWN_SOURCE_DIR=./docs
OUTPUT_FILE=output.html
DEFAULT_TEMPLATE=minimal
LOCALE=en
```

## Documentation

- [Configuration](docs/CONFIGURATION.md)
- [Templates](docs/TEMPLATE_DEVELOPMENT.md)
- [i18n](docs/I18N.md)

## License

MIT
