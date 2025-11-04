# Django Web Development Template

A comprehensive, production-ready Django project template with Claude Code integration. This template includes pre-configured commands, specialized AI agents, and automated workflows to accelerate Django development.

## What's Included

### Claude Code Configuration

- **10 Custom Slash Commands**: Quick access to common Django operations
- **5 Specialized Subagents**: AI assistants for security, optimization, testing, DRF, and migrations
- **3 Agent Skills**: Automated patterns for Django code generation and validation
- **CLAUDE.md**: Comprehensive Django context and best practices
- **Auto-formatting Hook**: Automatic Black formatting on file save

### Framework Setup

- Django 5.0+ with modern best practices
- Django REST Framework for API development
- PostgreSQL/SQLite database support
- Authentication (Session + JWT)
- Development tools (Debug Toolbar, django-extensions)
- Testing setup (pytest, coverage)
- Code quality tools (Black, flake8, isort)
- Production-ready configuration (gunicorn, whitenoise)

### Project Structure

```
django-template/
├── .claude/                       # Claude Code configuration
│   ├── commands/                  # 10 slash commands
│   │   ├── migrate.md
│   │   ├── makemigrations.md
│   │   ├── test.md
│   │   ├── runserver.md
│   │   ├── create-app.md
│   │   ├── create-model.md
│   │   ├── shell.md
│   │   ├── check.md
│   │   ├── collectstatic.md
│   │   └── showmigrations.md
│   ├── agents/                    # 5 specialized agents
│   │   ├── django-security.md
│   │   ├── orm-optimizer.md
│   │   ├── test-writer.md
│   │   ├── drf-expert.md
│   │   └── migration-helper.md
│   ├── skills/                    # 3 automated skills
│   │   ├── django-patterns/
│   │   ├── drf-serializer/
│   │   └── model-validator/
│   └── settings.json              # Claude Code settings
├── CLAUDE.md                      # Django context and conventions
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Django-specific gitignore
├── setup_instructions.md          # Detailed setup guide
└── README.md                      # This file
```

## Quick Start

### 1. Download Template

```bash
# Clone the repository
git clone <repo-url>

# Navigate to Django template
cd django-template

# Optional: Copy to your project directory
cp -r . /path/to/your/project
```

### 2. Set Up Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your settings (especially SECRET_KEY and DATABASE_URL)
```

### 3. Create Django Project

```bash
# Create project (replace 'myproject' with your name)
django-admin startproject myproject .

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Open in VSCode with Claude Code

```bash
# Open project in VSCode
code .

# Launch Claude Code and start developing!
```

## Using Claude Code Features

### Slash Commands

Quick access to common Django operations:

| Command | Description | Example |
|---------|-------------|---------|
| `/migrate` | Run database migrations | `/migrate` or `/migrate app_name` |
| `/makemigrations` | Create new migrations | `/makemigrations` or `/makemigrations app_name` |
| `/test` | Run test suite | `/test` or `/test app_name` |
| `/runserver` | Start development server | `/runserver` or `/runserver 8080` |
| `/create-app` | Create new Django app | `/create-app myapp` |
| `/create-model` | Generate model boilerplate | `/create-model myapp Product` |
| `/shell` | Open Django shell | `/shell` or `/shell --plain` |
| `/check` | Run system checks | `/check` or `/check --deploy` |
| `/collectstatic` | Collect static files | `/collectstatic --noinput` |
| `/showmigrations` | Display migration status | `/showmigrations` or `/showmigrations app_name` |

**Usage**: Type the command in Claude Code's input field and press Enter.

### Specialized Subagents

AI assistants that automatically activate based on context or can be explicitly invoked:

#### 1. Django Security Agent
**Triggers**: Security reviews, authentication code, permission handling
**Capabilities**:
- OWASP vulnerability detection (SQL injection, XSS, CSRF)
- Django security best practices enforcement
- Settings security validation
- Permission and authentication review

**Explicit use**: "Use the django-security agent to review my authentication views"

#### 2. ORM Optimizer Agent
**Triggers**: Slow queries, database-heavy code
**Capabilities**:
- N+1 query detection and fixes
- select_related() and prefetch_related() optimization
- Database index recommendations
- Query performance analysis

**Explicit use**: "Use the orm-optimizer agent to improve my product list view"

#### 3. Test Writer Agent
**Triggers**: New code without tests, test coverage mentions
**Capabilities**:
- Model, view, form, and API test generation
- Comprehensive test coverage patterns
- Edge case and error condition testing
- Test fixtures and mocking

**Explicit use**: "Use the test-writer agent to create tests for my Order model"

#### 4. DRF Expert Agent
**Triggers**: REST API development, serializer work
**Capabilities**:
- Serializer design and generation
- ViewSet and API view patterns
- Authentication and permissions setup
- API optimization and best practices

**Explicit use**: "Use the drf-expert agent to create a product API"

#### 5. Migration Helper Agent
**Triggers**: Complex migrations, migration conflicts
**Capabilities**:
- Complex migration creation (renaming, data transforms)
- Migration conflict resolution
- Zero-downtime migration strategies
- Migration troubleshooting

**Explicit use**: "Use the migration-helper agent to create a data migration"

### Automated Skills

Skills that automatically activate when appropriate:

#### Django Patterns Skill
**Auto-activates**: When refactoring or implementing architectural patterns
**Provides**: Custom managers, model mixins, service layer, view mixins, signal patterns

#### DRF Serializer Skill
**Auto-activates**: When creating or updating API serializers
**Provides**: Nested serializers, validation patterns, different read/write serializers

#### Model Validator Skill
**Auto-activates**: When implementing model validation
**Provides**: Field validators, clean() methods, Meta constraints, business rule validation

## Development Workflow

### Creating a New Feature

1. **Create app** (if needed):
   ```
   /create-app myapp
   ```

2. **Define models**:
   ```
   /create-model myapp Product
   ```
   Claude will generate model boilerplate with best practices

3. **Create and run migrations**:
   ```
   /makemigrations
   /migrate
   ```

4. **Generate tests**:
   Ask: "Generate tests for the Product model"
   (test-writer agent will activate)

5. **Create API** (if needed):
   Ask: "Create a REST API for products"
   (drf-expert agent will activate)

6. **Review security**:
   Ask: "Review security of my product views"
   (django-security agent will activate)

7. **Optimize performance**:
   Ask: "Optimize queries in my product list view"
   (orm-optimizer agent will activate)

### Running Tests

```bash
# All tests
/test

# Specific app
/test myapp

# With coverage
pytest --cov=myapp --cov-report=html
```

### Code Quality

The template includes automatic code formatting:
- **Black**: Auto-formats Python files on save
- **flake8**: Linting (run manually: `flake8`)
- **isort**: Import sorting (run manually: `isort .`)

## API Development

This template is optimized for API development with Django REST Framework:

### Creating an API Endpoint

1. **Define model and serializer**:
   ```python
   # Ask Claude: "Create a Product API with list, detail, create, update, delete"
   # drf-expert agent will generate complete ViewSet and serializers
   ```

2. **Configure URLs**:
   ```python
   # Claude will help add router configuration
   ```

3. **Test API**:
   ```python
   # test-writer agent can generate API tests
   ```

### API Features Included

- Token and JWT authentication
- Pagination (configurable page size)
- Filtering, searching, and ordering
- CORS support
- API documentation with drf-spectacular
- Rate limiting and throttling

## Security Best Practices

The django-security agent enforces:

- ✅ CSRF protection enabled
- ✅ SQL injection prevention
- ✅ XSS protection with auto-escaping
- ✅ Secure password hashing
- ✅ HTTPS redirect (production)
- ✅ Secure cookies (production)
- ✅ Proper permission checks
- ✅ Input validation

## Performance Optimization

The orm-optimizer agent helps with:

- ✅ N+1 query detection
- ✅ select_related() for foreign keys
- ✅ prefetch_related() for many-to-many
- ✅ Database indexing
- ✅ Queryset optimization
- ✅ Bulk operations
- ✅ Caching strategies

## Testing

Comprehensive testing setup included:

- **pytest** with Django plugin
- **factory_boy** for test data generation
- **coverage** for test coverage reports
- **Test patterns** via test-writer agent

Target: 80%+ test coverage

## Production Deployment

Before deploying:

1. **Update settings**:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Enable security settings (HTTPS redirect, secure cookies)

2. **Environment variables**:
   - Set `SECRET_KEY` (generate new one!)
   - Configure `DATABASE_URL`
   - Set production email backend

3. **Static files**:
   ```
   /collectstatic --noinput
   ```

4. **Migrations**:
   ```
   /migrate --noinput
   ```

5. **Use production server**:
   ```bash
   gunicorn myproject.wsgi:application
   ```

See `setup_instructions.md` for detailed deployment guide.

## Customization

### Adding More Commands

Create `.claude/commands/mycommand.md`:

```markdown
---
description: Description of what this command does
---

Command instructions here
```

### Creating Custom Agents

Create `.claude/agents/my-agent.md`:

```markdown
---
name: my-agent
description: When and how this agent should be used
tools: Read, Write, Bash
---

Agent system prompt and instructions
```

### Adding Skills

Create `.claude/skills/my-skill/SKILL.md`:

```markdown
---
name: my-skill
description: What this skill does and when to trigger it
---

Detailed skill instructions
```

## Resources

### Documentation
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Claude Code: https://docs.claude.com/en/docs/claude-code

### Community
- Django Forum: https://forum.djangoproject.com/
- Django Discord: https://discord.gg/django
- Stack Overflow: Tag `django`

### Learning
- Django Tutorial: https://docs.djangoproject.com/en/stable/intro/tutorial01/
- DRF Tutorial: https://www.django-rest-framework.org/tutorial/1-serialization/
- Two Scoops of Django: https://www.feldroy.com/books/two-scoops-of-django-3-x

## Troubleshooting

### Common Issues

**Q: Commands not working**
A: Ensure you're in the django-template directory when using Claude Code

**Q: Agents not activating**
A: Try explicitly invoking: "Use the [agent-name] agent to [task]"

**Q: Import errors**
A: Verify virtual environment is activated and dependencies are installed

**Q: Database errors**
A: Check `.env` file has correct `DATABASE_URL`

### Getting Help

1. Check `setup_instructions.md` for detailed guidance
2. Review `CLAUDE.md` for Django-specific conventions
3. Ask Claude Code directly - agents will help!
4. Refer to Django documentation

## Contributing

To improve this template:

1. Test changes thoroughly
2. Update documentation
3. Maintain consistency with Django best practices
4. Ensure all agents and commands work correctly

## License

[Your chosen license]

---

**Ready to build amazing Django applications with AI assistance? Start coding!**

For detailed setup instructions, see [setup_instructions.md](setup_instructions.md).

For Django conventions and patterns, see [CLAUDE.md](CLAUDE.md).
