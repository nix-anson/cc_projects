# Streamlit Application Template

A production-ready Streamlit application template with authentication, database integration, API communication, and comprehensive testing. Optimized for use with Claude Code.

## Features

- 🔐 **Authentication** - User authentication with streamlit-authenticator
- 🗄️ **Database** - SQLAlchemy ORM with Alembic migrations
- 📊 **Visualization** - Plotly and Altair for interactive charts
- 🌐 **API Integration** - httpx for async HTTP requests
- ✅ **Testing** - pytest with Streamlit AppTest
- 🎨 **Code Quality** - Ruff, Black, mypy, pre-commit hooks
- 🐳 **Docker** - Development and production Docker setup
- 🤖 **Claude Code** - 12 commands, 6 agents, 4 skills

## Quick Start

### Prerequisites

- Python 3.13.9 or higher
- pip or poetry
- PostgreSQL (optional, SQLite works by default)

### Installation

1. **Clone or use this template**:
   ```bash
   # If using as a template, just open the folder
   cd streamlit-template
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure secrets**:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml with your credentials
   ```

4. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

5. **Run the application**:
   ```bash
   streamlit run main.py
   # Or use Claude Code: /run
   ```

Visit `http://localhost:8501`

## Claude Code Integration

This template is optimized for Claude Code with comprehensive configuration.

### Slash Commands

- `/run [port]` - Start development server
- `/test [path]` - Run tests with coverage
- `/lint [--fix]` - Check code quality
- `/format` - Format code with Ruff + Black
- `/typecheck [path]` - Run mypy type checking
- `/db-migrate "<message>"` - Create database migration
- `/db-upgrade [target]` - Apply migrations
- `/create-page <name>` - Generate new page
- `/create-component <name>` - Generate reusable component
- `/create-model <name>` - Generate SQLAlchemy model
- `/build [tag]` - Build Docker image
- `/check` - Run all quality checks

### Specialized Agents

- **streamlit-expert** - State management, caching, performance
- **data-viz-optimizer** - Chart selection and optimization
- **security-reviewer** - Security vulnerabilities and OWASP
- **database-architect** - SQLAlchemy models and queries
- **test-generator** - Test creation with AppTest
- **api-integrator** - API patterns and error handling

### Skills

- **streamlit-patterns** - Common UI patterns
- **caching-optimizer** - Performance optimization
- **auth-system** - Authentication and RBAC
- **database-operations** - Database patterns

## Project Structure

```
streamlit-template/
├── app/
│   ├── core/              # Core application logic
│   │   ├── auth.py        # Authentication
│   │   ├── config.py      # Settings
│   │   └── database.py    # Database connection
│   ├── models/            # SQLAlchemy models
│   ├── services/          # Business logic
│   ├── utils/             # Utilities
│   └── components/        # Reusable UI components
├── pages/                 # Multi-page app pages
├── tests/                 # Test files
├── .claude/               # Claude Code configuration
│   ├── commands/          # Slash commands
│   ├── agents/            # Specialized agents
│   ├── skills/            # Agent skills
│   └── settings.json
├── .streamlit/
│   ├── config.toml        # Streamlit config
│   └── secrets.toml       # Secrets (not committed)
├── main.py                # Entry point
├── requirements.txt       # Dependencies
├── pyproject.toml         # Tool configuration
└── docker-compose.yml     # Docker setup
```

## Development

### Running Tests

```bash
# All tests with coverage
pytest

# Specific test file
pytest tests/test_main.py

# With coverage report
pytest --cov=app --cov-report=html

# Or use Claude Code
/test
```

### Code Quality

```bash
# Lint
ruff check .

# Format
ruff format . && black . && isort .

# Type check
mypy .

# Run all checks
/check
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Or use Claude Code
/db-migrate "Add users table"
/db-upgrade
```

## Configuration

### Secrets

Edit `.streamlit/secrets.toml`:

```toml
[database]
url = "postgresql://user:pass@localhost/db"

[api]
base_url = "https://api.example.com"
key = "your-api-key"

[auth]
[auth.cookie]
name = "auth_cookie"
key = "random-signature-key"
expiry_days = 30

[auth.credentials]
# Add user credentials
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
DATABASE_URL=postgresql://user:pass@localhost/db
API_BASE_URL=https://api.example.com
API_KEY=your-api-key
```

## Docker

### Development

```bash
docker-compose up
```

Includes PostgreSQL database and auto-reload.

### Production

```bash
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
```

## Authentication

To enable authentication, uncomment the authentication code in `main.py` and configure credentials in `secrets.toml`.

Generate password hash:

```python
import streamlit_authenticator as stauth
passwords = ['password123']
hashed = stauth.Hasher(passwords).generate()
print(hashed[0])  # Use in secrets.toml
```

## Documentation

- **CLAUDE.md** - Development guidelines and best practices
- **setup_instructions.md** - Detailed setup instructions
- **Streamlit Docs** - https://docs.streamlit.io
- **SQLAlchemy Docs** - https://docs.sqlalchemy.org

## Testing

The template includes comprehensive test examples:

```python
from streamlit.testing.v1 import AppTest

def test_app_runs():
    at = AppTest.from_file("main.py")
    at.run()
    assert not at.exception
```

## Performance

- Uses `@st.cache_data` for data caching
- Uses `@st.cache_resource` for connections
- Connection pooling for database
- Async HTTP requests with httpx

## Security

- Password hashing with bcrypt
- Secrets management (never commit secrets.toml)
- SQL injection prevention (parameterized queries)
- XSRF protection enabled
- Input validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run `/check` to validate
5. Submit pull request

## Best Practices

See **CLAUDE.md** for comprehensive development guidelines including:
- Streamlit patterns
- State management
- Caching strategies
- Database operations
- API integration
- Testing patterns
- Security considerations

## Troubleshooting

### Database Connection Issues

```python
# Check connection string in secrets.toml
# Verify database is running
# Check pool settings
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Cache Issues

```python
# Clear Streamlit cache
st.cache_data.clear()
st.cache_resource.clear()
```

## License

MIT License - feel free to use for your projects

## Support

- Check CLAUDE.md for development guidelines
- Review skills in `.claude/skills/` for patterns
- Use Claude Code agents for assistance
