---
description: Install npm dependencies
argument-hint: [package-name] [--save-dev]
allowed-tools: Bash(*)
---

Install project dependencies using npm.

Arguments:
- $ARGUMENTS: Optional package names and flags

Common usage patterns:
- `/install` - Install all dependencies from package.json
- `/install axios` - Add new dependency
- `/install -D vitest` - Add new dev dependency
- `/install axios zod react-router-dom` - Add multiple packages

Execute: `npm install $ARGUMENTS`

Without Arguments (Fresh Install):
- Reads `package.json`
- Installs all dependencies
- Installs all devDependencies
- Creates/updates `package-lock.json`
- Creates `node_modules/` directory

With Package Names:
- Installs specified packages
- Adds to `dependencies` in package.json
- Updates package-lock.json
- Use `-D` or `--save-dev` for dev dependencies

When to Run:
- **First time setup**: After cloning repository
- **After pulling**: When package.json changed
- **Adding packages**: When installing new libraries
- **Dependency updates**: After modifying package.json
- **Troubleshooting**: When node_modules seems corrupted

Dependencies vs DevDependencies:
- **dependencies**: Required at runtime (React, Zustand, Axios)
- **devDependencies**: Only for development (Vite, ESLint, Vitest)

Common Package Types:

**UI & Framework:**
- `react-router-dom` - Routing
- `@radix-ui/react-*` - Accessible UI components
- `clsx` - Conditional classNames

**Data & State:**
- `axios` - HTTP requests
- `@tanstack/react-query` - Data fetching
- `zustand` - State management
- `zod` - Schema validation

**Dev Tools:**
- `@types/node` - Node type definitions
- `@types/react` - React type definitions
- `eslint-plugin-*` - ESLint plugins

**Utilities:**
- `date-fns` - Date utilities
- `lodash` - Utility functions
- `uuid` - Generate unique IDs

Clean Install:
```bash
# Remove node_modules and lock file
rm -rf node_modules package-lock.json

# Fresh install
/install
```

Troubleshooting Install Issues:
1. Clear npm cache: `npm cache clean --force`
2. Delete node_modules: `rm -rf node_modules`
3. Delete package-lock.json: `rm package-lock.json`
4. Run `/install` again

Version Management:
- `^1.2.3` - Install 1.x.x (minor and patch updates)
- `~1.2.3` - Install 1.2.x (patch updates only)
- `1.2.3` - Exact version only
- `latest` - Always latest version (risky)

Checking for Updates:
- `npm outdated` - Show outdated packages
- `npm update` - Update packages within semver ranges
- `npm update package-name` - Update specific package

Security:
- Run `npm audit` to check vulnerabilities
- Run `npm audit fix` to auto-fix issues
- Keep dependencies updated regularly

Best Practices:
- Commit `package-lock.json` to version control
- Don't commit `node_modules/` (add to .gitignore)
- Review what packages you're installing
- Keep dependencies up to date
- Remove unused dependencies

Notes:
- Installation can take 1-5 minutes depending on packages
- `node_modules/` can be large (100MB+)
- Package lock ensures consistent installs across machines
- CI/CD should use `npm ci` for faster, reliable installs

Common issues:
- "Permission denied" - Don't use sudo, fix npm permissions
- "EACCES" - Node/npm permission issues
- "Cannot find module" - Run `/install` to install dependencies
- "Peer dependency conflict" - Check compatibility, may need --legacy-peer-deps
- Slow install - Clear cache or try different registry
