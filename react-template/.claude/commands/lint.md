---
description: Run ESLint on source files
argument-hint: [FILE_PATTERN]
allowed-tools: Bash(*)
---

Run ESLint to check code quality, find bugs, and enforce coding standards.

Arguments:
- $ARGUMENTS: Optional file patterns or paths to lint

Common usage patterns:
- `/lint` - Lint all source files
- `/lint src/components` - Lint specific directory
- `/lint src/App.tsx` - Lint specific file
- `/lint --fix` - Auto-fix issues (use `/lint-fix` command instead)

Execute: `npm run lint $ARGUMENTS`

What ESLint Checks:
- **Code Quality**: Potential bugs and bad practices
- **Style**: Consistent code formatting
- **React Rules**: React-specific best practices
- **TypeScript**: TypeScript-specific linting
- **Hooks**: Correct hooks usage (dependencies, rules)
- **Accessibility**: Basic a11y issues

Common Issues Found:
- Unused variables and imports
- Missing dependencies in useEffect
- Incorrect hook usage
- TypeScript type issues
- Formatting inconsistencies
- Potential bugs (== vs ===, etc.)

Lint Rules:
- Based on ESLint recommended rules
- React plugin for React-specific rules
- TypeScript plugin for type-aware linting
- Hooks plugin for React hooks rules

Output Format:
- Lists files with issues
- Shows line numbers and column
- Explains each issue
- Suggests fixes where possible
- Summary of total errors and warnings

Error Levels:
- **Error** (red): Must be fixed, breaks build
- **Warning** (yellow): Should be fixed, but not critical
- **Info**: Suggestions for improvement

Best Practices:
- Fix errors before committing
- Address warnings when possible
- Run lint before pushing code
- Configure IDE to show lint errors in real-time

Integration:
- Runs automatically in CI/CD
- Can be run as pre-commit hook
- IDE extensions available (VS Code ESLint)

Disabling Rules:
```typescript
// Disable for next line
// eslint-disable-next-line rule-name
const x = dangerousOperation();

// Disable for entire file (use sparingly!)
/* eslint-disable rule-name */
```

Notes:
- Linting doesn't modify files (use `/lint-fix` for that)
- Zero errors is the goal
- Warnings should be addressed but aren't blocking
- Configure rules in `.eslintrc.cjs`

Common issues:
- "Parsing error" - Check TypeScript syntax
- "Rule not found" - Check ESLint plugins are installed
- Too many errors - Run `/lint-fix` first, then address remaining issues
- False positives - Disable specific rules if needed (document why)
