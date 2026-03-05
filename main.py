#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDOne HTML Packager - Universal documentation packager
Converts Markdown files into self-contained HTML with template support, i18n, and CDN resource management.
"""

import os
import sys
import glob
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import markdown
import re

# ======================
# Configuration & Localization
# ======================

# Load environment variables from .env
# Load environment variables from .env (if exists)
env_loaded = load_dotenv()


def get_env(key, default=""):
    """Get environment variable with optional default"""
    return os.getenv(key, default)


def parse_bool(value):
    """Convert string to boolean"""
    return value.lower() in ("true", "1", "yes", "on")


def parse_list(value, delimiter=","):
    """Convert comma-separated string to list"""
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter)]


# Configuration from environment
CONFIG = {
    "markdown_source_dir": get_env("MARKDOWN_SOURCE_DIR", "./markdown"),
    "output_file": get_env("OUTPUT_FILE", "system_guide.html"),
    "templates_dir": get_env("TEMPLATES_DIR", "templates"),
    "default_template": get_env("DEFAULT_TEMPLATE", "normal"),
    "minify_html": parse_bool(get_env("MINIFY_HTML", "true")),
    "markdown_extensions": parse_list(
        get_env("MARKDOWN_EXTENSIONS", "tables,fenced_code,nl2br,sane_lists,attr_list")
    ),
    "site_title": get_env("SITE_TITLE", "Documentation"),
    "theme_mode": get_env("THEME_MODE", "light"),
    "locale": get_env("LOCALE", "en"),
    "locales_dir": get_env("LOCALES_DIR", "locales"),
    "template_config_file": get_env("TEMPLATE_CONFIG_FILE", "template.config.json"),
}

# Setup logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ======================
# i18n (Internationalization)
# ======================


class I18n:
    """Multi-language resource manager"""

    def __init__(self, locale="en", locales_dir="locales"):
        self.locale = locale
        self.locales_dir = locales_dir
        self.resources = {}
        self.load(locale)

    def load(self, locale):
        """Load locale resource file"""
        locale_file = Path(self.locales_dir) / f"{locale}.json"

        if not locale_file.exists():
            logger.warning(
                f"Locale file not found: {locale_file}. Falling back to 'en'."
            )
            locale_file = Path(self.locales_dir) / "en.json"

        if not locale_file.exists():
            logger.error(f"Default locale 'en' not found at {locale_file}")
            self.resources = {"cli": {}, "template": {}}
            return

        try:
            with open(locale_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.resources = data
                self.locale = locale
        except Exception as e:
            logger.error(f"Failed to load locale: {e}")
            self.resources = {"cli": {}, "template": {}}

    def get_cli(self, key, **kwargs):
        """Get CLI message string"""
        text = self.resources.get("cli", {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text

    def get_template(self, key, **kwargs):
        """Get template UI string"""
        text = self.resources.get("template", {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text

    def get_all_template(self):
        """Get all template strings as dict"""
        return self.resources.get("template", {})


# Initialize i18n
i18n = I18n(CONFIG["locale"], CONFIG["locales_dir"])

# ======================
# Core Functions
# ======================


def validate_config():
    """Validate required configuration"""
    errors = []

    if not CONFIG["markdown_source_dir"]:
        errors.append(
            i18n.get_cli("err_md_dir_missing", dir=CONFIG["markdown_source_dir"])
        )

    if not Path(CONFIG["markdown_source_dir"]).exists():
        errors.append(
            i18n.get_cli("err_md_dir_missing", dir=CONFIG["markdown_source_dir"])
        )

    if errors:
        for err in errors:
            logger.error(err)
        return False

    return True


def get_available_templates():
    """Get list of available templates"""
    templates = []
    templates_path = Path(CONFIG["templates_dir"])

    if templates_path.exists():
        for template_dir in templates_path.iterdir():
            if template_dir.is_dir():
                css_file = template_dir / "style.css"
                html_file = template_dir / "template.html"
                if css_file.exists() and html_file.exists():
                    templates.append(template_dir.name)

    return sorted(templates)


def load_template(template_name):
    """Load template files and configuration"""
    template_dir = Path(CONFIG["templates_dir"]) / template_name

    if not template_dir.exists():
        raise FileNotFoundError(
            i18n.get_cli("err_template_not_found", name=template_name)
        )

    # Load CSS
    css_file = template_dir / "style.css"
    if not css_file.exists():
        raise FileNotFoundError(f"Missing style.css in template '{template_name}'")

    with open(css_file, "r", encoding="utf-8") as f:
        css_content = f.read()

    # Load HTML template
    html_file = template_dir / "template.html"
    if not html_file.exists():
        raise FileNotFoundError(f"Missing template.html in template '{template_name}'")

    with open(html_file, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Load template config (if exists)
    config_file = template_dir / CONFIG["template_config_file"]
    extra_css_urls = []
    extra_js_urls = []
    template_version = "1.0.0"  # Default version
    schema_version = "v1"  # Default schema version
    template_metadata = {}
    toc_config = {"enabled": False, "levels": [2, 3]}  # Default TOC config

    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                template_config = json.load(f)
                extra_css_urls = template_config.get("extra_css", [])
                extra_js_urls = template_config.get("extra_js", [])
                template_metadata = template_config.get("_metadata", {})
                template_version = template_metadata.get("version", "1.0.0")
                schema_version = template_metadata.get("schema_version", "v1")
                toc_config = template_config.get("toc", toc_config)
        except Exception as e:
            logger.warning(f"Failed to load template config: {e}")

    return {
        "css": css_content,
        "template": html_template,
        "extra_css": extra_css_urls,
        "extra_js": extra_js_urls,
        "version": template_version,
        "schema_version": schema_version,
        "metadata": template_metadata,
        "toc_config": toc_config,
    }


def get_markdown_files():
    """Get Markdown files, sorted by name"""
    source_dir = CONFIG["markdown_source_dir"]
    pattern = os.path.join(source_dir, "*.md")
    md_files = sorted(glob.glob(pattern))
    return [(os.path.basename(f), f) for f in md_files]


def read_markdown(filepath):
    """Read Markdown file content"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(i18n.get_cli("err_read_failed", path=filepath, error=str(e)))
        return ""


def slugify(text):
    """Convert heading text to URL-friendly ID"""
    # Convert to lowercase
    slug = text.lower()
    # Remove HTML tags if any
    slug = re.sub(r"<[^>]+>", "", slug)
    # Replace spaces and underscores with hyphens
    slug = re.sub(r"[\s_]+", "-", slug)
    # Remove special characters except hyphens
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r"-+", "-", slug)
    # Strip hyphens from start and end
    slug = slug.strip("-")
    return slug or "heading"


def add_heading_ids(html):
    """Add id attributes to heading elements if they don't exist"""
    seen_ids = {}

    def add_id_to_heading(match):
        tag = match.group(1)  # h1, h2, h3, etc.
        text = match.group(2)  # heading text content

        # Check if id already exists in attributes
        if "id=" in match.group(0):
            return match.group(0)

        # Generate ID from heading text
        base_id = slugify(text)

        # Handle duplicate IDs
        if base_id in seen_ids:
            seen_ids[base_id] += 1
            final_id = f"{base_id}-{seen_ids[base_id]}"
        else:
            seen_ids[base_id] = 1
            final_id = base_id

        return f'<{tag} id="{final_id}">{text}</{tag}>'

    # Match heading tags: <h1>text</h1>, <h2>text</h2>, etc.
    html = re.sub(r"<(h[1-6])>([^<]+)</\1>", add_id_to_heading, html)

    return html


def markdown_to_html(markdown_text):
    """Convert Markdown to HTML"""
    extensions = CONFIG["markdown_extensions"]

    md = markdown.Markdown(extensions=extensions)
    html = md.convert(markdown_text)

    # Add heading IDs for TOC support
    html = add_heading_ids(html)

    # Convert fenced_code language class to data-lang attribute
    html = re.sub(
        r'<pre><code class="language-(\w+)">',
        lambda m: f'<pre data-lang="{m.group(1)}"><code>',
        html,
    )

    # Escape { and } inside <code> blocks so they are never mistaken for
    # template placeholders during str.replace() substitution in generate_html().
    def escape_braces_in_code(match):
        inner = match.group(1)
        inner = inner.replace("{", "&#123;").replace("}", "&#125;")
        return f"<code>{inner}</code>"

    html = re.sub(r"<code>(.*?)</code>", escape_braces_in_code, html, flags=re.DOTALL)

    # Escape <script> and <link> tag text inside <td> and <code> blocks.
    # Cloudflare and other CDN proxies detect literal <script> strings in HTML
    # and inject real executable script tags in their place, breaking JS parsing.
    # We replace them with HTML entities so they render as plain text safely.
    def escape_tags_in_cell(match):
        inner = match.group(1)
        inner = re.sub(r"<(/?script)", r"&lt;\1", inner, flags=re.IGNORECASE)
        inner = re.sub(r"<(/?link)", r"&lt;\1", inner, flags=re.IGNORECASE)
        return f"<td>{inner}</td>"

    html = re.sub(r"<td>(.*?)</td>", escape_tags_in_cell, html, flags=re.DOTALL)

    return html


def minify_html(html_content):
    """Minify HTML while preserving script/style content"""
    # Protect script tags
    scripts = []

    def save_script(match):
        scripts.append(match.group(0))
        return f"__SCRIPT_PLACEHOLDER_{len(scripts)-1}__"

    html_content = re.sub(
        r"<script[^>]*>.*?</script>", save_script, html_content, flags=re.DOTALL
    )

    # Protect style tags
    styles = []

    def save_style(match):
        styles.append(match.group(0))
        return f"__STYLE_PLACEHOLDER_{len(styles)-1}__"

    html_content = re.sub(
        r"<style[^>]*>.*?</style>", save_style, html_content, flags=re.DOTALL
    )

    # Remove HTML comments
    html_content = re.sub(r"<!--.*?-->", "", html_content, flags=re.DOTALL)

    # Remove whitespace between tags
    html_content = re.sub(r">\s+<", "><", html_content)

    # Restore script/style tags
    for i, script in enumerate(scripts):
        html_content = html_content.replace(f"__SCRIPT_PLACEHOLDER_{i}__", script)
    for i, style in enumerate(styles):
        html_content = html_content.replace(f"__STYLE_PLACEHOLDER_{i}__", style)

    return html_content


def generate_extra_css_tags(extra_css_urls):
    """Generate <link> tags for extra CSS"""
    if not extra_css_urls:
        return ""

    tags = []
    for url in extra_css_urls:
        tags.append(f'    <link rel="stylesheet" href="{url}">')

    return "\n".join(tags)


def generate_extra_js_tags(extra_js_urls):
    """Generate <script> tags for extra JS"""
    if not extra_js_urls:
        return ""

    tags = []
    for url in extra_js_urls:
        tags.append(f'    <script src="{url}"></script>')

    return "\n".join(tags)


def generate_data_script(documents_html, template_data):
    """Generate MDOne_DATA JSON script for client-side rendering"""
    build_date = get_env("BUILD_DATE", "")
    if not build_date:
        build_date = datetime.now().strftime("%Y.%m.%d")

    # Build docs array
    docs = []
    for tab_name, html_content in documents_html.items():
        short_name = tab_name[:20] + "…" if len(tab_name) > 20 else tab_name
        docs.append(
            {
                "id": tab_name,
                "title": short_name,
                "name": tab_name,
                "html": html_content,
            }
        )

    # Get i18n template strings
    template_i18n = i18n.get_all_template()
    # Process footer_label with BUILD_DATE substitution
    footer_label = template_i18n.get("footer_label", "")
    if "{BUILD_DATE}" in footer_label:
        footer_label = footer_label.format(BUILD_DATE=build_date)
    template_i18n["footer_label"] = footer_label
    # Remove internal comment keys
    template_i18n = {k: v for k, v in template_i18n.items() if not k.startswith("_")}

    # Build config object
    config = {
        "site_title": CONFIG["site_title"],
        "theme_mode": CONFIG["theme_mode"],
        "build_date": build_date,
        "toc": template_data.get("toc_config", {"enabled": False, "levels": [2, 3]}),
    }

    # Assemble data structure
    data = {"docs": docs, "config": config, "i18n": template_i18n}

    # JSON serialize with ensure_ascii=False for proper UTF-8 support
    data_json = json.dumps(data, ensure_ascii=False)
    return f"<script>window.MDOne_DATA = {data_json};</script>"


def generate_html(md_files, template_data):
    """Generate complete HTML file"""

    documents_html = {}
    for file_name, file_path in md_files:
        content = read_markdown(file_path)
        if content:
            tab_name = os.path.splitext(file_name)[0]
            html_content = markdown_to_html(content)
            documents_html[tab_name] = html_content

    if not documents_html:
        logger.error(i18n.get_cli("err_no_content"))
        return None

    # Generate data script (replaces all SSR HTML generation)
    data_script = generate_data_script(documents_html, template_data)

    # Start with template HTML
    html_output = template_data["template"]

    # Replace only essential placeholders
    html_output = html_output.replace("{TITLE}", CONFIG["site_title"])
    html_output = html_output.replace(
        "{LANG}", i18n.get_all_template().get("html_lang", "en")
    )
    html_output = html_output.replace("{CSS_CONTENT}", template_data["css"])

    # Generate and inject extra CSS/JS
    extra_css_html = generate_extra_css_tags(template_data.get("extra_css", []))
    extra_js_html = generate_extra_js_tags(template_data.get("extra_js", []))

    html_output = html_output.replace("{EXTRA_CSS}", extra_css_html)
    html_output = html_output.replace("{EXTRA_JS}", extra_js_html)

    # Inject data script before closing body tag
    html_output = html_output.replace("{MDONE_DATA_SCRIPT}", data_script)

    # Remove any remaining unfilled placeholders (safety check)
    html_output = re.sub(r"\{[A-Z_]+\}", "", html_output)

    # Minify if configured
    if CONFIG["minify_html"]:
        html_output = minify_html(html_output)

    return html_output


def main():
    """Main entry point"""

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="MDOne HTML Packager - Convert Markdown to self-contained HTML",
        epilog="""
EXAMPLES:
  python main.py --template normal --locale zh-TW
  python main.py --template normal --locale en --output build/docs.html
  python main.py --source ./markdown --output ./dist/guide.html
  python main.py --template minimal --locale zh-TW --output output.html --source ./docs

ENVIRONMENT VARIABLES:
  MARKDOWN_SOURCE_DIR    - Markdown source directory (default: ./markdown)
  OUTPUT_FILE            - Output file path (default: system_guide.html)
  TEMPLATES_DIR          - Templates directory (default: templates)
  DEFAULT_TEMPLATE       - Default template name (default: normal)
  MINIFY_HTML            - Minify HTML output (default: true)
  SITE_TITLE             - Documentation site title (default: Documentation)
  THEME_MODE             - Theme mode: light or dark (default: light)
  LOCALE                 - Default locale code (default: en)
  LOCALES_DIR            - Locales directory (default: locales)
  TEMPLATE_CONFIG_FILE   - Template config filename (default: template.config.json)
  BUILD_DATE             - Build date for footer (auto-generated if not set)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--template",
        metavar="NAME",
        help="Template name to use (e.g., normal, minimal). Available templates are loaded from the templates/ directory",
    )
    parser.add_argument(
        "--locale",
        metavar="CODE",
        help="Locale/language code (e.g., en, zh-TW). Locale files are loaded from the locales/ directory",
    )
    parser.add_argument(
        "--output",
        metavar="PATH",
        help="Output HTML file path (e.g., ./output/guide.html or build/docs.html). Supports relative and absolute paths",
    )
    parser.add_argument(
        "--source",
        metavar="DIR",
        help="Markdown source directory (e.g., ./markdown or ./docs). All *.md files in this directory will be processed",
    )

    args = parser.parse_args()

    # Override config with CLI arguments (CLI has highest priority)
    if args.template:
        CONFIG["default_template"] = args.template
    if args.locale:
        CONFIG["locale"] = args.locale
        i18n.load(args.locale)
    if args.output:
        CONFIG["output_file"] = args.output
    if args.source:
        CONFIG["markdown_source_dir"] = args.source

    # Print header
    logger.info(i18n.get_cli("app_title"))
    logger.info("")

    # Show configuration source
    if env_loaded:
        logger.info("📋 配置來源：.env + 命令行參數（參數優先）")
    else:
        logger.info("📋 配置來源：默認值 + 命令行參數（參數優先）")
    logger.info("")

    # Print configuration
    logger.info(i18n.get_cli("config_header"))
    logger.info(i18n.get_cli("config_source", value=CONFIG["markdown_source_dir"]))
    logger.info(i18n.get_cli("config_output", value=CONFIG["output_file"]))
    logger.info(i18n.get_cli("config_template", value=CONFIG["default_template"]))
    minify_status = (
        i18n.get_cli("config_minify_on")
        if CONFIG["minify_html"]
        else i18n.get_cli("config_minify_off")
    )
    logger.info(i18n.get_cli("config_minify", value=minify_status))
    logger.info(
        i18n.get_cli(
            "config_extensions", value=", ".join(CONFIG["markdown_extensions"])
        )
    )
    logger.info(i18n.get_cli("config_locale", value=CONFIG["locale"]))
    logger.info("")

    # Validate configuration
    if not validate_config():
        return

    # Get available templates
    available_templates = get_available_templates()
    if not available_templates:
        logger.error(i18n.get_cli("err_no_templates"))
        logger.info(i18n.get_cli("err_no_templates_hint", dir=CONFIG["templates_dir"]))
        return

    # Check template exists
    template_name = CONFIG["default_template"]
    if template_name not in available_templates:
        logger.error(i18n.get_cli("err_template_not_found", name=template_name))
        logger.info(
            i18n.get_cli("err_available_templates", list=", ".join(available_templates))
        )
        return

    logger.info(i18n.get_cli("using_template", name=template_name))

    # Load template
    try:
        template_data = load_template(template_name)
        template_version = template_data.get("version", "1.0.0")
        schema_version = template_data.get("schema_version", "v1")
        logger.info(
            f"   Template version: {template_version} (schema: {schema_version})"
        )
    except Exception as e:
        logger.error(i18n.get_cli("err_load_template", error=str(e)))
        return

    # Get Markdown files
    md_files = get_markdown_files()
    if not md_files:
        logger.error(i18n.get_cli("err_no_md_files"))
        logger.info(
            i18n.get_cli("err_no_md_files_hint", dir=CONFIG["markdown_source_dir"])
        )
        return

    logger.info(i18n.get_cli("found_md_files", n=len(md_files)))
    for file_name, _ in md_files:
        logger.info(f"   - {file_name}")

    logger.info("")
    logger.info(i18n.get_cli("generating"))

    # Generate HTML
    html_content = generate_html(md_files, template_data)
    if not html_content:
        return

    # Write output
    try:
        output_file = CONFIG["output_file"]
        # Ensure parent directory exists
        output_path = Path(output_file)
        if output_path.parent != Path("."):
            output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        file_size = os.path.getsize(output_file) / 1024
        logger.info("")
        logger.info(i18n.get_cli("success"))
        logger.info(i18n.get_cli("output_file_label", value=output_file))
        logger.info(i18n.get_cli("output_size_label", value=f"{file_size:.1f}"))
        logger.info("")

        logger.info(i18n.get_cli("usage_header"))
        logger.info(i18n.get_cli("usage_open", file=output_file))
        logger.info(i18n.get_cli("usage_tabs"))
        logger.info(i18n.get_cli("usage_offline"))
        logger.info("")

        logger.info(i18n.get_cli("available_templates_header"))
        for tmpl in available_templates:
            marker = i18n.get_cli("template_marker") if tmpl == template_name else " "
            logger.info(
                f"   {marker} python main.py --template {tmpl} --locale {CONFIG['locale']}"
            )

    except Exception as e:
        logger.error(i18n.get_cli("err_write_failed", error=str(e)))


if __name__ == "__main__":
    main()
