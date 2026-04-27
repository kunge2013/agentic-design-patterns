---
id: agentic-translation-workflow
trigger: "when translating content for this project"
confidence: 0.9
domain: content-translation
source: local-repo-analysis
---

# Translation Workflow Pattern

## Action
Always follow this translation workflow:
1. Reference `original/` directory as source of truth
2. Check `glossary.md` and `Index of Terms.md` for terminology
3. Translate to `chapters/` directory
4. Create side-by-side format in `bilingual/` (English → Chinese)
5. Update `progress.md` to track completion

## Evidence
- 200 commits analyzed from Oct 2025 - Apr 2026
- 80%+ commits follow bilingual directory structure maintenance
- Frequent commits for "统一术语翻译" (unify terminology translation)
- Multiple commits for "格式修正和内容完整性改进" (format fixes and content improvements)

## When to Apply
When you need to:
- Translate new chapter content
- Update existing translations
- Fix terminology inconsistencies
- Improve translation quality