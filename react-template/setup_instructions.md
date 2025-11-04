# Setup Instructions

This guide will help you set up your React + Vite + TypeScript project from this template.

## Prerequisites

Before starting, ensure you have:

- **Node.js 18 or higher** - [Download](https://nodejs.org/)
- **npm** (comes with Node.js) or **yarn/pnpm**
- **VS Code** (recommended) - [Download](https://code.visualstudio.com/)
- **Claude Code extension** for VS Code - [Install](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-code)
- **Git** (optional but recommended) - [Download](https://git-scm.com/)

## Step 1: Copy Template

### Option A: Download
1. Download this `react-template` directory
2. Copy it to your desired location
3. Rename it to your project name

### Option B: Clone from Repository
```bash
git clone <repository-url> my-project
cd my-project
```

## Step 2: Install Dependencies

Open a terminal in your project directory and run:

```bash
npm install
```

This will:
- Install all required dependencies
- Set up node_modules directory
- Create package-lock.json for dependency locking

**Expected time**: 2-5 minutes depending on internet speed

**Troubleshooting**:
- If installation fails, try: `npm cache clean --force` then retry
- For permission errors, don't use sudo - fix npm permissions instead
- If using Windows, ensure you're using a bash-compatible terminal

## Step 3: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:
   ```env
   # API Configuration
   VITE_API_URL=http://localhost:3000/api

   # App Configuration
   VITE_APP_NAME=My React App
   ```

3. **Important Notes**:
   - Only variables prefixed with `VITE_` are accessible in your React code
   - Never put secrets (API keys, tokens) in `VITE_` variables
   - The `.env` file is gitignored automatically
   - Create `.env.production` for production-specific variables

## Step 4: Verify Setup

Run the development server to ensure everything works:

```bash
npm run dev
```

Expected output:
```
VITE v6.x.x  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

Open http://localhost:5173/ in your browser. You should see the Vite + React welcome page.

## Step 5: Open in VS Code

1. Open the project in VS Code:
   ```bash
   code .
   ```

2. **Recommended Extensions** (VS Code will prompt you):
   - Claude Code (Anthropic.claude-code)
   - ESLint (dbaeumer.vscode-eslint)
   - Prettier (esbenp.prettier-vscode)
   - TypeScript Vue Plugin (Vue.vscode-typescript-vue-plugin)

3. **Configure VS Code Settings**:
   Create `.vscode/settings.json`:
   ```json
   {
     "editor.defaultFormatter": "esbenp.prettier-vscode",
     "editor.formatOnSave": true,
     "editor.codeActionsOnSave": {
       "source.fixAll.eslint": true
     },
     "typescript.tsdk": "node_modules/typescript/lib"
   }
   ```

## Step 6: Launch Claude Code

1. Click the Claude Code icon in VS Code sidebar
2. Or use shortcut: `Ctrl+Shift+P` → "Claude Code: Open"
3. Claude Code will load the project context from `CLAUDE.md`

**Available Slash Commands**:
- `/dev` - Start development server
- `/build` - Build for production
- `/test` - Run tests
- `/lint` - Check code quality
- `/create-component ComponentName` - Create new component

**Try it**: Type `/dev` in Claude Code to start the development server!

## Step 7: Create Your First Component

Use Claude Code to create a component:

```
/create-component Button --type common
```

This creates:
- `src/components/common/Button.tsx`
- `src/components/common/Button.test.tsx`

Or manually create your first component:

```typescript
// src/components/HelloWorld.tsx
interface HelloWorldProps {
  name: string;
}

export function HelloWorld({ name }: HelloWorldProps) {
  return (
    <div>
      <h1>Hello, {name}!</h1>
    </div>
  );
}
```

## Step 8: Run Tests

Verify testing is set up correctly:

```bash
npm test
```

You should see:
```
✓ tests/setup.ts (0) xxms
```

Create a test file to ensure testing works:

```typescript
// src/App.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByRole('heading')).toBeInTheDocument();
  });
});
```

## Step 9: Configure Git (Optional)

Initialize Git repository:

```bash
git init
git add .
git commit -m "Initial commit: React + Vite + TypeScript template"
```

Create a remote repository (GitHub, GitLab, etc.) and push:

```bash
git remote add origin <your-repo-url>
git push -u origin main
```

## Step 10: Customize for Your Project

1. **Update package.json**:
   ```json
   {
     "name": "your-project-name",
     "version": "1.0.0",
     "description": "Your project description"
   }
   ```

2. **Update index.html**:
   ```html
   <title>Your Project Name</title>
   ```

3. **Update CLAUDE.md** (optional):
   - Add project-specific context
   - Document your project structure
   - Add custom conventions

4. **Start building your app!**

## Next Steps

### Set Up API Integration

1. Create API client:
   ```typescript
   // src/services/api/client.ts
   import axios from 'axios';

   export const api = axios.create({
     baseURL: import.meta.env.VITE_API_URL,
   });
   ```

2. Create query hooks:
   ```typescript
   // src/services/queries/useExample.ts
   import { useQuery } from '@tanstack/react-query';
   import { api } from '../api/client';

   export function useExample() {
     return useQuery({
       queryKey: ['example'],
       queryFn: async () => {
         const { data } = await api.get('/example');
         return data;
       },
     });
   }
   ```

### Add State Management

Create a Zustand store:

```typescript
// src/store/authStore.ts
import { create } from 'zustand';

interface AuthState {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
```

### Add Routing (Optional)

Install React Router:

```bash
npm install react-router-dom
```

Set up routes:

```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { About } from './pages/About';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## Troubleshooting

### Development Server Won't Start

**Check Node version**:
```bash
node --version  # Should be 18+
```

**Clear cache and reinstall**:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Type Errors

**Run type check**:
```bash
npm run type-check
```

**Common fixes**:
- Ensure all imports have correct paths
- Check `tsconfig.json` paths are correct
- Install missing `@types/*` packages

### Tests Failing

**Update test setup**:
Ensure `tests/setup.ts` exists with:
```typescript
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});
```

### ESLint or Prettier Not Working

**Install VS Code extensions**:
- ESLint extension
- Prettier extension

**Check settings.json** includes:
```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true
}
```

## Getting Help

- **Claude Code**: Ask Claude for help with any issues
- **Documentation**: Check CLAUDE.md for project context
- **Official Docs**:
  - [React](https://react.dev/)
  - [Vite](https://vite.dev/)
  - [TypeScript](https://www.typescriptlang.org/)

## Success Checklist

- [ ] Dependencies installed (`node_modules` exists)
- [ ] Environment variables configured (`.env` exists)
- [ ] Dev server starts successfully (`npm run dev`)
- [ ] Tests run successfully (`npm test`)
- [ ] Linting works (`npm run lint`)
- [ ] Type checking passes (`npm run type-check`)
- [ ] VS Code opened with project
- [ ] Claude Code extension loaded
- [ ] Git repository initialized (optional)

Once all items are checked, you're ready to start development!

---

**Need Help?** Ask Claude Code or check the documentation. Happy coding!
