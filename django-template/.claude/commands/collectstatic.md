---
description: Collect static files for production deployment
argument-hint: [--noinput] [--clear] [--link]
allowed-tools: Bash(*), Read(*)
---

Collect all static files from apps and configured locations into STATIC_ROOT for production serving.

Arguments:
- $ARGUMENTS: All arguments passed to collectstatic command

Common usage patterns:
- `/collectstatic` - Collect static files (with confirmation)
- `/collectstatic --noinput` - Collect without confirmation prompt
- `/collectstatic --clear` - Clear existing files before collecting
- `/collectstatic --link` - Create symlinks instead of copying (Unix only)

Execute: `python manage.py collectstatic $ARGUMENTS`

This command:
1. Gathers static files from:
   - Each app's static/ directory
   - Additional paths in STATICFILES_DIRS
   - Static files from installed packages

2. Copies them to STATIC_ROOT directory

3. Reports number of files copied/linked

Prerequisites:
- STATIC_ROOT must be configured in settings.py
- STATIC_URL must be set
- For production, configure web server to serve STATIC_ROOT

After collecting:
1. Verify STATIC_ROOT directory contains files
2. Check file count and total size
3. Ensure STATIC_URL is properly configured
4. Test static file access in production

Common issues:
- "STATIC_ROOT not configured" - Add STATIC_ROOT to settings.py
- "Permission denied" - Check directory write permissions
- "Files not found in production" - Configure web server correctly

Production setup:
```python
# settings.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# For WhiteNoise (recommended)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Best practices:
- Run before each production deployment
- Use --noinput in automated deployment scripts
- Use WhiteNoise for serving static files in production
- Enable gzip compression for static files
- Use CDN for static assets in production
