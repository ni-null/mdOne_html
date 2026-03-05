# Configuration Guide

## Overview

MDOne uses two configuration methods:

1. **`.env` file** - Environment variables for local setup
2. **Command-line arguments** - Override `.env` settings at runtime

## Environment Variables (`.env`)

### Required Variables

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `MARKDOWN_SOURCE_DIR` | `./markdown` | Directory containing Markdown files | `./docs/markdown` |
| `OUTPUT_FILE` | `output.html` | Output HTML filename | `documentation.html` |

### Optional Variables

| Variable | Default | Description | Example |
|----------|---------|-------------|---------|
| `DEFAULT_TEMPLATE` | `normal` | Template name to use | `minimal`, `my_template` |
| `LOCALE` | `en` | Language code | `en`, `zh-TW` |
| `LOCALES_DIR` | `locales` | Directory containing language files | `./i18n` |
| `TEMPLATES_DIR` | `templates` | Directory containing templates | `./my_templates` |
| `SITE_TITLE` | `Documentation` | Page title | `My Project Docs` |
| `THEME_MODE` | `light` | Initial theme | `light` or `dark` |
| `BUILD_DATE` | Auto (today) | Build date for footer | `2024.03.05` |
| `MINIFY_HTML` | `true` | Minify output HTML | `true` or `false` |
| `MARKDOWN_EXTENSIONS` | `tables,fenced_code,codehilite,toc,attr_list,md_in_html` | Markdown extensions (comma-separated) | |

## Setup

### 1. Copy Template

```bash
cp .env.example .env
```

### 2. Edit `.env`

```ini
# Required
MARKDOWN_SOURCE_DIR=./markdown
OUTPUT_FILE=docs.html

# Optional
DEFAULT_TEMPLATE=normal
LOCALE=en
SITE_TITLE=My Documentation
MINIFY_HTML=true
```

### 3. Run

```bash
python main.py
```

## Command-line Arguments

Override `.env` settings with command-line arguments:

```bash
# Specify output file
python main.py --output my_docs.html

# Specify template
python main.py --template minimal

# Specify language
python main.py --locale zh-TW

# Specify markdown source directory
python main.py --source ./docs/guides

# Combine multiple arguments
python main.py --template minimal --locale en --output docs.html
```

## Template Configuration

Each template directory contains `template.config.json`:

```json
{
  "_metadata": {
    "name": "normal",
    "description": "Default template",
    "version": "1.0.0",
    "schema_version": "v1",
    "author": "MDOne Team"
  },
  "extra_css": [
    "https://cdn.jsdelivr.net/npm/highlight.js/styles/github.css"
  ],
  "extra_js": [
    "https://cdn.jsdelivr.net/npm/highlight.js/highlight.min.js"
  ]
}
```

### External Resources

- **`extra_css`** - External stylesheets (array of URLs)
- **`extra_js`** - External scripts (array of URLs)

These are injected into the HTML at `{EXTRA_CSS}` and `{EXTRA_JS}` placeholders.

## Dynamic Footer Date

Use `{BUILD_DATE}` placeholder in `locales/*.json`:

```json
{
  "template": {
    "footer_label": "Built on {BUILD_DATE}"
  }
}
```

Output: "Built on 2024.03.05"

To use a fixed date instead of today:

```ini
# In .env
BUILD_DATE=2024.03.05
```

## Best Practices

### Version Control

**Commit to git:**
```
✓ .env.example (template with defaults)
✓ templates/
✓ locales/
✓ main.py
✓ .gitignore
```

**Do NOT commit:**
```
✗ .env (local machine config)
✗ *.html (output files)
✗ venv/ (virtual environment)
✗ __pycache__/ (cache)
```

### Project Structure

```
project/
├── .env                      # Local config (git-ignored)
├── .env.example              # Template (committed)
├── main.py
├── markdown/
│   ├── intro.md
│   ├── guide.md
│   └── ...
├── templates/
│   └── normal/
├── locales/
│   ├── en.json
│   └── zh-TW.json
└── docs/                     # This documentation
    ├── CONFIGURATION.md
    ├── I18N.md
    └── ...
```

### Markdown Directory Structure

Any directory structure within `MARKDOWN_SOURCE_DIR` is flattened - all `.md` files become tabs.

```
markdown/
├── intro.md          → Tab: "intro"
├── getting-started.md → Tab: "getting-started"
└── advanced/
    └── api.md        → Tab: "api"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `.env` not read | Ensure file is named `.env`, not `.env.txt` |
| Template not found | Check `TEMPLATES_DIR` and template directory name |
| Language not changing | Verify `LOCALE` code exists in `locales/` |
| Settings not applied | Command-line args override `.env`; check priority |
| Date not updating | Set `BUILD_DATE=` empty to use today's date |

## Migration from v0.x

If you're upgrading from an older version:

1. Create `.env.example` with all settings
2. Create `.env` from the template
3. Update paths if directory structure changed
4. Re-run: `python main.py`
