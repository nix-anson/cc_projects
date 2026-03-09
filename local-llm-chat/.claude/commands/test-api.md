---
description: Run the pytest test suite
---

Execute all tests with verbose output.

```bash
pytest tests/ -v --tb=short
```

Run only API tests:
```bash
pytest tests/test_api.py -v
```

Run only WebSocket tests:
```bash
pytest tests/test_streaming.py -v
```

Run with coverage:
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```
