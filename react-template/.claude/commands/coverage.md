---
description: Generate test coverage report
argument-hint: none
allowed-tools: Bash(*)
---

Run all tests and generate a comprehensive code coverage report.

Execute: `npm test -- --coverage`

What This Does:
- Runs entire test suite
- Tracks which lines of code are executed
- Generates coverage statistics
- Creates HTML coverage report

Coverage Metrics:
- **Statements**: Percentage of statements executed
- **Branches**: Percentage of conditional branches tested
- **Functions**: Percentage of functions called
- **Lines**: Percentage of lines executed

Output:
1. **Terminal**: Summary table with coverage percentages
2. **HTML Report**: Detailed interactive report in `coverage/` directory

Coverage Report Structure:
```
coverage/
├── index.html          # Main coverage report (open in browser)
├── lcov.info          # LCOV format for tools
└── [source files]     # Per-file coverage details
```

Viewing the Report:
- Open `coverage/index.html` in your browser
- Navigate through files to see line-by-line coverage
- Red lines = not covered
- Green lines = covered
- Yellow lines = partially covered (branches)

Coverage Goals:
- **Overall**: Aim for 80%+ coverage
- **Critical Code**: Aim for 90%+ coverage
- **Utilities**: Aim for 100% coverage
- **UI Components**: Aim for 80%+ coverage

Interpreting Results:
- **High Coverage (>80%)**: Good test coverage
- **Medium Coverage (60-80%)**: Add more tests for critical paths
- **Low Coverage (<60%)**: Significant testing gaps

What to Focus On:
1. Critical business logic
2. Complex functions and algorithms
3. Error handling and edge cases
4. User-facing features
5. Security-sensitive code

What Not to Worry About:
- Configuration files
- Type definitions
- Simple pass-through code
- Third-party library wrappers

Improving Coverage:
1. Identify uncovered lines in report
2. Write tests for uncovered code
3. Focus on important functionality first
4. Don't chase 100% blindly - quality over quantity

Integration:
- Can be integrated with CI/CD
- Upload to services like Codecov or Coveralls
- Set coverage thresholds to fail CI if coverage drops

Notes:
- Coverage reports are in `.gitignore`
- Coverage doesn't guarantee quality, just execution
- 100% coverage doesn't mean bug-free code
- Focus on testing behavior, not just coverage numbers

Common issues:
- "No coverage data" - Ensure tests are actually running
- Low coverage - Write more tests for uncovered code
- False positives - Some code may not need testing (types, configs)
