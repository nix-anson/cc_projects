---
description: Build React app for production
argument-hint: [--mode MODE] [--base BASE]
allowed-tools: Bash(*)
---

Build the React application for production deployment with optimizations.

Arguments:
- $ARGUMENTS: All arguments passed to the build command

Common usage patterns:
- `/build` - Standard production build
- `/build --mode staging` - Build with staging environment variables
- `/build --mode production` - Explicitly specify production mode
- `/build --base /my-app/` - Set base public path for deployment

Execute: `npm run build $ARGUMENTS`

The build process will:
1. Run TypeScript type checking
2. Compile and bundle all source files
3. Minify JavaScript and CSS
4. Optimize assets (images, fonts)
5. Generate source maps
6. Output to `dist/` directory

Build Optimizations:
- **Code Splitting**: Automatically splits vendor and app code
- **Tree Shaking**: Removes unused code
- **Minification**: Reduces file sizes
- **Asset Optimization**: Compresses images and other assets
- **Hashing**: Adds content hashes to filenames for cache busting

Output Structure:
```
dist/
├── index.html
├── assets/
│   ├── index.[hash].js     # Main application bundle
│   ├── vendor.[hash].js    # Third-party dependencies
│   └── index.[hash].css    # Styles
└── vite.svg               # Static assets
```

Environment Variables:
- Uses `.env.production` by default
- Can override with `--mode` flag
- Only variables prefixed with `VITE_` are included in build

Next Steps:
- Preview build locally: `/preview`
- Deploy `dist/` directory to your hosting provider
- Serve with a static file server (nginx, Apache, Vercel, Netlify, etc.)

Notes:
- Build output is in `dist/` directory (gitignored)
- Delete dist/ before building if you encounter issues
- Check build size - warn if bundles are too large
- Verify all environment variables are set correctly

Common issues:
- "Type error" - Fix TypeScript errors before building
- "Module not found" - Check all imports are correct
- Large bundle size - Consider code splitting and lazy loading
- Missing environment variables - Check .env.production file
