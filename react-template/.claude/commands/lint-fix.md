---
description: Auto-fix ESLint issues
argument-hint: [FILE_PATTERN]
allowed-tools: Bash(*)
---

Automatically fix linting issues that can be resolved without manual intervention.

Arguments:
- $ARGUMENTS: Optional file patterns or paths to fix

Common usage patterns:
- `/lint-fix` - Fix all auto-fixable issues
- `/lint-fix src/components` - Fix issues in specific directory
- `/lint-fix src/App.tsx` - Fix issues in specific file

Execute: `npm run lint -- --fix $ARGUMENTS`

What Gets Auto-Fixed:
- **Formatting**: Indentation, spacing, quotes
- **Import Sorting**: Organize imports
- **Semicolons**: Add or remove based on config
- **Trailing Commas**: Add or remove
- **Unused Imports**: Remove automatically
- **Simple Fixes**: Various rule violations with clear fixes

What Doesn't Get Auto-Fixed:
- Complex logic issues
- Missing dependencies in hooks
- Type errors
- Accessibility issues
- Some React-specific problems

Process:
1. Scans all files for lint issues
2. Applies automatic fixes where possible
3. Modifies files in place
4. Reports remaining issues that need manual fixes

After Running:
- Review changes with `git diff`
- Verify code still works correctly
- Run tests to ensure nothing broke
- Address any remaining issues manually

Best Practices:
- Run before committing code
- Review auto-fixes to understand changes
- Commit auto-fixes separately from feature changes
- Run tests after auto-fixing

Workflow:
```bash
# 1. Fix auto-fixable issues
/lint-fix

# 2. Check for remaining issues
/lint

# 3. Fix remaining issues manually

# 4. Run tests to verify
/test

# 5. Commit changes
```

Safety:
- Auto-fixes are generally safe
- Formats code according to rules
- Doesn't change logic or behavior
- Still review changes before committing

Notes:
- Combines well with Prettier (formatting)
- Not all lint issues can be auto-fixed
- Some fixes may conflict - review carefully
- Use in combination with `/format` for best results

Common scenarios:
- "Too many lint errors" - Run this first to clear obvious issues
- "Before committing" - Clean up code automatically
- "After merge" - Fix formatting inconsistencies
- "New team member code" - Standardize code style

Common issues:
- Conflicts with Prettier - Ensure ESLint and Prettier configs are compatible
- Files changed unexpectedly - Review the ESLint rules and disable if needed
- Breaking changes - Rare, but always test after auto-fixing
