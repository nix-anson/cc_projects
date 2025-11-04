---
description: Run Django test suite
argument-hint: [app_name] [--keepdb] [--parallel] [-v 2]
allowed-tools: Bash(*), Read(*)
---

Run Django tests with various options for test execution.

Arguments:
- $ARGUMENTS: All arguments passed to the test command

Common usage patterns:
- `/test` - Run all tests
- `/test app_name` - Run tests for specific app
- `/test app_name.tests.TestClass` - Run specific test class
- `/test app_name.tests.TestClass.test_method` - Run specific test method
- `/test --keepdb` - Preserve test database between runs (faster)
- `/test --parallel` - Run tests in parallel
- `/test -v 2` - Verbose output

Execute: `python manage.py test $ARGUMENTS`

After running tests:
1. Report the number of tests run
2. Show any failures or errors with details
3. Display test coverage summary if available
4. Suggest fixes for common test failures

Best practices:
- Use `--keepdb` for faster test runs during development
- Use `--parallel` for large test suites
- Aim for 80%+ test coverage
- Write tests for models, views, and business logic
