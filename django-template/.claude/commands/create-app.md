---
description: Create a new Django app with boilerplate
argument-hint: <app_name>
allowed-tools: Bash(*), Read(*), Write(*)
---

Create a new Django application with standard structure and boilerplate files.

Arguments:
- $1: Name of the app to create (required)

Execute the following steps:

1. Create the app using Django's startapp command:
   `python manage.py startapp $1`

2. Create the app directory if it doesn't exist in a standard location (apps/ or root)

3. After creating the app, help configure it:
   - Show the generated app structure
   - Add app to INSTALLED_APPS in settings.py (show the line to add)
   - Create urls.py in the new app with basic URL configuration
   - Create a basic view example
   - Update project's main urls.py to include the new app

4. Provide a checklist of next steps:
   - Define models in models.py
   - Create views in views.py
   - Add URL patterns in urls.py
   - Create templates directory
   - Register models in admin.py
   - Write tests in tests.py

Example app structure:
```
$1/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── urls.py (created)
├── tests.py
└── migrations/
    └── __init__.py
```

Best practices:
- Use singular or plural noun for app names (e.g., 'products', 'blog', 'users')
- Keep apps focused on single functionality
- Apps should be reusable across projects when possible
