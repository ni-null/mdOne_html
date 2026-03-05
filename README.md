# MDOne Template System - 模板系統指南

## 概述

MDOne 是一個通用的文檔打包器，支援：
- ✅ 多語言支援（i18n）- 英文、繁體中文等
- ✅ 環境變數配置（`.env`）
- ✅ 外部資源引入（CDN CSS/JS）
- ✅ 靈活的模板系統
- ✅ 輸出單一自含式 HTML 檔案（離線使用）

---

## 目錄結構

```
project_root/
├── .env                           ← 環境變數（本地配置，不提交 git）
├── .env.example                   ← 範本說明（提交 git）
├── main.py                        ← 主打包器腳本
├── locales/                       ← 多語言資源
│   ├── en.json                    ← 英文字串
│   └── zh-TW.json                 ← 繁體中文字串
├── templates/                     ← 模板根目錄
│   ├── normal/                    ← 預設模板
│   │   ├── style.css              ← 模板樣式
│   │   ├── template.html          ← 模板 HTML
│   │   └── template.config.json   ← 模板配置（CDN 資源）
│   └── your_template/             ← 自訂模板
│       ├── style.css
│       ├── template.html
│       └── template.config.json
└── markdown/                      ← Markdown 源文件目錄
    ├── doc1.md
    └── doc2.md
```

---

## 快速開始

### 1. 安裝依賴

```bash
pip install python-dotenv markdown
```

### 2. 配置 `.env` 檔案

複製 `.env.example` 為 `.env` 並設定：

```bash
cp .env.example .env
```

編輯 `.env`：

```ini
# Markdown 源目錄
MARKDOWN_SOURCE_DIR=./markdown

# 輸出 HTML 檔名
OUTPUT_FILE=system_guide.html

# 預設模板
DEFAULT_TEMPLATE=normal

# 語系：en 或 zh-TW
LOCALE=zh-TW

# HTML 壓縮
MINIFY_HTML=true
```

### 3. 執行打包器

```bash
# 使用 .env 的預設設定
python main.py

# 或指定語系
python main.py --locale en

# 或指定模板
python main.py --template normal --locale zh-TW
```

---

## 環境變數配置（`.env`）

| 變數名 | 說明 | 預設值 | 範例 |
|---|---|---|---|
| `MARKDOWN_SOURCE_DIR` | Markdown 源目錄 | `./markdown` | `C:\docs\markdown` |
| `OUTPUT_FILE` | 輸出 HTML 檔名 | `system_guide.html` | `docs.html` |
| `DEFAULT_TEMPLATE` | 預設模板名稱 | `normal` | `minimal` |
| `TEMPLATES_DIR` | 模板根目錄 | `templates` | `./my_templates` |
| `MINIFY_HTML` | 是否壓縮 HTML | `true` | `true` / `false` |
| `MARKDOWN_EXTENSIONS` | Markdown 擴展 | `tables,fenced_code,...` | (逗號分隔) |
| `SITE_TITLE` | 頁面標題 | `Documentation` | `My Docs` |
| `THEME_MODE` | 初始主題 | `light` | `light` / `dark` |
| `LOCALE` | 語系代碼 | `en` | `en` / `zh-TW` |
| `BUILD_DATE` | 構建日期 | (自動今日) | `2024.03.05` |
| `LOCALES_DIR` | 語言資源目錄 | `locales` | `./i18n` |

---

## 多語言支援（i18n）

### 語言資源檔結構

`locales/en.json` 和 `locales/zh-TW.json` 包含兩個主要部分：

#### `cli` 區塊 - 工具訊息

打包器本身的 CLI 輸出、錯誤訊息。只對開發者可見。

```json
{
  "cli": {
    "app_title": "MDOne HTML Packager",
    "err_no_templates": "[ERROR] No templates found.",
    "success": "[OK] Done!"
  }
}
```

#### `template` 區塊 - UI 字串

注入到輸出 HTML 的使用者界面字串，通過佔位符 `{I18N_*}` 替換。

```json
{
  "template": {
    "html_lang": "en",
    "page_subtitle": "Documentation",
    "loading": "Loading...",
    "theme_light_label": "Light",
    "theme_dark_label": "Dark"
  }
}
```

### 支援的語言

- **en** - English（英文）
- **zh-TW** - 繁體中文

### 新增語言支援

1. 複製 `locales/en.json` 為 `locales/your_locale.json`
2. 翻譯所有 `cli` 和 `template` 鍵值
3. 在 `.env` 設定 `LOCALE=your_locale`
4. 模板中自動使用新語言

---

## 創建自訂模板

### 步驟 1：建立模板目錄

```bash
mkdir templates/my_template
```

### 步驟 2：建立 `style.css`

定義所有樣式。使用 CSS 變數便於主題切換：

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

### 步驟 3：建立 `template.html`

HTML 模板，使用佔位符注入內容。

#### 必須的佔位符

| 佔位符 | 來源 | 說明 |
|---|---|---|
| `{LANG}` | `.env` `LOCALE` | HTML `lang` 屬性 |
| `{TITLE}` | `.env` `SITE_TITLE` | 頁面標題 |
| `{CSS_CONTENT}` | `style.css` | 樣式內容（內嵌） |
| `{TABS_HTML}` | 自動生成 | 側邊欄頁籤按鈕 |
| `{CONTENT_HTML}` | 自動生成 | Markdown 內容 HTML |
| `{THEME_INIT}` | 自動生成 | 主題初始化腳本 |
| `{EXTRA_CSS}` | `template.config.json` | 外部 CSS `<link>` 標籤 |
| `{EXTRA_JS}` | `template.config.json` | 外部 JS `<script>` 標籤 |

#### i18n 佔位符

模板中使用 `{I18N_KEY}` 引入多語言字串。使用 UPPERCASE 的鍵名（對應 `locales/*.json` 中 `template.*` 的鍵）：

| 佔位符 | 對應 JSON key | 說明 |
|---|---|---|
| `{I18N_HTML_LANG}` | `template.html_lang` | HTML `lang` 屬性（例：`en`, `zh-TW`） |
| `{I18N_PAGE_SUBTITLE}` | `template.page_subtitle` | 頁面副標題 |
| `{I18N_LOADING}` | `template.loading` | 載入中文字 |
| `{I18N_FOOTER_LABEL}` | `template.footer_label` | 頁腳標籤（支援 `{BUILD_DATE}` 佔位符） |
| `{I18N_MENU_OPEN_TITLE}` | `template.menu_open_title` | 選單按鈕 title 屬性 |
| `{I18N_BREADCRUMB_DOCS}` | `template.breadcrumb_docs` | 麵包屑「文件」標籤 |
| `{I18N_BREADCRUMB_INDEX}` | `template.breadcrumb_index` | 麵包屑起始標籤 |
| `{I18N_STATUS_OFFLINE}` | `template.status_offline` | 離線狀態標籤 |
| `{I18N_THEME_LIGHT_LABEL}` | `template.theme_light_label` | 淺色主題標籤 |
| `{I18N_THEME_DARK_LABEL}` | `template.theme_dark_label` | 深色主題標籤 |
| `{I18N_THEME_TOGGLE_TITLE}` | `template.theme_toggle_title` | 主題按鈕 title 屬性 |
| `{I18N_DOC_COUNT_SUFFIX}` | `template.doc_count_suffix` | 文檔計數後綴（例：「份」） |

#### 最小模板範例

```html
<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <title>{TITLE}</title>
    <style>
{CSS_CONTENT}
    </style>
{EXTRA_CSS}
</head>
<body>
    <div class="sidebar">
        <h1>{TITLE}</h1>
        <div class="tabs">
{TABS_HTML}
        </div>
    </div>
    <div class="content">
{CONTENT_HTML}
    </div>
    <script>
        // Theme toggle 邏輯：初始化主題狀態
{THEME_INIT}

        // 頁籤切換邏輯（必須）
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.addEventListener('click', function () {
                const tab = this.getAttribute('data-tab');
                // 隱藏所有內容區塊
                document.querySelectorAll('.tab-content').forEach(c => {
                    c.classList.remove('active');
                });
                // 移除所有按鈕的 active 狀態
                document.querySelectorAll('.tab-button').forEach(b => {
                    b.classList.remove('active');
                });
                // 顯示選中的內容塊
                document.querySelector(`.tab-content[data-tab="${tab}"]`).classList.add('active');
                // 標記選中的按鈕
                this.classList.add('active');
            });
        });
    </script>
{EXTRA_JS}
</body>
</html>
```

#### HTML 結構要求

自動生成的 `{TABS_HTML}` 和 `{CONTENT_HTML}` 具有固定結構，模板中必須配合：

**頁籤按鈕的數據結構**：
```html
<!-- {TABS_HTML} 生成的結構 -->
<button class="tab-button" data-tab="document_name">
    Document Name
</button>
```

**內容區塊的數據結構**：
```html
<!-- {CONTENT_HTML} 生成的結構 -->
<div class="tab-content" data-tab="document_name">
    <!-- Markdown HTML 內容 -->
</div>
```

模板必須包含：
- `.tab-button` - 可點擊的頁籤按鈕，帶 `data-tab` 屬性
- `.tab-content` - 內容區塊，帶 `data-tab` 屬性，必須與按鈕的 `data-tab` 值相同
- `.active` 類 - CSS 控制頁籤活躍狀態的顯示/隱藏

#### 主題切換邏輯

`{THEME_INIT}` 自動生成主題初始化代碼。模板應包含：

1. **HTML `<html>` 元素** - 根據主題狀態設定 `data-theme` 屬性
   ```html
   <html data-theme="">              <!-- Dark mode -->
   <html data-theme="light">         <!-- Light mode -->
   ```

2. **主題按鈕** - 用於切換主題
   ```html
   <button id="theme-toggle">
       <span id="theme-icon">☀</span>
       <span id="theme-label">{I18N_THEME_LIGHT_LABEL}</span>
   </button>
   ```

3. **CSS 變數** - 定義兩種主題的顏色變數
   ```css
   :root {
       --bg-primary: #fff;
       --text-primary: #333;
   }
   [data-theme="dark"] {
       --bg-primary: #1e1e1e;
       --text-primary: #fff;
   }
   ```

### 步驟 4：建立 `template.config.json`

聲明外部 CDN 資源（CSS/JS）和元數據：

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
    "https://cdn.jsdelivr.net/npm/highlight.js/styles/github.css"
  ],
  "extra_js": [
    "https://cdn.jsdelivr.net/npm/highlight.js/highlight.min.js"
  ]
}
```

#### `_metadata` 欄位說明

| 欄位 | 必需 | 說明 |
|---|---|---|
| `name` | ✓ | 模板名稱（與目錄名一致） |
| `description` | ✓ | 模板簡述 |
| `version` | ✓ | 模板版本號（`MAJOR.MINOR.PATCH`） |
| `schema_version` | ✓ | 支持的主程式 API 版本（`v1`, `v2` 等） |
| `author` | | 作者名稱或組織 |

**版本字段說明**：

1. **`version`** - 模板自身版本（語義版本）
   - 格式：`MAJOR.MINOR.PATCH`（例：`1.0.0`, `1.1.0`, `2.0.0`）
   - 用途：追蹤模板的功能更新和修復
   - 範例：
     ```
     1.0.0 → 初始版本
     1.1.0 → 新增深色主題支援
     1.1.1 → 修正行距問題
     2.0.0 → 改用 Grid 布局（需要新主程式）
     ```

2. **`schema_version`** - 支持的主程式 API 版本
   - 格式：`v1`, `v2`, `v3` 等
   - 用途：標記此模板與主程式的兼容性
   - 範例：
     ```
     v1 → 與主程式 v1.x 兼容（目前版本）
     v2 → 與主程式 v2.x 兼容（未來版本，新 API）
     v1,v2 → 支持 v1 和 v2（多版本）
     ```

**語義版本規則**（[語義版本](https://semver.org/lang/zh-TW/)）：
- **MAJOR**：不相容的 API 改動（如：移除 i18n 佔位符）
- **MINOR**：向後相容的功能新增（如：新增 CSS 變數）
- **PATCH**：向後相容的修正（如：元素樣式調整）

這些 URL 會自動轉換成 `<link>` 和 `<script>` 標籤，注入到 `{EXTRA_CSS}` 和 `{EXTRA_JS}` 位置。

---

## 高級用法

### 命令行參數

```bash
# 指定語系
python main.py --locale zh-TW

# 指定模板
python main.py --template my_template

# 指定輸出檔案
python main.py --output my_docs.html

# 指定 Markdown 源目錄
python main.py --source /path/to/markdown

# 組合使用
python main.py --template my_template --locale en --output docs.html
```

### 動態日期在頁腳

在 `locales/*.json` 的 `template.footer_label` 中使用 `{BUILD_DATE}` 佔位符：

```json
{
  "template": {
    "footer_label": "Built on {BUILD_DATE}"
  }
}
```

打包器會自動替換為構建日期（格式：`YYYY.MM.DD`）。

若要固定日期，在 `.env` 設定：

```ini
BUILD_DATE=2024.03.05
```

---

## 模板開發檢查清單

使用此清單確保新模板完整且正常工作：

### 必要條件
- [ ] 目錄名稱只包含小寫字母、數字、底線（例：`my_template`, `doc-theme`）
- [ ] 包含 `style.css` 檔案
- [ ] 包含 `template.html` 檔案
- [ ] 包含 `template.config.json` 檔案

### HTML 結構
- [ ] `<html lang="{LANG}">` - 語言屬性
- [ ] `<title>{TITLE}</title>` - 頁面標題
- [ ] `<style>{CSS_CONTENT}</style>` - 樣式內容
- [ ] `{TABS_HTML}` 區域包含可點擊元素（帶 `class="tab-button"` 和 `data-tab` 屬性）
- [ ] `{CONTENT_HTML}` 區域用於顯示內容（帶 `class="tab-content"` 和 `data-tab` 屬性）
- [ ] `{EXTRA_CSS}` 位置（通常在 `</head>` 前）
- [ ] `{EXTRA_JS}` 位置（通常在 `</body>` 前）

### JavaScript
- [ ] 實現頁籤切換邏輯（點擊 `.tab-button` 時切換 `.tab-content` 的顯示）
- [ ] 使用 `{THEME_INIT}` 初始化主題
- [ ] 提供主題切換功能（可選但推薦）
- [ ] 沒有硬編碼的文字，所有文字使用 `{I18N_*}` 佔位符

### 樣式
- [ ] 使用 CSS 變數便於主題切換（`:root` 和 `[data-theme="dark"]`）
- [ ] `[data-theme="dark"]` 選擇器定義深色主題顏色
- [ ] `.active` 類用於高亮活躍頁籤
- [ ] 響應式設計（支援手機、平板、桌面）
- [ ] 沒有硬編碼顏色，使用 `var(--color-name)` 引入

### 多語言支援
- [ ] 检查 `locales/en.json` 和 `locales/zh-TW.json` 中所有必需的 i18n 鍵
- [ ] 模板中只使用 `{I18N_KEY}` 佔位符（不硬編碼文字）

### 測試步驟

1. **複製模板為測試**
   ```bash
   cp -r my_template test_template
   ```

2. **生成測試 HTML**
   ```bash
   python main.py --template my_template --locale zh-TW --output test.html
   ```

3. **在瀏覽器檢查**
   - [ ] 頁籤點擊能切換內容
   - [ ] 樣式正確加載
   - [ ] i18n 字串已替換（沒有 `{I18N_*}` 佔位符顯示）
   - [ ] 主題切換工作正常
   - [ ] 響應式設計：縮小瀏覽器窗口測試

4. **深色主題測試**
   ```bash
   python main.py --template my_template --locale zh-TW --output test_dark.html
   ```
   （在 `locales/zh-TW.json` 臨時改 `THEME_MODE` 後重新生成）

---

## 最佳實踐

### 開發方法

1. **從現有模板開始**
   - 複製 `normal` 或 `minimal` 模板作為起點，比從零開始更快
   ```bash
   cp -r templates/minimal templates/my_template
   ```

2. **漸進式修改**
   - 先修改 `style.css` 顏色和排版
   - 再修改 `template.html` 的 HTML 結構
   - 最後調整 `template.config.json` 的資源

3. **測試驅動**
   - 修改後立即用 `python main.py --template my_template` 測試
   - 在瀏覽器的開發者工具（F12）檢查錯誤

### 版本控制

1. **提交的檔案**
   ```bash
   ✓ templates/my_template/style.css
   ✓ templates/my_template/template.html
   ✓ templates/my_template/template.config.json
   ✓ .env.example
   ✓ locales/*.json
   ✓ main.py
   ```

2. **不提交的檔案/目錄**
   ```bash
   ✗ .env (本地配置)
   ✗ *.html (輸出檔案)
   ✗ venv/ (虛擬環境)
   ✗ __pycache__/ (編譯快取)
   ```

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

