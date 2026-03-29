# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Chinese translation project for "Agentic Design Patterns" - a technical book about AI Agent design patterns. The project maintains three versions of content:
- **Chinese translation** (`chapters/`) - Fully translated Chinese content
- **Original English** (`original/`) - Source English content
- **Bilingual** (`bilingual/`) - Side-by-side English and Chinese content

The site is deployed to GitHub Pages using Jekyll, with automated PDF/EPUB generation via GitHub Actions.

## Development Commands

### Local Development
```bash
# Install dependencies
bundle install

# Serve locally for development
bundle exec jekyll serve

# Build site
bundle exec jekyll build
```

### Manual PDF/EPUB Generation
The GitHub workflow automatically generates PDFs/EPUBs on push, but you can test locally with Pandoc:

```bash
# Install required dependencies (Ubuntu/Debian)
sudo apt-get install -y texlive-xetex texlive-fonts-recommended texlive-lang-chinese fonts-noto-cjk
wget https://github.com/jgm/pandoc/releases/download/3.2/pandoc-3.2-1-amd64.deb
sudo dpkg -i pandoc-3.2-1-amd64.deb

# The workflow concatenates markdown files first, then runs pandoc
# See .github/workflows/generate-pdf.yml for the full process
```

## Project Structure

### coding 目录
- coding 目录是用于对一章节(chapters) 目录下的文件的代码实践，
例如 章节 Chapter 1_ Prompt Chaining.md 的代码需要放入 coding/Chapter_1_Prompt_Chaining/ 目录下，且基于python langchain.  安装包 requires.txt.
- 每个章节可能有很多代码文件注意都放到章节目录下面 按照 章节内容 对于的 功能生成 {章节段落}-{功能}.py ,py文件名是英文。
- 代码目录每个章节需要生成一个README.md,说明每个文件为了讲解什么内容，以及相关的代码文件说明 
- 生成的每个文件需要带上章节序号，有序命名 (生成的python文件需要带上需要带上序号 从1开始 按照章节顺序生成序号放到python 文件名前面 生成)
- python 依赖和coding/requirements.txt 维护 都是基于langchain 实现
- 生成代码摘要: 基于生成的代码 + agentic设计模式内容(Chapter_X.md)，生成摘要文件，且摘要文件的名字为Chapter_x_xxx_SUMMARY.md，生成位置在 coding/Chapter_x_xxx_SUMMARY
 *** 摘要要求***
 - 1.摘要基于中文语言描述
 - 2.摘要需要映入代码块，并说明每个代码用到了什么范式
 - 3.总结范式的使用场景
 - 4.摘要生成
  - 1.标题: 以范式名为标题-不要带任何其他内容例如(路由模式-代码摘要)不允许，只能是(路由模式)
  - 2.摘要格式: 要求整体章节结构要清晰，分层次描述，分为 4级标题
  - 3.流程图: 通过流程图 绘制 当前agentic范式的流程，基于 “mermaid” 语法
  - 4.代码块: 摘要的agentic 范式中，需要带上完整的流程代码，便于理解范式如何使用，以及场景

### Content Directories
- `chapters/` - Translated Chinese markdown files
- `original/` - Original English markdown files
- `bilingual/` - Bilingual format (English paragraph followed by Chinese translation)
- `images/` - Image resources organized by chapter (`chapter-1/`, `chapter-2/`, etc.)

### Key Configuration Files
- `_config.yml` - Jekyll configuration for GitHub Pages
- `Gemfile` - Ruby dependencies (Jekyll, GitHub Pages plugins)
- `glossary.md` - Terminology mapping for consistent translations
- `translation-guide.md` - Translation guidelines and standards
- `progress.md` - Translation progress tracking
- `CONTRIBUTING.md` - Contribution guidelines for translators

### GitHub Workflow
- `.github/workflows/generate-pdf.yml` - Automated PDF/EPUB generation on push to main
  - Runs Pandoc with XeLaTeX for Chinese font support
  - Generates Chinese, English, and Bilingual versions
  - Creates GitHub releases with artifacts

## Translation Workflow

1. **Reference Original Content**: Always work from `original/` files as source of truth
2. **Maintain Structure**: Keep identical file names and structure across `chapters/`, `original/`, and `bilingual/`
3. **Update Images**: Ensure image references point to `../images/chapter-XX/`
4. **Check Terminology**: Use `glossary.md` for consistent technical term translations
5. **Progress Tracking**: Update `progress.md` when completing translation work

## Bilingual Content Format

The `bilingual/` directory contains side-by-side format where each English paragraph is followed by its Chinese translation. This format is used for:
- Learning purposes (comparing original and translation)
- Quality verification
- Bilingual PDF/EPUB generation

## Important Notes

- **Markdown Format**: Use UTF-8 encoding, maintain original heading structure
- **Code Preservation**: Keep all code examples, variable names, and technical terms in English
- **Image Paths**: Update to relative paths pointing to `../images/chapter-XX/`
- **Jekyll Theme**: Uses `jekyll-theme-cayman` for GitHub Pages deployment
- **Chinese Font Support**: PDF generation uses Noto Sans CJK SC via XeLaTeX

## Deployment

- **GitHub Pages**: https://adp.xindoo.xyz/
- **Automatic Builds**: Triggered on push to `main` branch when content changes
- **Generated Artifacts**: PDF and EPUB files available via GitHub releases
