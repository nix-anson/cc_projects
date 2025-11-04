---
description: Run TypeScript type checking
argument-hint: none
allowed-tools: Bash(*)
---

Run TypeScript compiler in check mode to find type errors without generating output files.

Execute: `npm run type-check`

What This Does:
- Runs `tsc --noEmit` to check types
- Scans all TypeScript files
- Reports type errors and warnings
- Doesn't generate JavaScript output
- Doesn't affect build process

What TypeScript Checks:
- **Type Safety**: Variable and function types match
- **Missing Properties**: Required props and object properties
- **Invalid Operations**: Type-incompatible operations
- **Null/Undefined**: Potential null/undefined access
- **Type Inference**: Correct type inference
- **Generic Constraints**: Generic type parameters used correctly

Common Type Errors:
```typescript
// Error: Type 'string' is not assignable to type 'number'
const age: number = "25";

// Error: Property 'email' is missing
interface User { name: string; email: string; }
const user: User = { name: "John" };

// Error: Argument of type 'null' is not assignable
function greet(name: string) {}
greet(null);

// Error: Object is possibly 'undefined'
const user: User | undefined = getUser();
console.log(user.name); // Need to check if user exists first
```

Output Format:
- Shows file name and line number
- Displays specific error message
- Provides error code (e.g., TS2322)
- Summary of total errors found

When to Run:
- Before committing code
- After making type changes
- When adding new features
- Before creating pull request
- Continuously in CI/CD

Benefits of Type Checking:
- **Catch Bugs Early**: Find errors before runtime
- **Better Refactoring**: Safe code changes
- **Documentation**: Types serve as documentation
- **IDE Support**: Better autocomplete and hints
- **Confidence**: Know your code is type-safe

Fixing Type Errors:
1. Read the error message carefully
2. Check the file and line number
3. Understand what types are expected vs received
4. Fix the type mismatch
5. Re-run type-check to verify

Common Fixes:
```typescript
// Add type annotations
const name: string = "John";

// Handle undefined cases
const user = getUser();
if (user) {
  console.log(user.name);
}

// Fix prop types
interface Props {
  name: string;
  age?: number; // Optional property
}

// Use type guards
function isString(value: unknown): value is string {
  return typeof value === "string";
}
```

IDE Integration:
- Most IDEs show type errors in real-time
- VS Code with TypeScript extension
- WebStorm has built-in TypeScript support
- Inline errors save time vs running command

Build vs Type-Check:
- `/build` runs type-check automatically
- `/type-check` is faster (no output generation)
- Use type-check during development
- Build ensures production readiness

Strict Mode:
- Project uses strict TypeScript settings
- Catches more potential issues
- Requires explicit null handling
- No implicit `any` types
- Better type safety overall

Notes:
- Type-checking is fast (seconds)
- Doesn't modify any files
- Safe to run anytime
- Zero errors should be the goal
- Types are compile-time only, no runtime overhead

Integration:
- Runs automatically in dev mode (Vite)
- Should run in CI/CD pipeline
- Can be added to pre-commit hooks
- IDE extensions provide real-time feedback

Common issues:
- "Cannot find module" - Check import paths and installed types
- "Implicit any" - Add type annotations
- "Strict null checks" - Handle potential null/undefined values
- "Type instantiation is excessively deep" - Simplify complex types
