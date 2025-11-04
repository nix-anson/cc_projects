# Django Project - Claude Code Configuration

## Project Type
Django web application framework (Python-based)

## Django Version
This template is configured for Django 5.x (latest stable)

## Project Structure and Architecture

### MVT Pattern (Model-View-Template)
Django follows the MVT architectural pattern:
- **Models**: Define database structure and business logic
- **Views**: Handle request/response logic and data processing
- **Templates**: Render HTML with Django template language
- **URLs**: Map URL patterns to views

### Standard Django Project Structure
```
project_name/
├── manage.py                    # Django management script
├── project_name/                # Project configuration directory
│   ├── __init__.py
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Root URL configuration
│   ├── asgi.py                 # ASGI server entry
│   └── wsgi.py                 # WSGI server entry
├── apps/                        # Django applications
│   ├── app_name/
│   │   ├── migrations/         # Database migrations
│   │   ├── __init__.py
│   │   ├── admin.py           # Django admin configuration
│   │   ├── apps.py            # App configuration
│   │   ├── models.py          # Database models
│   │   ├── views.py           # View functions/classes
│   │   ├── urls.py            # App-specific URLs
│   │   ├── forms.py           # Django forms
│   │   ├── serializers.py     # DRF serializers (if using REST)
│   │   └── tests.py           # Test cases
├── templates/                   # HTML templates
├── static/                      # Static files (CSS, JS, images)
├── media/                       # User-uploaded files
└── requirements.txt            # Python dependencies
```

## Common Django Commands

### Development Server
- `python manage.py runserver` - Start development server (port 8000)
- `python manage.py runserver 0.0.0.0:8000` - Accessible from network

### Database Operations
- `python manage.py makemigrations` - Create new migrations from model changes
- `python manage.py migrate` - Apply migrations to database
- `python manage.py showmigrations` - List migration status
- `python manage.py sqlmigrate app_name 0001` - Show SQL for migration
- `python manage.py dbshell` - Open database shell

### Application Management
- `python manage.py startapp app_name` - Create new Django app
- `python manage.py check` - Check for project issues
- `python manage.py shell` - Open Django interactive shell
- `python manage.py shell_plus` - Enhanced shell (requires django-extensions)

### User Management
- `python manage.py createsuperuser` - Create admin user
- `python manage.py changepassword username` - Change user password

### Testing
- `python manage.py test` - Run all tests
- `python manage.py test app_name` - Test specific app
- `python manage.py test app_name.tests.TestClass` - Test specific class
- `python manage.py test --keepdb` - Preserve test database between runs

### Static Files
- `python manage.py collectstatic` - Collect static files for production
- `python manage.py findstatic filename` - Find static file location

### Other Utilities
- `python manage.py dumpdata` - Export database data
- `python manage.py loaddata fixture.json` - Load fixture data
- `python manage.py showurls` - List all URL patterns (requires django-extensions)

## Code Style and Conventions

### Python/Django Style
- Follow PEP 8 for Python code style
- Use 4 spaces for indentation (Python standard)
- Maximum line length: 88 characters (Black formatter default) or 79 (PEP 8)
- Use descriptive variable and function names in snake_case
- Class names in PascalCase
- Constants in UPPER_SNAKE_CASE

### Model Conventions
- Use singular names for models: `User`, `Product`, `Order`
- Define `__str__()` method for all models
- Use `related_name` for reverse relationships
- Order model fields logically: key fields first, then relationships, then metadata
- Add `class Meta` with ordering, verbose names, indexes
- Use Django's built-in field validators
- Prefer `blank=True` for optional fields (forms), `null=True` for database

Example:
```python
class Product(models.Model):
    # Key fields
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    # Relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    # Additional fields
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name
```

### View Conventions
- Prefer Class-Based Views (CBVs) for CRUD operations
- Use Function-Based Views (FBVs) for simple or unique logic
- Keep views thin - move business logic to models or services
- Use Django's generic views when possible
- Always validate and sanitize user input
- Return appropriate HTTP status codes

**CBV Example**:
```python
from django.views.generic import ListView, DetailView, CreateView

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 20
```

**FBV Example**:
```python
from django.shortcuts import render, get_object_or_404

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/detail.html', {'product': product})
```

### URL Patterns
- Use path() instead of deprecated url()
- Name all URL patterns for reverse lookups
- Use angle brackets for path converters: `<int:id>`, `<slug:slug>`
- Organize URLs by app with include()
- Use trailing slashes (Django convention)

```python
from django.urls import path, include

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='detail'),
]
```

### Template Conventions
- Use Django Template Language (DTL) for HTML rendering
- Keep templates in app-specific directories: `templates/app_name/`
- Use template inheritance with `base.html`
- Always escape user input (Django does this by default)
- Use `{% static %}` tag for static files
- Use `{% url %}` tag for URL generation

### Forms
- Create ModelForms for model-based forms
- Always validate forms with `form.is_valid()`
- Use Django's built-in validators
- Add custom validation with `clean_field()` methods
- Use crispy-forms for better form rendering

```python
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be positive')
        return price
```

## Django REST Framework (DRF) Patterns

### Serializers
- Use ModelSerializer for model-based APIs
- Define `fields` or `exclude` in Meta class
- Add custom validation with `validate_field()` methods
- Use nested serializers for relationships

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'created_at']
        read_only_fields = ['id', 'created_at']
```

### ViewSets
- Use ModelViewSet for full CRUD operations
- Use ReadOnlyModelViewSet for read-only APIs
- Override methods for custom behavior
- Use `@action` decorator for custom endpoints

```python
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
```

## Security Best Practices

### Essential Security Measures
1. **CSRF Protection**: Enabled by default, always use `{% csrf_token %}` in forms
2. **SQL Injection**: Use Django ORM, never raw SQL with string concatenation
3. **XSS Protection**: Django auto-escapes templates, use `|safe` cautiously
4. **Clickjacking**: Use `X-Frame-Options` middleware (enabled by default)
5. **HTTPS**: Always use HTTPS in production, set `SECURE_SSL_REDIRECT = True`
6. **Secret Key**: Never commit SECRET_KEY, use environment variables
7. **Debug Mode**: Set `DEBUG = False` in production
8. **Allowed Hosts**: Configure `ALLOWED_HOSTS` properly in production
9. **Passwords**: Use Django's password hashing (PBKDF2 by default)
10. **File Uploads**: Validate file types and sizes, use secure storage

### Settings Configuration
```python
# Development
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Production
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')  # Required!
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

### User Input Validation
- Always validate and sanitize user input
- Use Django forms and model validation
- Never trust client-side validation alone
- Use `get_object_or_404()` instead of direct queries
- Implement proper permission checks

## Database and ORM Best Practices

### Query Optimization
- Use `select_related()` for foreign key relationships (one-to-one, many-to-one)
- Use `prefetch_related()` for many-to-many and reverse foreign keys
- Use `only()` and `defer()` to limit retrieved fields
- Use `values()` and `values_list()` for specific field retrieval
- Avoid N+1 queries - always check query counts
- Use `annotate()` for aggregations
- Add database indexes for frequently queried fields

```python
# Bad - N+1 queries
products = Product.objects.all()
for product in products:
    print(product.category.name)  # Additional query each iteration

# Good - Single query with join
products = Product.objects.select_related('category').all()
for product in products:
    print(product.category.name)  # No additional queries
```

### Migrations
- Create migrations for all model changes
- Review migration files before applying
- Use data migrations for complex changes
- Never edit applied migrations directly
- Use `--fake` only when you know what you're doing
- Keep migrations small and focused
- Test migrations on staging before production

## Testing Strategy

### Test Structure
- Write tests for models, views, forms, and APIs
- Use Django's TestCase for database-dependent tests
- Use SimpleTestCase for tests without database
- Use TransactionTestCase for testing transactions
- Aim for high test coverage (80%+ is good)

### Test Organization
```python
from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            price=99.99
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 99.99)

    def test_string_representation(self):
        self.assertEqual(str(self.product), 'Test Product')
```

### Testing Commands
- `python manage.py test` - Run all tests
- `python manage.py test app_name` - Test specific app
- `python manage.py test --keepdb` - Reuse test database (faster)
- `python manage.py test --parallel` - Run tests in parallel
- Use `coverage` for test coverage reports

## Performance Considerations

### Caching
- Use Django's cache framework
- Cache expensive queries and computed values
- Use Redis or Memcached for production
- Cache template fragments for static content
- Use `@cache_page` decorator for view caching

### Database Optimization
- Add indexes for frequently filtered/ordered fields
- Use `bulk_create()` for multiple inserts
- Use `update()` for bulk updates instead of save()
- Use `iterator()` for large querysets
- Consider database connection pooling

### Static Files
- Use WhiteNoise for serving static files in production
- Enable gzip compression
- Use CDN for static assets
- Minimize and bundle CSS/JS files

## Environment Configuration

### Settings Organization
- Split settings into base, development, production
- Use environment variables for sensitive data
- Use python-decouple or django-environ
- Never commit sensitive data to version control

### Required Environment Variables
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgres://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Common Django Packages

### Development
- `django-debug-toolbar` - Debug panel for development
- `django-extensions` - Useful management commands
- `ipython` - Enhanced Python shell

### Production
- `gunicorn` - WSGI HTTP server
- `psycopg2` - PostgreSQL adapter
- `whitenoise` - Static file serving
- `python-decoenv` - Environment variable management

### APIs
- `djangorestframework` - REST API framework
- `django-cors-headers` - CORS handling
- `djangorestframework-simplejwt` - JWT authentication

### Other
- `pillow` - Image processing
- `celery` - Asynchronous task queue
- `django-crispy-forms` - Better form rendering
- `django-allauth` - Authentication system

## Documentation Links

### Official Django Documentation
- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Django Security: https://docs.djangoproject.com/en/stable/topics/security/
- Django Best Practices: https://docs.djangoproject.com/en/stable/misc/design-philosophies/

### Python Resources
- PEP 8 Style Guide: https://pep8.org/
- Python Type Hints: https://docs.python.org/3/library/typing.html

## Custom Commands and Agents

This template includes:
- **Slash Commands**: Quick access to common Django operations
- **Subagents**: Specialized AI assistants for Django development
- **Skills**: Automated patterns for Django code generation

Use `/help` to see available commands and `@` to invoke specific agents.

---

**Remember**: Django follows the "batteries included" philosophy. Use built-in features before adding third-party packages. Always prioritize security, especially when handling user data.
