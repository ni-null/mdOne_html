# Template Development Guide

## Overview

Templates control the HTML structure, styling, and layout of your output. Each template includes:

- `template.html` - HTML structure
- `style.css` - Styling
- `template.config.json` - Metadata and external resources

## Quick Start

### Copy Existing Template

```bash
cp -r templates/normal templates/my_template
```

### Modify Files

1. Edit `templates/my_template/template.html`
2. Edit `templates/my_template/style.css`
3. Update `templates/my_template/template.config.json`

### Test

```bash
python main.py --template my_template --output test.html
```

## File Structure

```
templates/my_template/
├── template.html          # Main HTML template
├── style.css             # Stylesheet
└── template.config.json  # Metadata & external resources
```

## template.html

The main HTML file with placeholders for dynamic content.

### Required Placeholders

| Placeholder | Purpose | Source |
|------------|---------|--------|
| `{LANG}` | HTML lang attribute | `.env` LOCALE |
| `{TITLE}` | Page title | `.env` SITE_TITLE |
| `{CSS_CONTENT}` | Inline styles | style.css |
| `{TABS_HTML}` | Document tabs | Auto-generated |
| `{CONTENT_HTML}` | Document content | Auto-generated |
| `{THEME_INIT}` | Theme initialization | Auto-generated |
| `{EXTRA_CSS}` | External <link> tags | template.config.json |
| `{EXTRA_JS}` | External <script> tags | template.config.json |

### i18n Placeholders

```html
{I18N_PAGE_SUBTITLE}
{I18N_LOADING}
{I18N_FOOTER_LABEL}
{I18N_MENU_OPEN_TITLE}
<!-- etc. - see I18N.md for complete list -->
```

### Minimum Template

```html
<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE}</title>
    <style>
{CSS_CONTENT}
    </style>
{EXTRA_CSS}
</head>
<body>
    <aside class="sidebar">
        <h1>{TITLE}</h1>
        <nav class="tabs">
{TABS_HTML}
        </nav>
    </aside>
    
    <main class="content">
{CONTENT_HTML}
    </main>

    <script>
{THEME_INIT}

        // Tab switching: required
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.addEventListener('click', function() {
                const tab = this.getAttribute('data-tab');
                
                // Hide all content
                document.querySelectorAll('.tab-content').forEach(c => {
                    c.classList.remove('active');
                });
                
                // Deactivate all buttons
                document.querySelectorAll('.tab-button').forEach(b => {
                    b.classList.remove('active');
                });
                
                // Show selected content
                document.querySelector(`.tab-content[data-tab="${tab}"]`).classList.add('active');
                
                // Activate button
                this.classList.add('active');
            });
        });
    </script>
{EXTRA_JS}
</body>
</html>
```

### Generated HTML Structure

**Tabs** (`{TABS_HTML}` generates):
```html
<button class="tab-button active" data-tab="document-name">
    Document Name
</button>
```

**Content** (`{CONTENT_HTML}` generates):
```html
<div class="tab-content active" data-tab="document-name">
    <h1>Document Name</h1>
    <!-- Markdown HTML content -->
</div>
```

**Required Classes:**
- `.tab-button` - Clickable tab with `data-tab` attribute
- `.tab-content` - Content container with matching `data-tab` attribute
- `.active` - Class for active tab/content (show/hide via CSS)

## style.css

### CSS Variables (Dark Theme Support)

```css
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f5;
    --text-primary: #333333;
    --text-secondary: #666666;
    --border-color: #e0e0e0;
    --accent-color: #0066cc;
}

[data-theme="dark"] {
    --bg-primary: #1e1e1e;
    --bg-secondary: #2d2d2d;
    --text-primary: #ffffff;
    --text-secondary: #cccccc;
    --border-color: #404040;
    --accent-color: #6699ff;
}

body {
    background: var(--bg-primary);
    color: var(--text-primary);
}

.tab-button {
    border-color: var(--border-color);
}

.tab-button.active {
    color: var(--accent-color);
}
```

### Tab Styling

```css
.tab-button {
    cursor: pointer;
    padding: 8px 16px;
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    transition: all 0.3s ease;
}

.tab-button:hover {
    background: var(--bg-secondary);
}

.tab-button.active {
    background: var(--accent-color);
    color: white;
    border-color: var(--accent-color);
}

.tab-content {
    display: none;
    padding: 20px;
}

.tab-content.active {
    display: block;
}
```

### Responsive Design

```css
@media (max-width: 768px) {
    .sidebar {
        width: 100%;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .tabs {
        flex-wrap: wrap;
    }
    
    .content {
        width: 100%;
    }
}
```

### Best Practices

✅ **DO:**
- Use CSS variables for colors
- Use semantic HTML elements
- Define both light and dark themes
- Make design responsive
- Use flexbox/grid for layout

❌ **DON'T:**
- Hardcode colors
- Use inline styles excessively
- Assume desktop-only layout
- Use deprecated HTML features
- Reference external images without CDN

## template.config.json

Metadata and external resource declarations.

```json
{
  "_metadata": {
    "name": "my_template",
    "description": "My custom template",
    "version": "1.0.0",
    "schema_version": "v1",
    "author": "Your Name"
  },
  "extra_css": [
    "https://cdn.jsdelivr.net/npm/highlight.js/styles/github.css",
    "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
  ],
  "extra_js": [
    "https://cdn.jsdelivr.net/npm/highlight.js/highlight.min.js"
  ]
}
```

### _metadata Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | ✓ | Template name (lowercase, matches directory) |
| `description` | ✓ | Short description |
| `version` | ✓ | Semantic version (MAJOR.MINOR.PATCH) |
| `schema_version` | ✓ | API version compatibility (v1, v2, etc.) |
| `author` | | Author/organization name |

### Version Strategy

**Template Version** (e.g., 1.2.3):
- **MAJOR**: Breaking changes (removed placeholders, API changes)
- **MINOR**: New features (new i18n keys, CSS vars)
- **PATCH**: Fixes (style tweaks, bugs)

**Schema Version** (v1, v2, ...):
- Marks compatibility with main program version
- Future-proofs when main program changes API

### External Resources

**CDN Best Practices:**

1. Use established CDN providers:
   - jsDelivr: `https://cdn.jsdelivr.net/npm/`
   - CDN.js: `https://cdnjs.cloudflare.com/ajax/libs/`
   - Google Fonts: `https://fonts.googleapis.com/`

2. Pin specific versions:
   ```json
   "https://cdn.jsdelivr.net/npm/highlight.js@11.8.0/styles/github.css"
   ```

3. Use HTTPS always

4. Minimize external requests - combine when possible

## Theme Support

The `{THEME_INIT}` placeholder auto-generates theme switching code.

Your template must provide:

1. **HTML Root Element**:
   ```html
   <html lang="{LANG}">  <!-- Gets data-theme attribute -->
   ```

2. **Theme Toggle Button** (optional):
   ```html
   <button id="theme-toggle" title="{I18N_THEME_TOGGLE_TITLE}">
       <span id="theme-icon">☀</span>
       <span id="theme-label">{I18N_THEME_LIGHT_LABEL}</span>
   </button>
   ```

3. **CSS Variables**:
   ```css
   [data-theme="dark"] {
       /* Dark theme variables */
   }
   ```

## Development Workflow

### 1. Start from Existing Template

```bash
cp -r templates/normal templates/my_template
cd templates/my_template
```

### 2. Iterative Development

- Modify CSS
- Test with: `python main.py --template my_template`
- Check browser dev tools (F12)
- Repeat

### 3. Testing Checklist

- [ ] Tabs switch content
- [ ] Styles load correctly
- [ ] i18n strings replaced (no `{I18N_*}` visible)
- [ ] Theme toggle works
- [ ] Responsive design (resize browser)
- [ ] Works in multiple browsers
- [ ] Offline mode (save page as HTML)

### 4. Git Workflow

Commit template files:
```bash
git add templates/my_template/
git commit -m "Add my_template"
```

## Common Customizations

### Add Google Fonts

In `template.config.json`:
```json
{
  "extra_css": [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
  ]
}
```

In `style.css`:
```css
body {
    font-family: 'Inter', sans-serif;
}
```

### Add Syntax Highlighting

In `template.config.json`:
```json
{
  "extra_css": [
    "https://cdn.jsdelivr.net/npm/highlight.js/styles/atom-one-dark.css"
  ],
  "extra_js": [
    "https://cdn.jsdelivr.net/npm/highlight.js/highlight.min.js"
  ]
}
```

In your HTML template after `{CONTENT_HTML}`:
```html
<script>
    hljs.highlightAll();
</script>
```

### Custom Theme Colors

In `style.css`:
```css
:root {
    /* Brand colors */
    --primary: #6366f1;
    --secondary: #06b6d4;
    /* Apply to UI */
    --accent-color: var(--primary);
}
```

### Hide Tab Labels

In `style.css`:
```css
.tab-button {
    width: 40px;
    overflow: hidden;
    text-indent: -9999px;
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Placeholder not replaced | Check syntax: `{PLACEHOLDER_NAME}` (uppercase) |
| Styles not applied | Check CSS Variables spelling |
| Tabs don't work | Verify `.tab-button`, `.tab-content`, `data-tab` attributes |
| i18n text shows `{I18N_*}` | Check locales/*.json has that key |
| Theme not switching | Verify `<html>` has no data-theme set initially |
| External CSS not loading | Check URL is HTTPS and valid |
| Content doesn't display | Ensure `.tab-content.active { display: block; }` in CSS |

## Next Steps

- Review [Multi-language Support](I18N.md)
- Check [Advanced Usage](ADVANCED_USAGE.md)
- Submit your template to the project!
