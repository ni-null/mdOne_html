# Documentation Index

Welcome to MDOne documentation. Find the guide you need:

## 🚀 Getting Started

**Just getting started?** Start here:

1. [Quick Start](#quick-start) - 5-minute setup
2. [Configuration Guide](CONFIGURATION.md) - Setup `.env` file
3. [Running First Time](CONFIGURATION.md#setup) - Initial setup

## 📚 Main Guides

### [Configuration Guide](CONFIGURATION.md)
Set up and configure MDOne with environment variables and command-line options.

- `.env` file setup
- All environment variables explained
- Command-line arguments
- Template configuration
- Dynamic footer dates
- Next steps

**Read this if:** You need to configure settings or understand all available options.

### [Multi-language Support (i18n) Guide](I18N.md)
Add support for multiple languages in your documentation.

- Language file structure
- Using i18n in templates
- All available placeholders
- Adding new languages step-by-step
- Translation checklist
- Best practices

**Read this if:** You want to support multiple languages or translate existing content.

### [Template Development Guide](TEMPLATE_DEVELOPMENT.md)
Create custom HTML templates with your own styling and layout.

- Template file structure
- Template requirements
- HTML placeholders
- CSS styling and dark theme support
- External resources (CDN)
- Development workflow
- Common customizations
- Troubleshooting

**Read this if:** You want to create custom templates or modify existing ones.

### [Advanced Usage Guide](ADVANCED_USAGE.md)
Learn advanced features and integration scenarios.

- Full command-line reference
- Markdown organization tips
- Batch processing
- Automation and CI/CD integration
- Performance optimization
- Deployment options
- Docker support
- Multiple languages/templates

**Read this if:** You have advanced needs like CI/CD integration or batch processing.

### [Troubleshooting Guide](TROUBLESHOOTING.md)
Common issues and how to fix them.

- Error messages explained
- Debugging tips
- File encoding issues
- Performance problems
- HTML validation
- Step-by-step solutions

**Read this if:** Something isn't working or you're seeing errors.

### [Changelog](CHANGELOG.md)
Version history and what changed.

- v1.0.0 feature list
- Technical details
- Browser compatibility
- Known limitations
- Future roadmap
- Migration guides

**Read this if:** You want to know what's new or track project updates.

---

## 🎯 Find Answers by Task

### I want to...

#### Set up MDOne
→ Start with [Configuration Guide](CONFIGURATION.md)

#### Use a different language
→ Read [i18n Guide](I18N.md)

#### Create my custom template
→ Read [Template Development Guide](TEMPLATE_DEVELOPMENT.md)

#### Deploy to production
→ See [Advanced Usage](ADVANCED_USAGE.md#deployment)

#### Automate building (CI/CD)
→ See [Advanced Usage](ADVANCED_USAGE.md#integration-with-cicd)

#### Something isn't working
→ Check [Troubleshooting Guide](TROUBLESHOOTING.md)

#### Understand all options
→ Read [Configuration Guide](CONFIGURATION.md)

#### Generate multiple outputs
→ See [Advanced Usage](ADVANCED_USAGE.md#batch-processing)

#### Add custom fonts/styling
→ Read [Template Development - CSS](TEMPLATE_DEVELOPMENT.md#stylecss)

#### Support multiple teams/brands
→ See [Advanced Usage - Scenarios](ADVANCED_USAGE.md#customization-scenarios)

---

## 📖 Quick Reference

### Files to Know

| File | Purpose | Edit? |
|------|---------|-------|
| `.env.example` | Configuration template | ✓ Copy to `.env` |
| `.env` | Your local config | ✓ Edit with your settings |
| `main.py` | Main program | ✗ Usually don't edit |
| `templates/*/` | HTML templates | ✓ Customize or create new |
| `locales/*.json` | Language strings | ✓ Add translations |
| `markdown/` | Your content | ✓ Add `.md` files |

### Command Quick Ref

```bash
# Basic run with .env settings
python main.py

# Specify everything
python main.py --template normal --locale en --output docs.html

# Generate multiple versions
python main.py --locale en --output docs-en.html
python main.py --locale zh-TW --output docs-zh.html
```

For more: See [Advanced Usage](ADVANCED_USAGE.md#command-line-options)

### Key Concepts

- **`MARKDOWN_SOURCE_DIR`** - Folder with your `.md` files
- **`OUTPUT_FILE`** - Name of generated HTML file
- **`DEFAULT_TEMPLATE`** - Which template to use
- **`LOCALE`** - Language code (en, zh-TW)
- **`.env`** - Configuration file (git-ignored)
- **`template.html`** - HTML structure
- **`style.css`** - Styling and layout
- **`template.config.json`** - Template metadata

### Placeholders in Templates

| Placeholder | Replaced with |
|-------------|---|
| `{LANG}` | Language code |
| `{TITLE}` | Site title |
| `{CSS_CONTENT}` | Stylesheet content |
| `{TABS_HTML}` | Tab buttons |
| `{CONTENT_HTML}` | Markdown content |
| `{I18N_KEY}` | Translated strings |
| `{EXTRA_CSS}` | External stylesheets |
| `{EXTRA_JS}` | External scripts |

For complete list: See [Template Development](TEMPLATE_DEVELOPMENT.md#required-placeholders)

---

## 🆘 Need Help?

### I'm getting an error

1. Read the error message carefully
2. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
3. Common issues include:
   - `.env` file not found → Create from `.env.example`
   - Markdown directory empty → Add `.md` files to `markdown/`
   - Template not found → Check template name and directory
   - Locale not found → Verify language file exists

### Something isn't clear

1. Search this documentation using browser Ctrl+F
2. Check the relevant guide section
3. Look at examples in the guide

### I found a bug

Check [Troubleshooting Guide](TROUBLESHOOTING.md) first, then:
1. Note the exact error message
2. Include your `.env` settings
3. Include steps to reproduce
4. Include your Python version: `python --version`

---

## 📋 Learning Path

### Beginner (First time users)
1. Main [README](../README.md)
2. [Configuration Guide](CONFIGURATION.md) - Setup
3. [Quick Start](CONFIGURATION.md#setup)
4. [Troubleshooting](TROUBLESHOOTING.md) - if issues

### Intermediate (Building custom templates)
5. [Template Development](TEMPLATE_DEVELOPMENT.md)
6. Study existing templates in `templates/`
7. [i18n Guide](I18N.md) - Add translations

### Advanced (Automation & deployment)
8. [Advanced Usage](ADVANCED_USAGE.md)
9. [CI/CD Integration](ADVANCED_USAGE.md#integration-with-cicd)
10. [Deployment](ADVANCED_USAGE.md#deployment)

---

## 📝 Documentation Structure

```
docs/
├── CONFIGURATION.md        ← Start here for setup
├── I18N.md                ← Multi-language support
├── TEMPLATE_DEVELOPMENT.md ← Create custom templates
├── ADVANCED_USAGE.md      ← Advanced features
├── TROUBLESHOOTING.md     ← Common issues & fixes
├── CHANGELOG.md           ← Version history
└── README.md              ← This file
```

---

## ✅ Documentation Checklist

Before asking for help:

- [ ] I've read the relevant guide
- [ ] I've checked [Troubleshooting Guide](TROUBLESHOOTING.md)
- [ ] I've searched documentation with Ctrl+F
- [ ] I've verified `.env` file exists and is readable
- [ ] I've verified markdown files exist in `MARKDOWN_SOURCE_DIR`
- [ ] I've verified template directory exists

---

## 🔗 External Resources

- [Markdown Syntax](https://www.markdownguide.org/)
- [Python Documentation](https://docs.python.org/)
- [CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [HTML Reference](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [Git Guide](https://git-scm.com/doc)

---

**Last Updated:** 2024-03-05  
**Version:** 1.0.0

Happy documenting! 📚
