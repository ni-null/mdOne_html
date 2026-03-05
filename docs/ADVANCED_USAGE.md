# Advanced Usage

## Command-Line Options

### Full Usage

```bash
python main.py [OPTIONS]
```

### All Arguments

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--source` | `-s` | Markdown source directory | `-s ./docs/guides` |
| `--output` | `-o` | Output HTML file | `-o docs.html` |
| `--template` | `-t` | Template name | `-t minimal` |
| `--locale` | `-l` | Language code | `-l zh-TW` |
| `--help` | `-h` | Show help | |

### Examples

```bash
# Simple: use .env defaults
python main.py

# Specify everything
python main.py -s ./markdown -o output.html -t normal -l en

# Override just template
python main.py --template minimal

# Multiple options
python main.py --template my_template --locale zh-TW --output docs.html

# Short form
python main.py -t minimal -l en -o docs.html
```

## Markdown Organization

### Directory Structure Behavior

Files are discovered recursively from `MARKDOWN_SOURCE_DIR`, but directory structure is flattened to tabs.

Example:

```
markdown/
├── index.md              → Tab: "index"
├── getting-started.md    → Tab: "getting-started"
├── api/
│   ├── overview.md       → Tab: "overview"
│   ├── rest.md           → Tab: "rest"
│   └── websocket.md      → Tab: "websocket"
└── examples/
    └── basic.md          → Tab: "basic"
```

All files become separate tabs - subdirectory structure doesn't matter.

### Markdown Extensions

Enabled extensions (from `.env` `MARKDOWN_EXTENSIONS`):

```
tables
fenced_code
codehilite
toc
attr_list
md_in_html
```

### Markdown Features

**Tables:**
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

**Code Blocks:**
````markdown
```python
def hello():
    print("Hello")
```
````

**Table of Contents:**
```markdown
[TOC]
```

**Attributes:**
```markdown
## Section {#custom-id}

Paragraph
{: style="color: red;" }
```

## Batch Processing

Generate multiple outputs with different configurations:

```bash
# English version
python main.py --locale en --output docs-en.html

# Chinese version  
python main.py --locale zh-TW --output docs-zh.html

# Alternative template
python main.py --template minimal --output docs-minimal.html
```

### Automation with Shell Script

Create `build.sh`:

```bash
#!/bin/bash

python main.py --locale en --output docs-en.html
python main.py --locale zh-TW --output docs-zh.html
python main.py --template minimal --output docs-minimal.html

echo "Build complete!"
```

Run: `bash build.sh`

## Customization Scenarios

### Scenario 1: Multi-Language Documentation

```bash
# Create English version
python main.py --locale en --output docs-en.html

# Create Traditional Chinese version
python main.py --locale zh-TW --output docs-zh.html

# Create Simplified Chinese version
python main.py --locale zh-CN --output docs-zh-cn.html
```

Then host all versions on your website.

### Scenario 2: Different Templates for Different Audiences

```bash
# Technical docs - detailed template
python main.py --template normal --output technical.html

# User guide - minimal template
python main.py --template minimal --output guide.html

# Admin docs - custom template
python main.py --template admin --output admin.html
```

### Scenario 3: Branding

Create custom template with company branding:

```bash
# 1. Create templates/company-brand/
# 2. Add logo, colors in style.css
# 3. Update template.config.json with company fonts

python main.py --template company-brand --output branded-docs.html
```

## Environmental Variables

Set variables before running:

```bash
# Windows PowerShell
$env:LOCALE = "en"
$env:DEFAULT_TEMPLATE = "minimal"
python main.py

# Linux/macOS
export LOCALE=en
export DEFAULT_TEMPLATE=minimal
python main.py
```

## Dynamic Content

### Build Date in Footer

In `.env`:
```ini
# Auto-calculate today's date
BUILD_DATE=

# Or specify fixed date
BUILD_DATE=2024.03.05
```

In `locales/en.json`:
```json
{
  "template": {
    "footer_label": "Documentation - Last updated {BUILD_DATE}"
  }
}
```

### Version in Title

In `.env`:
```ini
SITE_TITLE=MyApp Documentation v1.2.3
```

## Integration with CI/CD

### GitHub Actions Example

Create `.github/workflows/docs.yml`:

```yaml
name: Build Docs

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install python-dotenv markdown
      
      - name: Build documentation
        run: |
          python main.py --locale en --output docs-en.html
          python main.py --locale zh-TW --output docs-zh.html
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: documentation
          path: docs-*.html
```

## Performance Tips

### 1. HTML Minification

In `.env`:
```ini
MINIFY_HTML=true
```

Reduces file size by ~20-30%.

### 2. External Resources

Use CDN efficiently:
- Avoid loading unused styles
- Pin specific versions
- Use compressed formats

Good:
```json
{
  "extra_css": [
    "https://cdn.jsdelivr.net/npm/highlight.js@11.8.0/styles/atom-one-dark.min.css"
  ]
}
```

Bad:
```json
{
  "extra_css": [
    "https://cdnjs.cloudflare.com/ajax/libs/some-huge-framework/full.css",
    "https://unpkg.com/another-framework/bundle.min.css"
  ]
}
```

### 3. CSS Variables

Use CSS variables instead of duplicating colors:

```css
/* ✗ Bad: 3KB */
.tab { color: #2563eb; }
.button { color: #2563eb; }
.link { color: #2563eb; }

/* ✓ Good: 1KB */
:root { --primary: #2563eb; }
.tab { color: var(--primary); }
.button { color: var(--primary); }
.link { color: var(--primary); }
```

## Deployment

### Static Hosting

Most static hosts support:

- GitHub Pages
- Netlify
- Vercel
- AWS S3
- Azure Static Web Apps

Just upload the HTML file!

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t mdone .
docker run -v $(pwd)/markdown:/app/markdown mdone
```

## Version History

Track changes to your documentation:

```bash
# Good: Commit generated files sparately
git add markdown/ templates/ locales/
git commit -m "Update docs content"

git add *.html
git commit -m "Rebuild documentation"

# Or: Keep .html files in .gitignore
echo "*.html" >> .gitignore
git add markdown/ templates/ locales/
```

## Troubleshooting Advanced Scenarios

### Multiple Languages, Multiple Templates

```bash
# 1 language × 2 templates = 2 files
for template in normal minimal; do
  python main.py --template $template --locale en --output docs-${template}.html
done
```

### Large Documentation Sets

If you have 100+ markdown files:

1. Organize in subdirectories (structure doesn't affect output)
2. Enable minification: `MINIFY_HTML=true`
3. Consider splitting into multiple "projects"
4. Use CI/CD to build automatically

### Custom Markdown Extensions

To add more Markdown extensions, edit `.env`:

```ini
MARKDOWN_EXTENSIONS=tables,fenced_code,codehilite,toc,attr_list,md_in_html,extra
```

## Advanced Template Tricks

### Dynamic Tab Icons

In template.html:
```html
<button class="tab-button" data-tab="api">
    <span class="icon">📚</span>
    <span class="label">API</span>
</button>
```

### Nested Navigation

```html
<nav class="sidebar-nav">
    <button class="tab-button" data-tab="intro">Introduction</button>
    <div class="section">
        <h3>Getting Started</h3>
        <button class="tab-button" data-tab="install">Installation</button>
        <button class="tab-button" data-tab="config">Configuration</button>
    </div>
    <div class="section">
        <h3>API Reference</h3>
        <button class="tab-button" data-tab="api">REST API</button>
    </div>
</nav>
```

### Search Functionality

Add to template.config.json:
```json
{
  "extra_js": [
    "https://cdn.jsdelivr.net/npm/lunr/lunr.min.js"
  ]
}
```

Then implement search in template.html (advanced JavaScript).

## Links to Other Sections

- [Configuration Guide](CONFIGURATION.md) - Detailed `.env` options
- [i18n Guide](I18N.md) - Multi-language setup
- [Template Development](TEMPLATE_DEVELOPMENT.md) - Create custom templates
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and fixes
