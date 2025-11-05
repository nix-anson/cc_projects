---
description: Build Docker image
argument-hint: '[tag]'
---

Build the Docker image for the Streamlit application.

```bash
docker build -t streamlit-app:${1:-latest} .
```

If $1 is provided, it will be used as the image tag. Otherwise, defaults to "latest".

To run the built image:
```bash
docker run -p 8501:8501 streamlit-app:${1:-latest}
```
