# Changelog

All notable changes to MDOne project are documented here.

## [1.0.0] - 2024-03-05

### Added
- ✅ Complete environment variable configuration (`.env`)
- ✅ Multi-language internationalization (i18n) support
  - English (`en`)
  - Traditional Chinese (`zh-TW`)
  - Extensible architecture for more languages
- ✅ Flexible template system
  - Builtin templates: `normal`, `minimal`
  - Custom template creation support
  - Template versioning and schema management
- ✅ External resource management (CDN CSS/JS)
- ✅ Command-line interface
  - `--template` for template selection
  - `--locale` for language selection
  - `--output` for output filename
  - `--source` for markdown directory
- ✅ Dark/Light theme support
- ✅ HTML minification option
- ✅ Single self-contained HTML output
- ✅ Comprehensive documentation
  - Configuration guide
  - i18n guide
  - Template development guide
  - Advanced usage examples
  - Troubleshooting guide

### Features
- **Single-file Output** - Package multiple Markdown documents into one offline-friendly HTML file
- **Multi-language** - Built-in i18n with placeholder system
- **Customizable** - Full control over templates, styles, and layout
- **Environment Variables** - Easy configuration via `.env`
- **CDN Resources** - Seamlessly integrate external CSS/JS
- **CLI Arguments** - Override configuration from command line
- **Semantic HTML** - Modern, accessible HTML structure
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Mode** - Built-in theme switching support

### Documentation
- Comprehensive README with quick start
- Configuration guide with all `.env` options
- Multi-language setup instructions
- Template development guide with examples
- Advanced usage scenarios and CI/CD integration
- Troubleshooting guide with common issues and solutions
- Changelog documenting project evolution

## Technical Details

### Architecture
- **Python 3.7+** - Core implementation
- **Markdown** - Document processing
- **python-dotenv** - Environment configuration
- **Pure HTML/CSS/JS** - No external template engine required

### Supported Markdown Extensions
- `tables` - GFM tables
- `fenced_code` - Code block syntax highlighting
- `codehilite` - Code highlighting
- `toc` - Table of contents generation
- `attr_list` - Attribute assignment
- `md_in_html` - Markdown inside HTML
- `extra` - Extra extensions (strikethrough, footnotes, etc.)

### Browser Compatibility
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Modern mobile browsers

### File Format
- Input: Markdown files (`.md`)
- Output: Single HTML file (self-contained, offline-compatible)
- File size: Typically 100-500KB for 10+ documents

## Version Strategy

### Semantic Versioning
- **MAJOR**: Breaking changes to API or CLI
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes and improvements

### Release Schedule
- Regular updates as features are added
- Security patches as needed
- Stability improvements ongoing

## Known Limitations

1. **Directory flattening** - Subdirectory structure in markdown folder doesn't affect tab organization (all files become tabs)
2. **No search** - Built-in search not available (can be added via external libraries)
3. **Single page output** - All content in one HTML file
4. **No database** - Purely file-based, no dynamic content

## Future Roadmap

Potential future enhancements (not committed):
- [ ] Export to PDF
- [ ] Built-in search functionality
- [ ] Plugin system for custom processors
- [ ] Web UI for configuration
- [ ] Template marketplace
- [ ] Analytics integration
- [ ] Multiple output formats (ePub, Markdown)
- [ ] Live preview server

## Deprecations

None yet. Started with v1.0.0.

## Migration Guides

### From v0.x
If upgrading from earlier versions:
1. Create `.env` from `.env.example` with your settings
2. Update template directories if using custom templates
3. Run: `python main.py`

## Contributors

Project maintained and developed actively.

## Support

For issues, feature requests, or questions:
- Check [Troubleshooting Guide](TROUBLESHOOTING.md)
- Review [Configuration Guide](CONFIGURATION.md)
- See [i18n Guide](I18N.md) for language issues
- Check [Template Development](TEMPLATE_DEVELOPMENT.md) for customization

## License

MIT License - Free for personal and commercial use.

---

## Version History

### v1.0.0 (2024-03-05)
- Initial stable release
- Complete feature set for document packaging
- Comprehensive documentation
- Production-ready

---

## Reporting Issues

When reporting issues, include:
1. Python version: `python --version`
2. OS: Windows/macOS/Linux
3. Error message (full output)
4. Steps to reproduce
5. `.env` configuration (without sensitive data)
6. Markdown sample that triggers the issue

## Contributing

Contributions welcome! Areas to contribute:
- Bug reports and fixes
- New language translations
- Template designs
- Documentation improvements
- Feature ideas

---

Last updated: 2024-03-05
