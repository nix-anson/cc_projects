---
description: Start Streamlit development server
argument-hint: '[port]'
---

Start the Streamlit development server on the specified port (default: 8501).

```bash
streamlit run main.py --server.port=${1:-8501}
```

The app will be available at http://localhost:${1:-8501}
