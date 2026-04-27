---
id: agentic-code-patterns
trigger: "when creating code examples for chapters"
confidence: 0.85
domain: python-development
source: local-repo-analysis
---

# LangChain Code Example Pattern

## Action
When creating chapter code examples:
1. Use LangChain framework (version 0.3.0)
2. Create `llm_config.py` in each chapter directory with standard configuration
3. Name files sequentially: `01-*.py`, `02-*.py`, `03-*.py`
4. Use English filenames even for Chinese content
5. Include descriptive README.md for each chapter
6. Generate `Chapter_X_*_SUMMARY.md` with code blocks and mermaid diagrams

## Evidence
- Centralized `coding/requirements.txt` with LangChain dependencies
- Consistent `llm_config.py` pattern across all chapter directories
- Sequential file naming observed: `01-langchain-routing-example.py`, `02-rule-based-routing.py`
- Multiple "Chapter_X_*_SUMMARY.md" files found in the codebase
- Recent commits show "章节 实战项目 生成规则添加" (chapter practical project generation rules)

## When to Apply
When you need to:
- Add new chapter code examples
- Create practical demonstration projects
- Structure code files for educational purposes
- Generate code summaries and documentation