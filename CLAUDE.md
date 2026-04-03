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
  - 5.所以的llm配置都和 coding/Chapter_1_Prompt_Chaining/llm_config.py 一样
- 5.实战演练
  - 1.基于章节文件 + 摘要 + 代码示例，你自己构思一个实用的实战项目，并体现使用场景。并应用应用章节知识 并生成代码到 (coding/{xx章节}/practical)，如果coding 下面的practical不存在，先创建
  - 2.项目要求
    - 1. 紧密结合章节内容,想象一个实用的业务场景，生成实战章节应用
    - 2. 项目模型配置和章节一样  coding/{xx章节}/llm_config.py,且复制到 practical 目录
    - 3. 生成项目要求有readme.md 说明如何使用范式，且需要有 "mermaid" 流程图，描述项目运行流程
    - 4. 项目框架,要求项目用flask框架，可以通过web 界面访问，且界面绘制项目的整体运作流程，如果涉及langgraph 可以给出到web界面
    - 5. 设计理念，要求每次跟其他 对象(agent, 大模型, 记忆, 工具调用, 或调用api,mcp,skills,等工具)调用都需要输出节点操作过程(入参，出参 内容)，
    便于排查问题，通过流程图形式展示过程信息，入参/出参用markdown 代码块输出，且要求，每个节点给一个tips 显示代码文件名+方法名(filename#methodName)
    - 6. 添加swagger 依赖 "lasgger" 支持swagger 接口访问,所有api接口都自动配置暴露出来，便于自测，接口 http://localhost:5000/api/docs
      - 1. Swagger API 文档配置说明 本项目使用 **Flasgger** 和 **装饰器注解** 的方式配置 Swagger API 文档。 接口文档位置 practical/docs/api_xxx.yml        # xx接口文档2. 装饰器注解配置使用 `@swag_from` 装饰器从外部 YAML 文件加载文档
      - 2. 接口文档 必须严格按照 ymal 格式，最好生成完成后自查下是否为标准yaml
      - 3. 严格按照标准的swagger格式生成文档 
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

## 虚拟环境

- ** source ~/.bashrc & conda activate agentic-design-patterns **