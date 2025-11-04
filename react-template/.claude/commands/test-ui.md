---
description: Run tests with Vitest UI interface
argument-hint: none
allowed-tools: Bash(*)
---

Launch Vitest's browser-based UI for an interactive testing experience.

Execute: `npm test -- --ui`

Features:
- **Visual Interface**: See all tests in a browser-based UI
- **Interactive Filtering**: Filter tests by name, file, or status
- **Real-time Updates**: Tests re-run automatically on file changes
- **Detailed Reports**: View test results, errors, and stack traces
- **Code Coverage**: Visual coverage reports
- **Test Hierarchy**: See test structure and organization

The UI will open automatically in your default browser at http://localhost:51204/__vitest__/

UI Benefits:
- Easier to navigate large test suites
- Better visualization of test results
- Click to run specific tests
- View console logs and errors inline
- Debug tests more easily

Usage:
1. Run `/test-ui` to start
2. Browser opens with test dashboard
3. All tests run automatically
4. Click on tests to see details
5. Tests re-run on code changes
6. Press Ctrl+C in terminal to stop

When to Use:
- Debugging failing tests
- Exploring test suite structure
- During active development
- When you prefer visual feedback

When Not to Use:
- CI/CD pipelines (use `/test` instead)
- Quick test runs (terminal is faster)
- Headless environments

Notes:
- UI server runs alongside test runner
- Changes to code trigger automatic re-runs
- Can filter tests by success/failure/skipped
- View coverage metrics visually
- Great for demos and presentations

Common issues:
- Port already in use - Vitest will try alternative ports
- Browser doesn't open - Check terminal for URL and open manually
- Slow performance - Close UI and use terminal for better performance
