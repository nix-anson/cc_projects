# React Project - Claude Code Configuration

## Project Type
Modern React 18 application with Vite, TypeScript, and comprehensive tooling

## Technology Stack
- **React**: 18.x (latest stable with concurrent features)
- **Build Tool**: Vite 6.x (fast dev server and optimized builds)
- **Language**: TypeScript 5.x (type-safe development)
- **State Management**: Zustand (lightweight, flexible state)
- **Data Fetching**: TanStack Query (React Query) + Axios
- **Testing**: Vitest + React Testing Library
- **Code Quality**: ESLint + Prettier

## Project Structure and Architecture

### Recommended Folder Structure
```
project-name/
├── public/                      # Static assets
│   └── vite.svg
├── src/
│   ├── assets/                  # Images, fonts, styles
│   ├── components/              # Reusable UI components
│   │   ├── common/             # Generic components (Button, Card, etc.)
│   │   ├── layout/             # Layout components (Header, Footer, Sidebar)
│   │   └── features/           # Feature-specific components
│   ├── hooks/                   # Custom React hooks
│   ├── pages/                   # Page-level components/routes
│   ├── services/                # API services and data fetching
│   │   ├── api/                # API clients and endpoints
│   │   ├── queries/            # React Query hooks
│   │   └── mutations/          # React Query mutations
│   ├── store/                   # Zustand stores
│   ├── types/                   # TypeScript type definitions
│   ├── utils/                   # Utility functions and helpers
│   ├── constants/               # App constants and configuration
│   ├── App.tsx                  # Root component
│   ├── main.tsx                 # Application entry point
│   └── vite-env.d.ts           # Vite type declarations
├── tests/                       # Test files
│   ├── setup.ts                # Test setup and configuration
│   └── __mocks__/              # Test mocks
├── .env                         # Environment variables (gitignored)
├── .env.example                 # Example environment variables
├── .eslintrc.cjs               # ESLint configuration
├── .prettierrc                  # Prettier configuration
├── .gitignore                   # Git ignore rules
├── index.html                   # HTML entry point
├── package.json                 # Dependencies and scripts
├── tsconfig.json               # TypeScript configuration
├── tsconfig.node.json          # TypeScript config for Node files
├── vite.config.ts              # Vite configuration
└── vitest.config.ts            # Vitest configuration
```

## Common npm Commands

### Development Server
- `npm run dev` - Start Vite development server (hot reload)
- `npm run dev -- --host` - Expose dev server to network
- `npm run dev -- --port 3000` - Start on specific port

### Building
- `npm run build` - Build production bundle
- `npm run build -- --mode staging` - Build with staging environment
- `npm run preview` - Preview production build locally

### Code Quality
- `npm run lint` - Run ESLint on source files
- `npm run lint:fix` - Auto-fix ESLint issues
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting
- `npm run type-check` - Run TypeScript compiler checks

### Testing
- `npm run test` - Run tests with Vitest
- `npm run test:ui` - Run tests with UI interface
- `npm run test:coverage` - Generate test coverage report
- `npm test -- --watch` - Run tests in watch mode
- `npm test -- MyComponent.test.tsx` - Run specific test file

### Package Management
- `npm install package-name` - Install new dependency
- `npm install -D package-name` - Install dev dependency
- `npm update` - Update dependencies
- `npm outdated` - Check for outdated packages
- `npm audit` - Check for security vulnerabilities
- `npm audit fix` - Fix security issues automatically

## Code Style and Conventions

### TypeScript/React Style
- Follow Airbnb React style guide principles
- Use 2 spaces for indentation (JavaScript/TypeScript standard)
- Maximum line length: 100 characters
- Use descriptive variable names in camelCase
- Component names in PascalCase
- Constants in UPPER_SNAKE_CASE
- File names match component names: `UserProfile.tsx`

### Component Conventions

**Functional Components with TypeScript**:
```typescript
// components/UserProfile.tsx
interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
  className?: string;
}

export function UserProfile({ userId, onUpdate, className }: UserProfileProps) {
  const [isLoading, setIsLoading] = useState(false);

  // Component logic here

  return (
    <div className={className}>
      {/* JSX content */}
    </div>
  );
}
```

**Component Organization**:
1. Interface/type definitions
2. Component function
3. Internal hooks and state
4. Effects
5. Event handlers
6. Render logic
7. Export at the bottom or top (be consistent)

### Props and Types

**Always define prop types**:
```typescript
// Good - explicit types
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick: () => void;
  children: React.ReactNode;
}

// Use type for unions/intersections
type IconButtonProps = ButtonProps & {
  icon: React.ReactNode;
  ariaLabel: string;
};
```

### Custom Hooks Conventions

**Naming and Structure**:
```typescript
// hooks/useAuth.ts
interface UseAuthReturn {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Hook logic

  return {
    user,
    isAuthenticated: !!user,
    login,
    logout,
    isLoading
  };
}
```

**Hook Best Practices**:
- Prefix with `use` (required by React)
- Return objects for multiple values, not arrays (unless order matters)
- Document dependencies and side effects
- Keep hooks focused and single-purpose
- Extract complex logic into custom hooks

## State Management with Zustand

### Store Structure
```typescript
// store/authStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthState {
  // State
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;

  // Actions
  login: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (updates: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  devtools(
    persist(
      (set) => ({
        // Initial state
        user: null,
        token: null,
        isAuthenticated: false,

        // Actions
        login: (user, token) => set({
          user,
          token,
          isAuthenticated: true
        }),

        logout: () => set({
          user: null,
          token: null,
          isAuthenticated: false
        }),

        updateUser: (updates) => set((state) => ({
          user: state.user ? { ...state.user, ...updates } : null
        })),
      }),
      { name: 'auth-storage' }
    )
  )
);
```

### Using Stores in Components
```typescript
// Selective subscription (prevents unnecessary re-renders)
function UserProfile() {
  const user = useAuthStore((state) => state.user);
  const updateUser = useAuthStore((state) => state.updateUser);

  // Component logic
}

// Multiple selections
function Header() {
  const { user, logout, isAuthenticated } = useAuthStore((state) => ({
    user: state.user,
    logout: state.logout,
    isAuthenticated: state.isAuthenticated
  }));
}
```

**Zustand Best Practices**:
- Use selectors to prevent unnecessary re-renders
- Keep stores focused on related state
- Use middleware (devtools, persist) for better DX
- Create actions within the store, not external functions
- Split large stores into multiple stores
- Use computed values with selectors, not stored derived state

## Data Fetching with React Query

### Setup and Configuration
```typescript
// main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      cacheTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <QueryClientProvider client={queryClient}>
    <App />
    <ReactQueryDevtools initialIsOpen={false} />
  </QueryClientProvider>
);
```

### Query Organization Pattern
```typescript
// services/api/users.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const usersApi = {
  getUser: async (id: string): Promise<User> => {
    const { data } = await api.get(`/users/${id}`);
    return data;
  },

  getUsers: async (params?: UsersParams): Promise<User[]> => {
    const { data } = await api.get('/users', { params });
    return data;
  },

  createUser: async (user: CreateUserInput): Promise<User> => {
    const { data } = await api.post('/users', user);
    return data;
  },

  updateUser: async (id: string, updates: Partial<User>): Promise<User> => {
    const { data } = await api.patch(`/users/${id}`, updates);
    return data;
  },

  deleteUser: async (id: string): Promise<void> => {
    await api.delete(`/users/${id}`);
  },
};

// services/queries/users.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { usersApi } from '../api/users';

// Query keys
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (params?: UsersParams) => [...userKeys.lists(), params] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

// Query hooks
export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => usersApi.getUser(id),
    enabled: !!id, // Only run if id exists
  });
}

export function useUsers(params?: UsersParams) {
  return useQuery({
    queryKey: userKeys.list(params),
    queryFn: () => usersApi.getUsers(params),
  });
}

// Mutation hooks
export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: usersApi.createUser,
    onSuccess: () => {
      // Invalidate and refetch users list
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, updates }: { id: string; updates: Partial<User> }) =>
      usersApi.updateUser(id, updates),
    onSuccess: (data, variables) => {
      // Update cache for specific user
      queryClient.setQueryData(userKeys.detail(variables.id), data);
      // Invalidate lists
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}

// Usage in components
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useUser(userId);
  const updateMutation = useUpdateUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>User not found</div>;

  const handleUpdate = () => {
    updateMutation.mutate({
      id: userId,
      updates: { name: 'New Name' }
    });
  };

  return <div>{/* Render user */}</div>;
}
```

**React Query Best Practices**:
- Organize queries by resource (users, posts, etc.)
- Use query keys factory for consistency
- Keep API calls separate from hooks
- Use optimistic updates for better UX
- Handle loading and error states consistently
- Leverage `enabled` option for conditional queries
- Use `select` option to transform data

## Testing Strategy

### Test Structure with Vitest
```typescript
// tests/setup.ts
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});

// Component tests
// components/Button.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });
});

// Hook tests
// hooks/useCounter.test.ts
import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

**Testing Best Practices**:
- Test behavior, not implementation
- Use Testing Library queries in order of preference: getByRole > getByLabelText > getByText
- Mock external dependencies (API calls, etc.)
- Test error states and edge cases
- Use `userEvent` instead of `fireEvent` for more realistic interactions
- Keep tests focused and independent
- Aim for 80%+ coverage on critical paths

## React Best Practices

### Component Patterns

**1. Composition over Inheritance**:
```typescript
// Good - Composition
interface CardProps {
  header?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

function Card({ header, children, footer }: CardProps) {
  return (
    <div className="card">
      {header && <div className="card-header">{header}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

// Usage
<Card
  header={<h2>Title</h2>}
  footer={<button>Action</button>}
>
  <p>Content</p>
</Card>
```

**2. Compound Components**:
```typescript
interface TabsProps {
  defaultValue: string;
  children: React.ReactNode;
}

interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

export function Tabs({ defaultValue, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.List = function TabsList({ children }: { children: React.ReactNode }) {
  return <div className="tabs-list">{children}</div>;
};

Tabs.Trigger = function TabsTrigger({ value, children }: { value: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  return (
    <button
      className={context?.activeTab === value ? 'active' : ''}
      onClick={() => context?.setActiveTab(value)}
    >
      {children}
    </button>
  );
};

Tabs.Content = function TabsContent({ value, children }: { value: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  if (context?.activeTab !== value) return null;
  return <div className="tabs-content">{children}</div>;
};

// Usage
<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Trigger value="tab1">Tab 1</Tabs.Trigger>
    <Tabs.Trigger value="tab2">Tab 2</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="tab1">Content 1</Tabs.Content>
  <Tabs.Content value="tab2">Content 2</Tabs.Content>
</Tabs>
```

**3. Render Props Pattern** (use sparingly, hooks are often better):
```typescript
interface MouseTrackerProps {
  render: (position: { x: number; y: number }) => React.ReactNode;
}

function MouseTracker({ render }: MouseTrackerProps) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return <>{render(position)}</>;
}

// Usage (but consider using a hook instead)
<MouseTracker render={({ x, y }) => <p>Mouse at {x}, {y}</p>} />
```

### Performance Optimization

**1. Memoization**:
```typescript
// useMemo for expensive calculations
function ProductList({ products, filter }: Props) {
  const filteredProducts = useMemo(() => {
    return products.filter(product =>
      product.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [products, filter]);

  return <div>{/* render filtered products */}</div>;
}

// useCallback for function identity
function Parent() {
  const [count, setCount] = useState(0);

  // Without useCallback, handleClick is recreated on every render
  const handleClick = useCallback(() => {
    setCount(c => c + 1);
  }, []); // Empty deps - function never changes

  return <ExpensiveChild onClick={handleClick} />;
}

// React.memo for component memoization
export const ExpensiveChild = memo(function ExpensiveChild({ onClick }: Props) {
  // Only re-renders if props change
  return <button onClick={onClick}>Click me</button>;
});
```

**2. Code Splitting**:
```typescript
// Lazy load routes
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Suspense>
  );
}
```

**3. Virtualization for Long Lists**:
```typescript
// Consider using @tanstack/react-virtual for long lists
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: string[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            {items[virtualItem.index]}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Security Best Practices

### Essential Security Measures

**1. XSS Prevention**:
```typescript
// React escapes by default
<div>{userInput}</div> // Safe

// Dangerous - only use with trusted content
<div dangerouslySetInnerHTML={{ __html: untrustedHTML }} /> // AVOID!

// Safe HTML rendering - use a library
import DOMPurify from 'dompurify';

function SafeHTML({ html }: { html: string }) {
  const clean = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

**2. Authentication Tokens**:
```typescript
// Store tokens securely (not in localStorage for sensitive apps)
// Use httpOnly cookies for highly sensitive tokens

// API client with auth
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - logout user
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);
```

**3. Environment Variables**:
```typescript
// .env (gitignored!)
VITE_API_URL=http://localhost:3000/api
VITE_APP_NAME=MyApp

// .env.example (committed)
VITE_API_URL=
VITE_APP_NAME=

// Usage in code
const apiUrl = import.meta.env.VITE_API_URL;

// NEVER expose secrets in client code
// NEVER commit .env files
```

**4. Input Validation**:
```typescript
// Validate all user input
function LoginForm() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateEmail(email)) {
      setError('Invalid email address');
      return;
    }

    // Proceed with submission
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      {error && <span className="error">{error}</span>}
      <button type="submit">Login</button>
    </form>
  );
}
```

**5. CSRF Protection**:
```typescript
// Include CSRF token in requests
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

api.defaults.headers.common['X-CSRF-Token'] = csrfToken;
```

### Security Checklist
- [ ] All user input is validated and sanitized
- [ ] Sensitive data (tokens) stored securely
- [ ] Environment variables for configuration
- [ ] HTTPS in production
- [ ] Dependencies regularly updated
- [ ] No secrets in client-side code
- [ ] Content Security Policy (CSP) headers
- [ ] Implement rate limiting on API calls
- [ ] Use TypeScript for type safety
- [ ] Regular security audits (`npm audit`)

## TypeScript Best Practices

### Type Safety
```typescript
// Use strict mode in tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}

// Define types for all props and state
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest'; // Union types for specific values
}

// Use generics for reusable components
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Utility types
type PartialUser = Partial<User>; // All properties optional
type RequiredUser = Required<User>; // All properties required
type UserWithoutEmail = Omit<User, 'email'>; // Exclude properties
type UserIdAndName = Pick<User, 'id' | 'name'>; // Include only specific properties
```

## Vite Configuration

### Common Configurations
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],

  // Path aliases
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@types': path.resolve(__dirname, './src/types'),
    },
  },

  // Server configuration
  server: {
    port: 3000,
    open: true, // Open browser automatically
    proxy: {
      // Proxy API requests during development
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },

  // Build configuration
  build: {
    sourcemap: true, // Generate source maps
    rollupOptions: {
      output: {
        // Code splitting
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'query-vendor': ['@tanstack/react-query'],
        },
      },
    },
  },

  // Environment variables prefix
  envPrefix: 'VITE_',
});
```

## Common Packages and Tools

### Essential Dependencies
- `react` - React library
- `react-dom` - React DOM rendering
- `@tanstack/react-query` - Data fetching and caching
- `zustand` - State management
- `axios` - HTTP client
- `react-router-dom` - Routing (if needed)

### Development Dependencies
- `@vitejs/plugin-react` - Vite React plugin
- `typescript` - TypeScript compiler
- `vitest` - Testing framework
- `@testing-library/react` - React testing utilities
- `@testing-library/jest-dom` - Custom matchers
- `@testing-library/user-event` - User interaction simulation
- `eslint` - Code linting
- `prettier` - Code formatting
- `@typescript-eslint/parser` - TypeScript ESLint parser
- `@typescript-eslint/eslint-plugin` - TypeScript ESLint rules

### Optional but Recommended
- `react-router-dom` - Client-side routing
- `@tanstack/react-virtual` - Virtualization for long lists
- `date-fns` - Date utilities (lighter than moment.js)
- `zod` - Schema validation
- `react-hook-form` - Form management
- `tailwindcss` - Utility-first CSS framework
- `clsx` - Conditional className utility
- `@radix-ui/*` - Accessible UI primitives

## Documentation Links

### Official Documentation
- React: https://react.dev/
- Vite: https://vite.dev/
- TypeScript: https://www.typescriptlang.org/docs/
- TanStack Query: https://tanstack.com/query/latest
- Zustand: https://github.com/pmndrs/zustand
- Vitest: https://vitest.dev/
- Testing Library: https://testing-library.com/react

### Style Guides and Best Practices
- React TypeScript Cheatsheet: https://react-typescript-cheatsheet.netlify.app/
- Airbnb React Style Guide: https://airbnb.io/javascript/react/

## Custom Commands and Agents

This template includes:
- **Slash Commands**: Quick access to common React/Vite operations
- **Subagents**: Specialized AI assistants for React development
- **Skills**: Automated patterns for React code generation

Use `/help` to see available commands and `@` to invoke specific agents.

---

**Remember**: React is declarative and component-based. Focus on building reusable components, managing state effectively, and optimizing performance only when needed. TypeScript adds type safety that catches bugs at compile time. Always prioritize user experience and accessibility.
