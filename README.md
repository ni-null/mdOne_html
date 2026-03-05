# MDOne HTML

A lightweight document packager that converts Markdown files into a single, self-contained HTML file with multi-language support and customizable templates.


<img width="1365" height="831" alt="Snipaste_2026-03-05_17-13-27" src="https://github.com/user-attachments/assets/1fb774d6-0554-43ef-89e2-433f241df411" />




## Features

- 📦 **Single-file Output** - Package multiple Markdown documents into one self-contained HTML file (offline-friendly)
- 🌍 **Multi-language Support** - Built-in i18n for English, Traditional Chinese, and extensible to other languages
- 🎨 **Flexible Templates** - Supports multiple templates with customizable styling and layout
- ⚙️ **Environment Configuration** - Easy setup via `.env` file
- 🔗 **External Resources** - Seamlessly integrate CDN CSS/JS resources
- 🎯 **CLI Arguments** - Control output via command-line parameters

## Quick Start

### 1. Install Dependencies

```bash
pip install python-dotenv markdown
```

### 2. Configure `.env`

```bash
cp .env.example .env
```

Edit `.env` with your settings:
```ini
MARKDOWN_SOURCE_DIR=./markdown
OUTPUT_FILE=documentation.html
DEFAULT_TEMPLATE=normal
LOCALE=en
```

### 3. Run

```bash
python main.py

# Or with options
python main.py --locale en --template normal --output docs.html
```

## Project Structure

```
.
├── main.py                    # Main packager script
├── .env                      # Local configuration (not committed)
├── .env.example              # Configuration template
├── templates/                # HTML templates
│   ├── normal/              # Default template
│   ├── minimal/             # Minimal template
│   └── your_template/       # Custom templates
├── locales/                 # Multi-language resources
│   ├── en.json             # English
│   └── zh-TW.json          # Traditional Chinese
├── docs/                    # Detailed documentation
│   ├── QUICK_START.md
│   ├── CONFIGURATION.md
│   ├── I18N.md
│   ├── TEMPLATE_DEVELOPMENT.md
│   └── ...
└── markdown/                # Your Markdown source files
```

## Documentation

For detailed information, see:

- [Configuration Guide](docs/CONFIGURATION.md)
- [Multi-language Setup](docs/I18N.md)
- [Template Development](docs/TEMPLATE_DEVELOPMENT.md)
- [Advanced Usage](docs/ADVANCED_USAGE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## Basic Usage

### Command-line Options

```bash
# Specify language
python main.py --locale zh-TW

# Specify template
python main.py --template minimal

# Specify output file
python main.py --output my_docs.html

# Markdown source directory
python main.py --source /path/to/markdown

# Combine options
python main.py --template minimal --locale en --output docs.html
```

## Creating a Custom Template

1. Create template directory: `templates/my_template/`
2. Add three required files:
   - `template.html` - HTML structure
   - `style.css` - Styling
   - `template.config.json` - Metadata and external resources

See [Template Development Guide](docs/TEMPLATE_DEVELOPMENT.md) for detailed instructions.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MARKDOWN_SOURCE_DIR` | `./markdown` | Markdown source directory |
| `OUTPUT_FILE` | `output.html` | Output HTML filename |
| `DEFAULT_TEMPLATE` | `normal` | Default template name |
| `LOCALE` | `en` | Language code (en, zh-TW) |
| `MINIFY_HTML` | `true` | Minify HTML output |
| `SITE_TITLE` | `Documentation` | Page title |

See [Configuration Guide](docs/CONFIGURATION.md) for all available options.

## License

MIT

### 模板設計原則

1. **使用 CSS 變數**
   
   ❌ 不好：
   ```css
   body { background: #fff; color: #333; }
   ```

   ✅ 好：
   ```css
   :root {
       --bg-primary: #fff;
       --text-primary: #333;
   }
   [data-theme="dark"] {
       --bg-primary: #1e1e1e;
       --text-primary: #fff;
   }
   body {
       background: var(--bg-primary);
       color: var(--text-primary);
   }
   ```

2. **避免硬編碼**
   
   ❌ 不好：
   ```html
   <span>Home</span>
   <span>Offline</span>
   ```

   ✅ 好：
   ```html
   <span>{I18N_BREADCRUMB_INDEX}</span>
   <span>{I18N_STATUS_OFFLINE}</span>
   ```

3. **靈活的 HTML 結構**
   - 使用 semantic HTML (`<header>`, `<aside>`, `<main>`, `<nav>`)
   - 避免過度 div 嵌套
   - 使用 CSS Grid/Flexbox 而不是 float

### 多語言支援

1. **新增語言**
   - 複製 `locales/en.json` 為 `locales/your_locale.json`
   - 翻譯 `cli` 和 `template` 區塊
   - 在使用時傳 `--locale your_locale`

2. **保持鍵名一致**
   ```json
   {
       "cli": {
           "app_title": "...",  // 開發者看見
       },
       "template": {
           "page_subtitle": "...",  // 使用者看見
       }
   }
   ```

### 效能最佳化

1. **啟用 HTML 壓縮**
   ```ini
   MINIFY_HTML=true
   ```

2. **優化外部資源**
   - 使用 CDN 資源時考慮檔案大小
   - 在 `template.config.json` 加入 CSS/JS
   - 避免重複引入相同資源

3. **檔案大小目標**
   - 典型文檔（10+ 個 Markdown 文件）應 < 500KB
   - 樣式表應 < 50KB
   - 圖片應透過 Markdown 外連（不內嵌）

### 可訪問性 (Accessibility)

1. 使用語義 HTML：`<nav>`, `<main>`, `<article>`, `<aside>`
2. 提供 `title` 和 `aria-label` 屬性
3. 確保色差對比度 (WCAG AA 標準)
4. 支援鍵盤導航

### 相容性

- 支援現代瀏覽器 (Chrome, Firefox, Safari, Edge)
- 建議不支援 IE11（已停止支援）
- 使用 CSS Grid 和 Flexbox（廣泛支援）
- 避免 CSS Grid 子網格（某些舊版本瀏覽器不支援）

### 版本管理

MDOne 使用雙版本系統：

#### 1. 模板版本 (`version`)

追蹤模板本身的功能演進，獨立於主程式版本。

**版本號格式**：語義版本 `MAJOR.MINOR.PATCH`

**何時升級**：
- **主版本 (1.0.0 → 2.0.0)**：破壞性改動
  - 移除 i18n 佔位符
  - 改變必需的 HTML 類名或結構
  
- **次版本 (1.0.0 → 1.1.0)**：向後相容新功能
  - 新增 i18n 佔位符
  - 新增 CSS 變數
  
- **修訂版本 (1.0.0 → 1.0.1)**：修正和最佳化
  - 修正樣式 bug
  - 改進響應式設計

#### 2. Schema 版本 (`schema_version`)

標明模板與主程式 API 的相容性。

**版本格式**：`v1`, `v2`, `v3` 等

**用途**：未來主程式有重大更新（如 v2.0）時，舊模板可能需要升級。

**範例**：
```
主程式 v1.0 + schema_version: v1 → ✓ 相容
主程式 v2.0 + schema_version: v1 → ✗ 不相容
主程式 v2.0 + schema_version: v2 → ✓ 相容
```

#### 實際例子

```
normal 模板演進過程：

v1.0.0 (schema: v1) → 初始版本，與主程式 v1.x 兼容
 ↓
v1.1.0 (schema: v1) → 新增深色主題，仍與 v1.x 兼容
 ↓
v1.1.1 (schema: v1) → 修正行距問題
 ↓
v2.0.0 (schema: v1) → 全面改版設計，仍兼容主程式 v1.x
 ↓
v2.1.0 (schema: v2) → 使用 v2 API 新功能（主程式需升至 v2.0+）

```

#### 檢查版本

打包器在加載模板時會顯示版本：

```bash
python main.py --template my_template
# 輸出示例：
# Template version: 1.0.0 (schema: v1)
```

#### 版本兼容性檢查（未來功能）

未來主程式可能添加自動檢查，例如：
```bash
# 如果 schema_version 不匹配，拒絕加載或發出警告
python main.py --template old_template
# ✚ 警告：此模板使用 schema v1，主程式已升至 v2
# ℹ 請升級模板或使用 --force 繼續
```

---

## 模板開發常見問題

### Q: 如何自訂配色？

**A:** 在 `style.css` 修改 CSS 變數：

```css
:root {
    --primary-color: #2563eb;      /* 主色 */
    --bg-primary: #ffffff;         /* 背景 */
    --text-primary: #1e293b;       /* 文字 */
}

[data-theme="dark"] {
    /* 深色主題的變數... */
}
```

### Q: 如何添加自訂字體？

**A:** 在 `template.config.json` 加入 Google Fonts CDN：

```json
{
    "extra_css": [
        "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
    ]
}
```

然後在 `style.css` 使用：

```css
body { font-family: 'Roboto', sans-serif; }
```

### Q: 如何添加程式碼高亮？

**A:** 在 `template.config.json` 加入 Highlight.js：

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

### Q: 如何隱藏某些頁籤？

**A:** 修改 `template.html` 的 `{TABS_HTML}` 區域，但這需要修改 `main.py`。更簡單的方法是用 CSS 隱藏：

```css
.tab-button[data-tab="internal-docs"] {
    display: none;
}
```

### Q: 如何添加頁腳連結？

**A:** 在 `template.html` 的頁腳區域修改，並在 `locales/*.json` 的 `template` 加入對應鍵。

---

## 最佳實踐

---

## 故障排查

| 問題 | 檢查事項 |
|---|---|
| 找不到模板 | 確認 `templates/template_name/` 存在 `style.css` 和 `template.html` |
| 語言未改變 | 確認 `.env` 的 `LOCALE` 值且對應的 `locales/*.json` 存在 |
| 佔位符未替換 | 檢查模板中佔位符名稱是否正確（大小寫敏感） |
| 樣式未加載 | 檢查 `style.css` 是否有 CSS 語法錯誤 |
| Markdown 無法讀取 | 確認 `MARKDOWN_SOURCE_DIR` 目錄存在且包含 `.md` 檔案 |
| `.env` 未讀取 | 確認檔案名稱為 `.env`（不是 `.env.txt`） |

---

## 更新日誌

### v1.0.0 (2024-03)
- ✅ 完全重構：環境變數配置（`.env`）
- ✅ 新增：多語言支援（i18n）
- ✅ 新增：外部資源管理（CDN CSS/JS）
- ✅ 新增：命令行參數（`--template`, `--locale`, 等）
- ✅ 改進：模板佔位符規範化
- ✅ 改進：日誌系統與錯誤訊息

---

## 許可證

MIT

