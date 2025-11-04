---
description: Create a new React component with TypeScript
argument-hint: <component-name> [--type TYPE]
allowed-tools: Read, Write, Bash
---

Create a new React component following project conventions and best practices.

Arguments:
- `$1` - Component name (PascalCase, e.g., UserProfile, ProductCard)
- `--type` - Component type: 'common', 'layout', 'feature', or 'page' (default: 'common')

Common usage patterns:
- `/create-component Button` - Create common component
- `/create-component UserProfile --type feature` - Create feature component
- `/create-component Dashboard --type page` - Create page component
- `/create-component Header --type layout` - Create layout component

Component Types:
- **common**: Reusable UI components (Button, Card, Input, etc.)
  - Location: `src/components/common/`
  - Examples: Button, Modal, Dropdown

- **feature**: Feature-specific components
  - Location: `src/components/features/`
  - Examples: UserProfile, ProductList, OrderSummary

- **layout**: Layout components
  - Location: `src/components/layout/`
  - Examples: Header, Footer, Sidebar, MainLayout

- **page**: Page-level components/routes
  - Location: `src/pages/`
  - Examples: Dashboard, Profile, Settings

What Gets Created:
1. Component file: `ComponentName.tsx`
2. Test file: `ComponentName.test.tsx`
3. Exports added to index file

Component Template:
```typescript
// ComponentName.tsx
interface ComponentNameProps {
  className?: string;
  children?: React.ReactNode;
}

export function ComponentName({ className, children }: ComponentNameProps) {
  return (
    <div className={className}>
      {children}
    </div>
  );
}
```

Test Template:
```typescript
// ComponentName.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders correctly', () => {
    render(<ComponentName>Test</ComponentName>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
});
```

Best Practices Applied:
- TypeScript with proper prop types
- Functional component pattern
- Named export (not default)
- Props interface defined
- Test file created automatically
- Follows project structure

Component Naming:
- Use PascalCase (UserProfile, not userProfile or user-profile)
- Descriptive names (Button not Btn, Navigation not Nav)
- Singular nouns for most components
- Plural for collections (UserList, ProductGrid)

After Creating:
1. Implement component logic
2. Add styles (inline, CSS modules, or styled)
3. Write comprehensive tests
4. Add prop validation
5. Document complex props with JSDoc

Example Usage:
```bash
# Create a button component
/create-component Button

# Create a user profile feature
/create-component UserProfile --type feature

# Create a dashboard page
/create-component Dashboard --type page
```

Next Steps After Creation:
1. Open the created files
2. Implement the component logic
3. Add necessary props and types
4. Style the component
5. Write tests
6. Use the component in your app

Notes:
- Component files are created in appropriate directories
- Tests are co-located with components
- Index files updated for easy imports
- Follows established project patterns
- TypeScript-first approach

Common issues:
- Component already exists - Check if file exists first
- Wrong directory - Verify --type flag
- Import errors - Ensure exports are added correctly
- Name conflicts - Use unique, descriptive names
