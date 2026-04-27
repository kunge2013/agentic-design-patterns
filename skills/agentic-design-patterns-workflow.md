---
name: agentic-design-patterns-workflow
description: Coding and workflow patterns for the Agentic Design Patterns translation project
version: 1.0.0
source: local-git-analysis
analyzed_commits: 200
---

# Agentic Design Patterns Project Patterns

## Project Overview

This is a Chinese translation project for "Agentic Design Patterns" - a technical book about AI Agent design patterns. The project maintains three content versions and practical coding examples using LangChain.

## Commit Conventions

The project uses **mixed commit conventions**:

### Chinese Descriptive Messages (Most Common)
- `章节 实战项目 生成规则添加` - Adding practical project generation rules
- `长期记忆短期记忆` - Long-term/short-term memory implementation
- `代码优化` - Code optimization
- `优化翻译` - Optimize translation
- `修复 xxx 问题` - Fix specific issues

### Conventional Commits (Emerging Pattern)
- `fix: 统一术语翻译` - Standardize terminology translation
- `fix code` - Fix code issues
- English conventions for technical fixes

### Merge Patterns
- `Merge pull request #XX from branch-name` - Standard GitHub merge format
- `Merge branch 'main' into feature-branch` - Feature development workflow

**Best Practice**: For technical code changes, use conventional commits. For content updates, use descriptive Chinese messages.

## Code Architecture

### Directory Structure
```
.
├── chapters/                    # Chinese translated content
├── original/                    # Original English content (source of truth)
├── bilingual/                   # Side-by-side English+Chinese format
├── coding/                      # Practical code implementations
│   ├── Chapter_1_Prompt_Chaining/
│   │   ├── llm_config.py        # LLM configuration (per chapter)
│   │   ├── 1-*.py              # Sequential example files
│   │   ├── 2-*.py
│   │   └── README.md
│   ├── requirements.txt          # Centralized dependencies
│   └── Chapter_X_*/             # Other chapters
├── images/chapter-XX/           # Image resources per chapter
└── docs/                        # Documentation
```

### Coding Patterns (Python/LangChain)

#### Standard LLM Configuration Pattern
```python
from llm_config import create_llm

# Initialize LLM with environment variables
llm = create_llm(
    temperature=0.7,
    model="gpt-3.5-turbo"
)
```

#### Code File Naming Convention
- **Sequential numbering**: `01-*.py`, `02-*.py`, `03-*.py`
- **Descriptive names**: `prompt-chaining-example.py`, `routing-system.py`
- **English filenames**: Even for Chinese content

#### Dependencies Management
- **Centralized**: Single `coding/requirements.txt`
- **Based on LangChain**: All examples use LangChain framework
- **Key packages**:
  - `langchain==0.3.0`
  - `langchain-openai==0.2.0`
  - `langchain-community==0.3.0`
  - `openai==1.50.0`

#### Configuration Pattern
Each chapter directory contains `llm_config.py` with:
```python
class LLMConfig:
    def __init__(self, api_key, api_url, model, temperature):
        # Configuration setup

def create_llm(**kwargs) -> ChatOpenAI:
    # Factory function for LLM creation
```

## Translation Workflow

### Content Synchronization Rule
**ALWAYS work from `original/` files as source of truth**

### Translation Process
1. Reference original English content from `original/` directory
2. Create/update Chinese translation in `chapters/`
3. Maintain side-by-side format in `bilingual/` (English paragraph → Chinese translation)
4. Keep identical file names and structure across all three directories

### Terminology Management
- **Primary reference**: `glossary.md` - Terminology mapping
- **Additional reference**: `chapters/Index of Terms.md`
- **Consistency rule**: Always check both files for term translations

### Common Translation Tasks
- Update chapter content: `优化 X 章翻译`
- Fix terminology issues: `统一术语翻译` / `修复术语不一致问题`
- Format corrections: `格式修正和内容完整性改进`
- Content improvements: `翻译内容更新：优化各章节翻译质量`

## Workflows

### Adding New Chapter Examples
1. Create `coding/Chapter_X_[Chapter_Name]/` directory
2. Add `llm_config.py` with standard configuration
3. Create sequential example files (`01-*.py`, `02-*.py`, etc.)
4. Write `README.md` explaining examples
5. Generate `Chapter_X_[Chapter_Name]_SUMMARY.md` summary
6. Test examples with LangChain framework

### Content Translation Workflow
1. Start from `original/Chapter_X_[Name].md`
2. Translate to `chapters/Chapter_X_[Name].md`
3. Create bilingual version in `bilingual/`
4. Update `progress.md` tracking
5. Verify terminology against `glossary.md`

### Documentation Updates
- **Progress tracking**: `progress.md` - Overall translation status
- **Translation guide**: `translation-guide.md` - Guidelines for translators
- **Contribution guide**: `CONTRIBUTING.md` - How to contribute

## Deployment and Automation

### GitHub Pages Deployment
- **Jekyll-based**: Uses `jekyll-theme-cayman` theme
- **Custom domain**: https://adp.xindoo.xyz/
- **Multi-language**: Supports Chinese, English, and Bilingual versions
- **Interactive features**: Dark mode, chat bot for Q&A

### Automated PDF/EPUB Generation
- **Trigger**: Push to `main` branch when content changes
- **Workflow**: `.github/workflows/generate-pdf.yml`
- **Technology**: Pandoc with XeLaTeX
- **Font support**: Noto Sans CJK SC for Chinese characters
- **Artifacts**: Available via GitHub Releases

### Jekyll Configuration
- **Layout system**: `_layouts/default.html` frequently modified (15+ commits)
- **Image paths**: Relative paths pointing to `../images/chapter-XX/`
- **Markdown format**: UTF-8 encoding, preserve heading structure

## File Co-Change Patterns

### Frequently Changed Together
- **Content sets**: Chapter files often updated in batches (e.g., "更新 14-18 章")
- **Translation sync**: `chapters/`, `original/`, `bilingual/` updated together
- **Deployment pairs**: `_layouts/default.html` + content updates
- **Documentation pairs**: `progress.md` + chapter translations

### High-Frequency Files
- `chapters/Chapter 3_ Parallelization.md` (17 changes)
- `chapters/Chapter 2_ Routing.md` (17 changes)
- `_layouts/default.html` (15 changes)
- `README.md` (14 changes)
- `progress.md` (13 changes)

## Testing and Quality Assurance

### Code Testing
- Test examples in chapter directories
- Verify LLM connectivity with `llm_config.py`
- Check environment variable configuration
- Use `python-dotenv` for `.env` file loading

### Content Verification
- Verify terminology consistency with `glossary.md`
- Check bilingual format (English → Chinese paragraph pairs)
- Test PDF/EPUB generation locally with Pandoc
- Verify image paths point to correct `images/chapter-XX/` directories

## Environment Configuration

### Required Environment Variables
```bash
OPENAI_API_KEY=your-api-key              # Required
OPENAI_API_BASE=https://api.openai.com/v1 # Optional
OPENAI_MODEL=gpt-3.5-turbo               # Optional
OPENAI_TEMPERATURE=0.7                    # Optional
```

### Development Environment
- **Python**: For coding examples
- **Ruby/Bundler**: For Jekyll local development
- **Pandoc/XeLaTeX**: For local PDF testing
- **Virtual environment**: `conda activate agentic-design-patterns`

## Common Patterns Summary

### When Adding Code Examples
- Use LangChain framework consistently
- Follow sequential file naming: `01-*.py`, `02-*.py`
- Include `llm_config.py` in each chapter directory
- Add descriptive `README.md`
- Generate `Chapter_X_*_SUMMARY.md` with code blocks and mermaid diagrams

### When Translating Content
- Reference `original/` directory as source of truth
- Check `glossary.md` and `Index of Terms.md` for terminology
- Update `bilingual/` with side-by-side format
- Track progress in `progress.md`

### When Committing Changes
- Use descriptive Chinese messages for content updates
- Use conventional commits for technical changes
- Keep commits focused and atomic
- Update progress tracking files

## Key Insights from Repository Analysis

- **200 commits analyzed** spanning October 2025 - April 2026
- **Active development**: Recent commits focus on practical projects and code optimization
- **Collaborative workflow**: Frequent merge pull requests from feature branches
- **Quality focus**: Regular optimization and terminology consistency commits
- **Multi-format output**: Strong emphasis on PDF/EPUB generation and GitHub Pages deployment