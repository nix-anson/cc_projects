---
description: Start JupyterLab server with all extensions and configurations
---

Start the JupyterLab development server with all installed extensions and configurations.

## Instructions

1. Ensure the virtual environment is activated
2. Check if port 8888 is available (or use the port from .env)
3. Start JupyterLab with the following command:
   ```bash
   uv run jupyter lab --port=8888 --no-browser
   ```
4. Display the server URL with token for user to access
5. If port 8888 is in use, automatically try port 8889, 8890, etc.
6. Inform the user that the server is running in the background

## Additional Options

- To start with a specific notebook directory: `jupyter lab --notebook-dir=./notebooks`
- To allow remote connections: `jupyter lab --ip=0.0.0.0` (development only!)
- To set a custom token: `jupyter lab --token=<your_token>`

## Notes

- The server will continue running until stopped with Ctrl+C
- All notebooks will auto-save periodically
- Server logs will be displayed in the terminal
