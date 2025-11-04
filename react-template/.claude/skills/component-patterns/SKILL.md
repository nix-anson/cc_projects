---
name: component-patterns
description: Implement advanced React component patterns including compound components, render props, and composition patterns. Use when building flexible, reusable component APIs.
allowed-tools: Read, Write, Grep
---

You are a React component patterns expert. You help implement advanced component patterns for flexible, maintainable component libraries.

## Component Pattern Implementations

### 1. Compound Components Pattern

Best for components with multiple related sub-components that share implicit state.

```typescript
// components/Tabs.tsx
import { createContext, useContext, useState, ReactNode } from 'react';

interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabs() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tabs compound components must be used within Tabs');
  }
  return context;
}

interface TabsProps {
  defaultValue: string;
  onChange?: (value: string) => void;
  children: ReactNode;
}

export function Tabs({ defaultValue, onChange, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue);

  const handleTabChange = (value: string) => {
    setActiveTab(value);
    onChange?.(value);
  };

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab: handleTabChange }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.List = function TabsList({ children }: { children: ReactNode }) {
  return (
    <div className="tabs-list" role="tablist">
      {children}
    </div>
  );
};

Tabs.Trigger = function TabsTrigger({
  value,
  children,
}: {
  value: string;
  children: ReactNode;
}) {
  const { activeTab, setActiveTab } = useTabs();
  const isActive = activeTab === value;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      onClick={() => setActiveTab(value)}
      className={isActive ? 'tab-trigger active' : 'tab-trigger'}
    >
      {children}
    </button>
  );
};

Tabs.Content = function TabsContent({
  value,
  children,
}: {
  value: string;
  children: ReactNode;
}) {
  const { activeTab } = useTabs();
  if (activeTab !== value) return null;

  return (
    <div role="tabpanel" className="tab-content">
      {children}
    </div>
  );
};

// Usage
<Tabs defaultValue="profile" onChange={(val) => console.log(val)}>
  <Tabs.List>
    <Tabs.Trigger value="profile">Profile</Tabs.Trigger>
    <Tabs.Trigger value="account">Account</Tabs.Trigger>
    <Tabs.Trigger value="settings">Settings</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="profile">Profile content</Tabs.Content>
  <Tabs.Content value="account">Account content</Tabs.Content>
  <Tabs.Content value="settings">Settings content</Tabs.Content>
</Tabs>
```

### 2. Render Props Pattern (Legacy, Hooks Preferred)

For sharing code between components using a prop whose value is a function.

```typescript
// components/MouseTracker.tsx
interface MousePosition {
  x: number;
  y: number;
}

interface MouseTrackerProps {
  render: (position: MousePosition) => ReactNode;
}

function MouseTracker({ render }: MouseTrackerProps) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      setPosition({ x: event.clientX, y: event.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return <>{render(position)}</>;
}

// Usage
<MouseTracker
  render={({ x, y }) => (
    <p>Mouse position: {x}, {y}</p>
  )}
/>

// Better: Use custom hook instead
function useMousePosition() {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return position;
}

// Usage with hook (preferred)
function Component() {
  const { x, y } = useMousePosition();
  return <p>Mouse position: {x}, {y}</p>;
}
```

### 3. Component Composition Pattern

Building complex UIs from simple, focused components.

```typescript
// components/Card.tsx
interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`card ${className}`}>
      {children}
    </div>
  );
}

Card.Header = function CardHeader({ children, className = '' }: CardProps) {
  return <div className={`card-header ${className}`}>{children}</div>;
};

Card.Body = function CardBody({ children, className = '' }: CardProps) {
  return <div className={`card-body ${className}`}>{children}</div>;
};

Card.Footer = function CardFooter({ children, className = '' }: CardProps) {
  return <div className={`card-footer ${className}`}>{children}</div>;
};

Card.Title = function CardTitle({ children, className = '' }: CardProps) {
  return <h3 className={`card-title ${className}`}>{children}</h3>;
};

Card.Description = function CardDescription({ children, className = '' }: CardProps) {
  return <p className={`card-description ${className}`}>{children}</p>;
};

// Usage
<Card>
  <Card.Header>
    <Card.Title>User Profile</Card.Title>
    <Card.Description>Manage your profile information</Card.Description>
  </Card.Header>
  <Card.Body>
    <UserForm />
  </Card.Body>
  <Card.Footer>
    <Button>Save</Button>
    <Button variant="outline">Cancel</Button>
  </Card.Footer>
</Card>
```

### 4. Controlled vs Uncontrolled Pattern

Support both controlled and uncontrolled modes in a single component.

```typescript
// components/Input.tsx
interface InputProps {
  value?: string;  // Controlled
  defaultValue?: string;  // Uncontrolled
  onChange?: (value: string) => void;
  placeholder?: string;
}

export function Input({
  value: controlledValue,
  defaultValue,
  onChange,
  placeholder,
}: InputProps) {
  // Internal state for uncontrolled mode
  const [internalValue, setInternalValue] = useState(defaultValue ?? '');

  // Determine if controlled
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : internalValue;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;

    if (!isControlled) {
      setInternalValue(newValue);
    }

    onChange?.(newValue);
  };

  return (
    <input
      value={value}
      onChange={handleChange}
      placeholder={placeholder}
    />
  );
}

// Usage - Controlled
function ControlledExample() {
  const [value, setValue] = useState('');
  return <Input value={value} onChange={setValue} />;
}

// Usage - Uncontrolled
function UncontrolledExample() {
  return <Input defaultValue="initial" onChange={(val) => console.log(val)} />;
}
```

### 5. Provider Pattern

Share data and functions across component tree without prop drilling.

```typescript
// context/ThemeContext.tsx
interface Theme {
  colors: {
    primary: string;
    secondary: string;
    background: string;
  };
  mode: 'light' | 'dark';
}

interface ThemeContextValue {
  theme: Theme;
  setMode: (mode: 'light' | 'dark') => void;
  toggleMode: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

const lightTheme: Theme = {
  colors: {
    primary: '#007bff',
    secondary: '#6c757d',
    background: '#ffffff',
  },
  mode: 'light',
};

const darkTheme: Theme = {
  colors: {
    primary: '#0d6efd',
    secondary: '#6c757d',
    background: '#212529',
  },
  mode: 'dark',
};

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [mode, setMode] = useState<'light' | 'dark'>('light');

  const theme = mode === 'light' ? lightTheme : darkTheme;

  const toggleMode = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={{ theme, setMode, toggleMode }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Usage
function App() {
  return (
    <ThemeProvider>
      <Layout />
    </ThemeProvider>
  );
}

function ThemedButton() {
  const { theme, toggleMode } = useTheme();

  return (
    <button
      style={{ backgroundColor: theme.colors.primary }}
      onClick={toggleMode}
    >
      Toggle Theme
    </button>
  );
}
```

### 6. HOC Pattern (Legacy, Hooks Preferred)

Higher-Order Components for cross-cutting concerns.

```typescript
// hocs/withAuth.tsx
interface WithAuthProps {
  isAuthenticated: boolean;
  user: User | null;
}

function withAuth<P extends object>(
  Component: ComponentType<P & WithAuthProps>
) {
  return function WithAuthComponent(props: P) {
    const { isAuthenticated, user } = useAuth();

    if (!isAuthenticated) {
      return <Navigate to="/login" />;
    }

    return <Component {...props} isAuthenticated={isAuthenticated} user={user} />;
  };
}

// Usage
interface DashboardProps extends WithAuthProps {
  title: string;
}

function Dashboard({ title, user }: DashboardProps) {
  return <div>Welcome {user?.name} to {title}</div>;
}

export default withAuth(Dashboard);

// Better: Use hook instead
function Dashboard({ title }: { title: string }) {
  const { user } = useAuth();
  return <div>Welcome {user?.name} to {title}</div>;
}
```

## Pattern Selection Guide

| Pattern | Use When | Example |
|---------|----------|---------|
| Compound Components | Building flexible component APIs with shared state | Tabs, Accordion, Dropdown |
| Composition | Building complex UIs from simple pieces | Card, Layout, Form |
| Controlled/Uncontrolled | Creating flexible form inputs | Input, Select, Checkbox |
| Provider | Sharing state without prop drilling | Theme, Auth, i18n |
| Custom Hooks | Extracting reusable logic | useLocalStorage, useDebounce |
| Render Props | (Legacy) Code sharing | Use hooks instead |
| HOC | (Legacy) Cross-cutting concerns | Use hooks instead |

## Best Practices

1. **Prefer Hooks Over HOCs/Render Props**
2. **Use TypeScript** for type-safe APIs
3. **Document Patterns** with examples
4. **Keep Components Focused** on single responsibility
5. **Compose Small Components** into larger ones
6. **Provide Sensible Defaults**
7. **Make APIs Flexible** but not complex

This skill helps you implement modern React component patterns for building flexible, reusable component libraries.
