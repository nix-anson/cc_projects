# React + Vite + TypeScript Template

A comprehensive, production-ready React template with Vite, TypeScript, TanStack Query, Zustand, and Claude Code integration.

## Features

- ⚡️ **Vite** - Lightning-fast dev server and optimized builds
- ⚛️ **React 18** - Latest React with concurrent features
- 🔷 **TypeScript** - Full type safety and excellent DX
- 🔄 **TanStack Query** - Powerful data fetching and caching
- 🐻 **Zustand** - Lightweight, flexible state management
- 🧪 **Vitest** - Fast unit testing with React Testing Library
- 🎨 **ESLint + Prettier** - Code quality and consistent formatting
- 🤖 **Claude Code Integration** - AI-powered development assistance

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- VS Code (recommended)
- Claude Code extension

### Installation

1. **Use this template or download it**
   ```bash
   # Option 1: Download/copy this directory

   # Option 2: Clone from repository
   git clone <repo-url> my-react-app
   cd my-react-app
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open in VS Code and launch Claude Code**
   ```bash
   code .
   # Then launch Claude Code from VS Code
   ```

## Project Structure

```
project-name/
├── .claude/                   # Claude Code configuration
│   ├── commands/             # Slash commands (/dev, /build, etc.)
│   ├── agents/               # Specialized AI agents
│   ├── skills/               # Automated patterns
│   └── settings.json         # Claude Code settings
├── src/
│   ├── assets/              # Images, fonts, styles
│   ├── components/          # React components
│   │   ├── common/          # Reusable UI components
│   │   ├── layout/          # Layout components
│   │   └── features/        # Feature-specific components
│   ├── hooks/               # Custom React hooks
│   ├── pages/               # Page components
│   ├── services/            # API services
│   │   ├── api/             # API clients
│   │   ├── queries/         # React Query hooks
│   │   └── mutations/       # React Query mutations
│   ├── store/               # Zustand stores
│   ├── types/               # TypeScript types
│   ├── utils/               # Utility functions
│   ├── App.tsx              # Root component
│   └── main.tsx             # Entry point
├── tests/                   # Test configuration
│   └── setup.ts             # Test setup
├── .env.example             # Environment variables template
├── .eslintrc.cjs            # ESLint configuration
├── .prettierrc              # Prettier configuration
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── vite.config.ts           # Vite configuration
├── vitest.config.ts         # Vitest configuration
└── CLAUDE.md                # Claude Code context (comprehensive)
```

## Available Scripts

### Development
- `npm run dev` - Start dev server (http://localhost:5173)
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Code Quality
- `npm run lint` - Lint code with ESLint
- `npm run lint:fix` - Auto-fix linting issues
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting
- `npm run type-check` - Run TypeScript type checking

### Testing
- `npm test` - Run tests
- `npm run test:ui` - Run tests with UI
- `npm run test:coverage` - Generate coverage report

### Package Management
- `npm install <package>` - Add dependency
- `npm install -D <package>` - Add dev dependency

## Claude Code Integration

This template includes comprehensive Claude Code configuration:

### Slash Commands (12)
- `/dev` - Start development server
- `/build` - Build for production
- `/preview` - Preview production build
- `/test` - Run tests
- `/test-ui` - Run tests with UI
- `/coverage` - Generate coverage report
- `/lint` - Run ESLint
- `/lint-fix` - Fix linting issues
- `/format` - Format code
- `/type-check` - TypeScript type checking
- `/install` - Install dependencies
- `/create-component` - Create new component

### Specialized Agents (6)
- **react-security** - Security vulnerability review
- **react-performance** - Performance optimization
- **testing-expert** - Test writing assistance
- **react-expert** - React patterns and best practices
- **query-expert** - TanStack Query specialist
- **accessibility-reviewer** - A11y compliance review

### Skills (3)
- **custom-hooks** - Reusable React hooks patterns
- **component-patterns** - Advanced component patterns
- **query-patterns** - Data fetching patterns

## Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Framework** | React 18 | UI library with concurrent features |
| **Build Tool** | Vite 6 | Fast dev server and optimized builds |
| **Language** | TypeScript 5 | Type-safe development |
| **State Management** | Zustand | Lightweight, flexible state |
| **Data Fetching** | TanStack Query | Server state management |
| **HTTP Client** | Axios | Promise-based HTTP requests |
| **Testing** | Vitest + RTL | Unit and component testing |
| **Linting** | ESLint | Code quality enforcement |
| **Formatting** | Prettier | Consistent code style |

## Development Workflow

1. **Start Development**
   ```bash
   npm run dev
   # Or use Claude Code: /dev
   ```

2. **Make Changes**
   - Write code with TypeScript
   - Components auto-reload with HMR
   - Type errors shown in real-time

3. **Write Tests**
   ```bash
   npm test
   # Or use Claude Code: /test
   ```

4. **Check Code Quality**
   ```bash
   npm run lint
   npm run format
   npm run type-check
   # Or use Claude Code: /lint, /format, /type-check
   ```

5. **Build for Production**
   ```bash
   npm run build
   # Or use Claude Code: /build
   ```

## Best Practices

### Code Organization
- Keep components small and focused
- Use custom hooks for reusable logic
- Colocate related files
- Use TypeScript for all files

### State Management
- Use React state for local/UI state
- Use Zustand for global client state
- Use TanStack Query for server state

### Performance
- Lazy load routes and heavy components
- Use React.memo for expensive components
- Memoize callbacks and values appropriately
- Virtualize long lists

### Testing
- Test behavior, not implementation
- Use Testing Library queries properly
- Mock external dependencies
- Aim for 80%+ coverage on critical code

### Security
- Never put secrets in VITE_ environment variables
- Validate all user input
- Sanitize HTML content
- Use HTTPS in production
- Regular `npm audit` checks

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# API Configuration
VITE_API_URL=http://localhost:3000/api

# App Configuration
VITE_APP_NAME=My React App

# Feature Flags
VITE_ENABLE_ANALYTICS=false
```

**Important**: Only variables prefixed with `VITE_` are exposed to the client. Never put secrets in these variables!

## Troubleshooting

### Common Issues

**Port already in use**
```bash
npm run dev -- --port 3000
```

**Module not found**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Type errors**
```bash
npm run type-check
```

**Test failures**
```bash
npm test -- --watch
# Fix issues and tests re-run automatically
```

## Deployment

### Build
```bash
npm run build
# Output in dist/ directory
```

### Preview Locally
```bash
npm run preview
```

### Deploy
Deploy the `dist/` directory to your hosting provider:
- **Vercel**: `vercel --prod`
- **Netlify**: `netlify deploy --prod`
- **Static Hosting**: Upload `dist/` contents

## Learn More

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vite.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [TanStack Query Documentation](https://tanstack.com/query/latest)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [Claude Code Documentation](https://docs.claude.com/claude-code)

## Contributing

1. Follow the project's code style
2. Write tests for new features
3. Update documentation
4. Submit pull requests with clear descriptions

## License

MIT - See LICENSE file for details

---

**Built with Claude Code** - AI-powered development assistance
