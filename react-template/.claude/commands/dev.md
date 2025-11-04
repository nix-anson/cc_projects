---
description: Start Vite development server
argument-hint: [--host] [--port PORT] [--open]
allowed-tools: Bash(*)
---

Start the Vite development server for local React development with hot module replacement (HMR).

Arguments:
- $ARGUMENTS: All arguments passed to the dev command

Common usage patterns:
- `/dev` - Start server on default port (usually 5173)
- `/dev --host` - Expose server to network (accessible from other devices)
- `/dev --port 3000` - Start server on specific port
- `/dev --open` - Automatically open browser
- `/dev --host --port 3000` - Combine options

Execute: `npm run dev $ARGUMENTS`

The server will run with hot module replacement enabled. You can access it at:
- http://localhost:5173/ (or specified port)
- If using --host, accessible from other devices on your network at http://[YOUR_IP]:5173/

Features:
- **Hot Module Replacement (HMR)**: Changes reflect instantly without full reload
- **Fast Refresh**: React components update while preserving state
- **TypeScript Support**: Type errors shown in browser and terminal
- **Fast Startup**: Vite's native ESM dev server starts in milliseconds

Notes:
- Development server is optimized for speed, not production
- Environment variables from .env.development will be loaded
- Source maps are enabled for easy debugging
- Press Ctrl+C to stop the server

Common issues:
- "Port already in use" - Try a different port with --port flag
- "EACCES permission denied" - Check if port is restricted (use port > 1024)
- Network access blocked - Check firewall settings when using --host
