---
description: Format code with Prettier
argument-hint: none
allowed-tools: Bash(*)
---

Format all source code using Prettier for consistent code style across the project.

Execute: `npm run format`

What This Does:
- Formats all files in `src/` directory
- Applies Prettier rules consistently
- Modifies files in place
- Ensures uniform code style

Prettier Handles:
- **Indentation**: Consistent spacing (2 spaces)
- **Line Length**: Wraps long lines (100 characters)
- **Quotes**: Standardizes to single quotes
- **Semicolons**: Adds/removes based on config
- **Trailing Commas**: Adds where valid (ES5)
- **Bracket Spacing**: Consistent object spacing
- **Arrow Functions**: Parentheses around single params

File Types Formatted:
- JavaScript (`.js`, `.jsx`)
- TypeScript (`.ts`, `.tsx`)
- JSON (`.json`)
- CSS (`.css`)
- HTML (`.html`)
- Markdown (`.md`)

Prettier vs ESLint:
- **Prettier**: Code formatting (style)
- **ESLint**: Code quality (bugs, best practices)
- **Together**: Comprehensive code quality

Workflow:
```bash
# 1. Format code
/format

# 2. Lint for quality issues
/lint

# 3. Fix auto-fixable lint issues
/lint-fix

# 4. Fix remaining issues manually
```

Best Practices:
- Format before committing
- Enable format-on-save in your editor
- Run as pre-commit hook (optional)
- Keep Prettier and ESLint configs compatible

Editor Integration:
- **VS Code**: Install Prettier extension, enable format-on-save
- **WebStorm**: Built-in Prettier support
- **Vim**: Use prettier-vim plugin

Configuration:
- Configured in `.prettierrc`
- Prettier ignores specified in `.prettierignore`
- Shared config ensures team consistency

Before/After Example:
```typescript
// Before
const  component  =  ( props )  =>  {
return     <div>{ props.name}</div>
}

// After
const component = (props) => {
  return <div>{props.name}</div>;
};
```

Checking Without Formatting:
- Use `npm run format:check` to verify formatting without modifying files
- Useful in CI/CD to enforce formatting
- Returns non-zero exit code if files need formatting

Notes:
- Formatting is opinionated but consistent
- Removes debates about code style
- Safe to run anytime - doesn't change logic
- Fast - formats entire codebase in seconds
- Idempotent - running multiple times has same result

Integration:
- Pre-commit hooks can run this automatically
- CI/CD can check formatting compliance
- Editor plugins format on save

Common issues:
- Conflicts with ESLint - Update configs to be compatible
- Different formatting in editor - Install Prettier extension
- Files not formatted - Check `.prettierignore` file
- Unexpected formatting - Review `.prettierrc` configuration
