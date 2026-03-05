# Troubleshooting Guide

## Common Issues

### 1. "No markdown files found" Error

**Symptom:** Error message when running `python main.py`

**Causes:**
- `MARKDOWN_SOURCE_DIR` points to non-existent directory
- Directory exists but contains no `.md` files
- File permissions prevent reading

**Solutions:**

```bash
# 1. Verify directory exists
ls markdown/  # Linux/macOS
dir markdown  # Windows

# 2. Create directory if missing
mkdir markdown

# 3. Add a test markdown file
echo "# Test" > markdown/test.md

# 4. Check file permissions
chmod 644 markdown/*.md  # Linux/macOS

# 5. Run again
python main.py
```

### 2. "Template not found" Error

**Symptom:** Template directory couldn't be located

**Solutions:**

```bash
# 1. Verify template directory exists
ls templates/

# 2. Check template name matches directory name
# If using "my_template", verify:
#   - Directory: templates/my_template/
#   - Command: python main.py --template my_template

# 3. Verify required files exist
ls templates/my_template/
# Should show:
# - template.html
# - style.css
# - template.config.json
```

### 3. `.env` File Not Read

**Symptom:** Settings from `.env` not applied, using defaults instead

**Solutions:**

```bash
# 1. Verify file naming - must be exactly ".env"
ls -la | grep env  # Linux/macOS
dir | findstr env  # Windows

# Issue: .env.txt or .env.bak won't work
# Solution: Rename to .env (no extension)

# 2. Verify file location - must be in project root
pwd  # Check current directory
# Should be in same directory as main.py

# 3. Verify file syntax
# Check for syntax errors:
cat .env  # Linux/macOS
type .env  # Windows

# 4. In Windows, ensure file doesn't have hidden .txt extension
# Use: Rename to ".env" (with quotes)
```

### 4. Language Not Changing

**Symptom:** `--locale` argument ignored or text not translating

**Solutions:**

```bash
# 1. Verify language file exists
ls locales/

# If using --locale zh-TW:
# Check: locales/zh-TW.json exists

# 2. Verify LOCALE code in .env matches filename
# In .env:
LOCALE=zh-TW

# In locales/:
# ✓ locales/zh-TW.json
# ✗ locales/zh_tw.json  (underscore won't work)
# ✗ locales/zh-cn.json  (different code)

# 3. Verify JSON syntax in language file
python -c "import json; json.load(open('locales/YOUR_LOCALE.json'))"

# 4. Test with known working language
python main.py --locale en
```

### 5. Placeholders Not Replaced

**Symptom:** i18n placeholders like `{I18N_PAGE_SUBTITLE}` appear in output HTML

**Causes:**
- Placeholder name misspelled in template
- Placeholder missing from locales JSON
- Template syntax error

**Solutions:**

```bash
# 1. Verify placeholder format
# ✓ Correct: {I18N_PAGE_SUBTITLE}
# ✗ Wrong: {i18n_page_subtitle}  (must be uppercase)
# ✗ Wrong: {I18N_Page_Subtitle}  (uppercase only)

# 2. Check JSON has the key
# For placeholder {I18N_PAGE_SUBTITLE}, check:
# In locales/en.json:
# {
#   "template": {
#     "page_subtitle": "..."  <-- This is the key
#   }
# }

# 3. Verify JSON syntax
python -m json.tool locales/en.json > /dev/null && echo "Valid JSON"

# 4. Common placeholder/key mapping
# Placeholder            → JSON key
# {I18N_PAGE_SUBTITLE}   → template.page_subtitle
# {I18N_LOADING}         → template.loading
# {I18N_FOOTER_LABEL}    → template.footer_label
```

### 6. Styles Not Loading / Broken Layout

**Symptom:** Generated HTML has no styling or layout is broken

**Solutions:**

```bash
# 1. Check CSS syntax
# Verify style.css has no errors
python -m css_validator templates/MY_TEMPLATE/style.css

# Or manually check in browser:
# Open .html file → F12 → Console → check for CSS errors

# 2. Verify CSS placeholder replaced
# In generated HTML (view source), check:
# ✓ <style>...actual CSS content...</style>
# ✗ <style>{CSS_CONTENT}</style>  (not replaced)

# 3. Check CSS variables are defined
# In style.css, must have:
:root {
    --bg-primary: #fff;
    --text-primary: #333;
}

# 4. Verify template includes CSS placeholder
# template.html must have:
# <style>{CSS_CONTENT}</style>

# 5. Check for typos in CSS variable names
# ✓ color: var(--text-primary);
# ✗ color: var(--textPrimary);   (camelCase won't work)
```

### 7. Tabs Don't Switch Content

**Symptom:** Clicking tabs does nothing, content doesn't change

**Solutions:**

```bash
# 1. Verify HTML structure
# In generated HTML, check:
# ✓ <button class="tab-button" data-tab="doc-name">
# ✓ <div class="tab-content" data-tab="doc-name">

# Missing classes/attributes will break functionality

# 2. Check CSS for .active class
# In style.css, must have:
.tab-content { display: none; }
.tab-content.active { display: block; }

# 3. Verify JavaScript is present
# In generated HTML, check:
# ✓ <script>...JavaScript code...</script>
# ✗ <script>{THEME_INIT}</script>  (not replaced)

# 4. Check browser console (F12)
# Look for JavaScript errors

# 5. Verify template has tab switching code
# template.html must have JavaScript like:
document.querySelectorAll('.tab-button').forEach(btn => {
    btn.addEventListener('click', function() {
        // switching logic
    });
});
```

### 8. Theme Toggle Not Working

**Symptom:** Theme button present but dark mode doesn't work

**Solutions:**

```bash
# 1. Verify CSS has dark theme variables
# style.css must have:
[data-theme="dark"] {
    --bg-primary: #1e1e1e;
    --text-primary: #fff;
}

# 2. Check HTML root element
# <html> tag must allow data-theme attribute:
# ✓ <html lang="{LANG}">
# ✓ <html data-theme="light">  (gets set by JS)

# 3. Verify CSS uses variables
# ✓ background: var(--bg-primary);
# ✗ background: #ffffff;  (hardcoded color stays same)

# 4. Check {THEME_INIT} is in template
# template.html must have:
# <script>{THEME_INIT}</script>

# 5. Verify theme button element
# Optional but recommended:
# <button id="theme-toggle">...</button>
```

### 9. UTF-8 / Encoding Issues

**Symptom:** Chinese/special characters appear as garbled text

**Solutions:**

```bash
# 1. Verify file encoding
# All JSON files must be UTF-8
# In editor: Set encoding to UTF-8

# Windows Notepad:
# - Open file
# - Save As → Encoding: UTF-8

# VS Code:
# - Bottom right: Click encoding
# - Select "UTF-8"

# 2. Verify HTML meta tag
# template.html must have:
# <meta charset="UTF-8">

# 3. Check JSON files have UTF-8 BOM removed
# (most editors handle this automatically)

# 4. Verify locale file is valid JSON
python -m json.tool locales/zh-TW.json > /dev/null
```

### 10. Performance / File Size Too Large

**Symptom:** Generated HTML file is very large (>10MB)

**Solutions:**

```bash
# 1. Enable HTML minification
# In .env:
MINIFY_HTML=true

# This reduces size by ~20-30%

# 2. Check for large external resources
# In template.config.json:
# Avoid large libraries (>500KB)
# Use minified versions:
# ✓ filename.min.js   (minified)
# ✗ filename.js       (full source)

# 3. Reduce markdown files
# Fewer markdown files = smaller HTML
# Split into multiple projects if needed

# 4. Remove unused styling
# Delete unused CSS rules
# Remove unused external CSS

# 5. Check file size
# Windows: dir  /s MY_TEMPLATE.html
# Linux/macOS: ls -lh my_template.html
```

## Debugging

### Enable Verbose Output

```bash
# Add python debugging
python -u main.py 2>&1 | tee output.log

# This saves all output to output.log file
```

### Check Generated HTML

```bash
# Open in browser and inspect
# F12 → Elements/Inspector → Check structure

# View source:
# Right-click → View Page Source

# Or check with command line
# Windows PowerShell:
Get-Content output.html -Head 50  # First 50 lines

# Linux/macOS:
head -50 output.html
```

### Validate HTML

```bash
# Use online validator
# https://validator.w3.org/

# Or command line:
python -m html
