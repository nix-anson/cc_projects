---
description: Preview production build locally
argument-hint: [--port PORT] [--host]
allowed-tools: Bash(*)
---

Preview the production build locally before deployment to verify everything works correctly.

Arguments:
- $ARGUMENTS: All arguments passed to the preview command

Common usage patterns:
- `/preview` - Preview on default port (usually 4173)
- `/preview --port 3000` - Preview on specific port
- `/preview --host` - Make accessible from network

Execute: `npm run preview $ARGUMENTS`

Prerequisites:
- Must run `/build` first to generate production files
- Serves files from `dist/` directory

What This Does:
- Starts a local static file server
- Serves the production build exactly as it will be in deployment
- Tests that all assets load correctly
- Verifies routing and navigation work
- Checks that environment variables are correctly embedded

This is NOT:
- A development server (no HMR)
- A replacement for the dev server
- Suitable for actual production hosting

Usage Workflow:
1. Make changes to your code
2. Run `/build` to create production bundle
3. Run `/preview` to test the build
4. Verify everything works as expected
5. Deploy to production

Notes:
- Preview server uses the same output as production
- Press Ctrl+C to stop the preview server
- If you make code changes, you must rebuild before previewing
- Check browser console for any errors
- Test all routes and functionality thoroughly

Common issues:
- "Failed to load" - Run `/build` first
- "404 Not Found" - Check routing configuration for SPA
- "Port already in use" - Specify different port with --port
- Blank page - Check browser console for errors
