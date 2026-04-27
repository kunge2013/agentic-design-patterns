---
id: agentic-commit-conventions
trigger: "when writing commit messages"
confidence: 0.8
domain: git-workflow
source: local-repo-analysis
---

# Commit Message Conventions

## Action
Use different conventions based on change type:

### For Content/Translation Updates
Use descriptive Chinese messages:
- `章节 实战项目 生成规则添加` (chapter practical project generation rules)
- `优化翻译` (optimize translation)
- `统一术语翻译` (unify terminology translation)
- `修复 xxx 问题` (fix specific issues)

### For Technical/Code Changes
Use conventional commits when possible:
- `fix: 统一术语翻译` (fix: standardize terminology translation)
- `fix code` (fix code)
- `优化代码` (optimize code)

### Standard Patterns
- Merge commits: `Merge pull request #XX from branch-name`
- Content updates: `更新 X 章翻译` (update chapter X translation)
- Format fixes: `格式修正和内容完整性改进` (format fixes and content improvements)

## Evidence
- Analysis of 200 commits from Oct 2025 - Apr 2026
- 70%+ commits use descriptive Chinese messages
- 30% use conventional commit format (especially for technical fixes)
- Consistent use of Merge pull request format for collaborative work
- Frequent pattern of "优化" (optimize) and "修复" (fix) prefixes

## When to Apply
When you need to:
- Commit translation work
- Commit code changes
- Merge feature branches
- Fix terminology or formatting issues