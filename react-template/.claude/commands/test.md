---
description: Run tests with Vitest
argument-hint: [--watch] [--coverage] [FILE_PATTERN]
allowed-tools: Bash(*)
---

Run unit and component tests using Vitest and React Testing Library.

Arguments:
- $ARGUMENTS: All arguments passed to the test command

Common usage patterns:
- `/test` - Run all tests once
- `/test --watch` - Run tests in watch mode (re-run on file changes)
- `/test --coverage` - Run tests and generate coverage report
- `/test Button` - Run tests matching "Button" pattern
- `/test src/components` - Run tests in specific directory
- `/test --ui` - Open Vitest UI in browser (use `/test-ui` command instead)
- `/test --run` - Run tests without watch mode (CI mode)

Execute: `npm test -- $ARGUMENTS`

Test Organization:
- Test files: `*.test.ts`, `*.test.tsx`, `*.spec.ts`, `*.spec.tsx`
- Location: Co-located with source files or in `tests/` directory
- Setup: `tests/setup.ts` configures test environment

What Gets Tested:
- Component rendering and behavior
- User interactions (clicks, typing, etc.)
- Hook logic and state management
- Utility functions
- API integration (mocked)

Test Output:
- Shows passed/failed tests
- Displays error messages and stack traces
- Reports test execution time
- Coverage summary (if --coverage flag used)

Features:
- **Fast Execution**: Vitest is extremely fast
- **Watch Mode**: Auto-reruns tests on file changes
- **Coverage**: Built-in code coverage with c8
- **TypeScript**: Full TypeScript support
- **Snapshot Testing**: Component snapshot testing

Best Practices:
- Write tests for critical functionality
- Test user behavior, not implementation
- Keep tests focused and independent
- Mock external dependencies
- Aim for 80%+ coverage on important code

Common Patterns:
```typescript
// Component test
describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});

// Hook test
describe('useCounter', () => {
  it('increments count', () => {
    const { result } = renderHook(() => useCounter());
    act(() => result.current.increment());
    expect(result.current.count).toBe(1);
  });
});
```

Notes:
- Tests run in jsdom environment (simulates browser)
- Watch mode is great during development
- Run all tests before committing code
- CI/CD should run tests automatically

Common issues:
- "Cannot find module" - Check test setup and imports
- "Timeout" - Async tests need proper waiting (waitFor, findBy)
- "Act warning" - Wrap state updates in act() or use Testing Library queries
- Flaky tests - Usually caused by async timing issues
