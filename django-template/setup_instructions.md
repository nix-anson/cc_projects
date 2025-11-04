# Django Template Setup Instructions

This guide will help you set up a new Django project using this template.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- PostgreSQL (recommended) or SQLite for development
- Git
- VSCode with Claude Code extension

## Quick Start

### 1. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your settings
# At minimum, update:
# - SECRET_KEY (generate a new one)
# - DATABASE_URL (if using PostgreSQL)
# - DEBUG (True for development)
```

**Generate a new SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Create Django Project

```bash
# Create a new Django project (replace 'myproject' with your project name)
django-admin startproject myproject .

# The dot (.) at the end is important - it creates the project in the current directory
```

### 5. Configure Settings

Update `myproject/settings.py`:

```python
# At the top, add:
from decouple import config
from pathlib import Path

# Update SECRET_KEY:
SECRET_KEY = config('SECRET_KEY')

# Update DEBUG:
DEBUG = config('DEBUG', default=False, cast=bool)

# Update ALLOWED_HOSTS:
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Add installed apps:
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    'debug_toolbar',
    'django_extensions',

    # Your apps (add as you create them)
    # 'myapp',
]

# Add middleware:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'corsheaders.middleware.CorsMiddleware',  # For CORS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # For debug toolbar
]

# Database configuration (if using PostgreSQL):
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files configuration:
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration:
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# REST Framework configuration:
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# Crispy Forms configuration:
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Debug Toolbar configuration:
INTERNAL_IPS = ['127.0.0.1']

# CORS configuration (adjust as needed):
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
]
```

### 6. Set Up Database

```bash
# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### 7. Create Your First App

```bash
# Use the /create-app command in Claude Code, or:
python manage.py startapp myapp

# Add 'myapp' to INSTALLED_APPS in settings.py
```

### 8. Run Development Server

```bash
python manage.py runserver

# Or use the /runserver command in Claude Code
```

Access your project at: http://127.0.0.1:8000/
Admin panel at: http://127.0.0.1:8000/admin/

## Using Claude Code Features

This template includes pre-configured Claude Code features:

### Slash Commands

Available commands (use `/help` to see all):

- `/migrate` - Run database migrations
- `/makemigrations` - Create new migrations
- `/test` - Run tests
- `/runserver` - Start development server
- `/create-app <name>` - Create new Django app
- `/create-model <app> <model>` - Generate model boilerplate
- `/shell` - Open Django shell
- `/check` - Run system checks
- `/collectstatic` - Collect static files
- `/showmigrations` - Show migration status

### Subagents

Specialized AI assistants available:

- **django-security**: Security review and vulnerability detection
- **orm-optimizer**: Query optimization and performance tuning
- **test-writer**: Generate comprehensive tests
- **drf-expert**: Django REST Framework guidance
- **migration-helper**: Complex migration assistance

### Skills

Automatically activated patterns:

- **django-patterns**: Common Django design patterns
- **drf-serializer**: DRF serializer generation
- **model-validator**: Model validation patterns

## Project Structure

After setup, your project should look like:

```
project-root/
├── venv/                          # Virtual environment
├── myproject/                     # Django project directory
│   ├── __init__.py
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── myapp/                         # Your Django apps
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── static/                        # Static files (CSS, JS, images)
├── media/                         # User-uploaded files
├── templates/                     # HTML templates
├── .claude/                       # Claude Code configuration
│   ├── commands/
│   ├── agents/
│   ├── skills/
│   └── settings.json
├── .env                          # Environment variables (not committed)
├── .env.example                  # Environment template
├── .gitignore
├── requirements.txt              # Python dependencies
├── CLAUDE.md                     # Project context for Claude
└── README.md                     # Project documentation
```

## Development Workflow

### Creating a New App

1. Use `/create-app myapp` or `python manage.py startapp myapp`
2. Add app to `INSTALLED_APPS` in settings.py
3. Create models in `myapp/models.py`
4. Run `/makemigrations` and `/migrate`
5. Register models in `admin.py`
6. Create views, URLs, and templates

### Running Tests

```bash
# All tests
python manage.py test

# Specific app
python manage.py test myapp

# With coverage
pytest --cov=myapp
```

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports
isort .

# Run linter
flake8
```

### Creating API Endpoints

1. Define models
2. Create serializers (ask drf-expert agent)
3. Create viewsets
4. Configure URLs with routers
5. Test with Django REST Framework browsable API

## Production Deployment

Before deploying to production:

1. **Update settings.py**:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

2. **Set environment variables** on your hosting platform

3. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate --noinput
   ```

5. **Use production WSGI server** (gunicorn):
   ```bash
   gunicorn myproject.wsgi:application
   ```

6. **Set up HTTPS** with Let's Encrypt or your hosting provider

7. **Configure database backups**

8. **Set up monitoring and logging**

## Common Issues and Solutions

### Issue: ImportError for installed packages
**Solution**: Ensure virtual environment is activated and packages are installed

### Issue: Database connection errors
**Solution**: Check DATABASE_URL in .env file and ensure database server is running

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic` and check STATIC_ROOT configuration

### Issue: CSRF verification failed
**Solution**: Ensure CSRF middleware is enabled and CSRF token is included in forms

### Issue: Migration conflicts
**Solution**: Use `/showmigrations` to check status, resolve conflicts, or use `--merge`

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

## Getting Help

- Use Claude Code's agents for specific guidance
- Check CLAUDE.md for project-specific conventions
- Refer to Django documentation
- Ask in Django community forums

Happy coding with Django and Claude Code!
