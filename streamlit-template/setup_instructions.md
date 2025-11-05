# Setup Instructions

Complete step-by-step guide for setting up the Streamlit application template.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.13.9+** installed
- **Git** (if cloning from repository)
- **PostgreSQL** (optional, SQLite works by default)
- **VSCode** with Claude Code extension (recommended)

## Step 1: Get the Template

```bash
# Option A: Copy the template folder
cp -r streamlit-template my-project
cd my-project

# Option B: If in a git repository
git clone <repository-url>
cd my-project
```

## Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import streamlit; print(streamlit.__version__)"
```

## Step 4: Configure Secrets

### 4.1 Create Secrets File

```bash
# Copy example file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### 4.2 Generate Password Hashes

For authentication, generate password hashes:

```python
# Run in Python
import streamlit_authenticator as stauth

passwords = ['your_password_here']
hashed = stauth.Hasher(passwords).generate()
print(hashed[0])
```

### 4.3 Generate Cookie Key

```python
# Run in Python
import secrets
print(secrets.token_urlsafe(32))
```

### 4.4 Edit Secrets File

Edit `.streamlit/secrets.toml`:

```toml
[database]
url = "sqlite:///./app.db"  # Or PostgreSQL URL

[api]
base_url = "https://api.example.com"
key = "your-api-key-here"

[auth]
[auth.cookie]
name = "streamlit_auth_cookie"
key = "<generated-cookie-key-here>"  # From step 4.3
expiry_days = 30

[auth.credentials]
[auth.credentials.usernames]
[auth.credentials.usernames.admin]
email = "admin@example.com"
name = "Admin User"
password = "<generated-hash-here>"  # From step 4.2

[auth.roles]
admin = ["admin"]
```

## Step 5: Set Up Database (Optional)

### Using SQLite (Default)

No setup needed! The app will create `app.db` automatically.

### Using PostgreSQL

1. **Install PostgreSQL**:
   ```bash
   # macOS
   brew install postgresql

   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib

   # Windows: Download from postgresql.org
   ```

2. **Create Database**:
   ```bash
   # Start PostgreSQL
   psql postgres

   # In psql shell:
   CREATE DATABASE streamlit_db;
   CREATE USER streamlit_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE streamlit_db TO streamlit_user;
   \q
   ```

3. **Update Secrets**:
   ```toml
   [database]
   url = "postgresql://streamlit_user:your_password@localhost:5432/streamlit_db"
   ```

### Using Docker PostgreSQL

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=streamlit \
  -e POSTGRES_PASSWORD=streamlit \
  -e POSTGRES_DB=streamlit_db \
  -p 5432:5432 \
  postgres:16-alpine
```

## Step 6: Initialize Database

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head

# Or use Claude Code
/db-migrate "Initial schema"
/db-upgrade
```

## Step 7: Set Up Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

## Step 8: Configure Environment Variables (Optional)

```bash
# Copy example file
cp .env.example .env

# Edit .env with your values
nano .env  # or use your preferred editor
```

## Step 9: Run the Application

```bash
# Start the app
streamlit run main.py

# Or use Claude Code
/run

# Custom port
streamlit run main.py --server.port=8502
```

Visit `http://localhost:8501` in your browser.

## Step 10: Verify Setup

### Check Application

1. Open `http://localhost:8501`
2. Verify the home page loads
3. Check that no errors appear

### Run Tests

```bash
# Run all tests
pytest

# Or use Claude Code
/test
```

### Check Code Quality

```bash
# Lint
ruff check .

# Type check
mypy .

# Or run all checks
/check
```

## Using Docker (Alternative Setup)

If you prefer Docker:

### Development with Docker Compose

```bash
# Start services (app + database)
docker-compose up

# In another terminal, run migrations
docker-compose exec app alembic upgrade head
```

Visit `http://localhost:8501`

### Production Docker

```bash
# Build image
docker build -t streamlit-app .

# Run container
docker run -p 8501:8501 \
  -e DATABASE_URL="your-db-url" \
  streamlit-app
```

## Troubleshooting

### Issue: Module Not Found

```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Database Connection Failed

```bash
# Check PostgreSQL is running
pg_isready

# Verify connection string in secrets.toml
# Format: postgresql://user:password@host:port/database
```

### Issue: Pre-commit Hook Fails

```bash
# Update pre-commit hooks
pre-commit autoupdate

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

### Issue: Port Already in Use

```bash
# Use different port
streamlit run main.py --server.port=8502

# Or find and kill the process
# macOS/Linux:
lsof -i :8501
kill -9 <PID>

# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Issue: Import Errors with Streamlit

```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Restart application
```

## Next Steps

1. **Read CLAUDE.md** - Development guidelines and best practices
2. **Explore Examples** - Check `.claude/skills/` for pattern examples
3. **Create Your First Page** - Use `/create-page dashboard`
4. **Add Database Models** - Use `/create-model User`
5. **Enable Authentication** - Uncomment auth code in `main.py`

## Development Workflow

### Daily Development

1. Activate virtual environment
2. Start application: `streamlit run main.py`
3. Make changes
4. Run tests: `/test`
5. Check quality: `/check`
6. Commit changes

### Adding Features

1. Create feature branch
2. Implement feature
3. Add tests
4. Run `/check`
5. Commit and push

### Database Changes

1. Modify models in `app/models/`
2. Create migration: `/db-migrate "description"`
3. Review migration file
4. Apply migration: `/db-upgrade`
5. Test changes

## Tips

- **Use Claude Code commands** - They handle common operations efficiently
- **Check CLAUDE.md** - Comprehensive development guidelines
- **Use agents** - Let specialized agents help with complex tasks
- **Reference skills** - Pattern examples in `.claude/skills/`
- **Enable debug mode** - Set `echo=True` in database engine for SQL logging
- **Monitor performance** - Use Streamlit's built-in profiler

## Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Alembic Tutorial**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **httpx Documentation**: https://www.python-httpx.org
- **pytest Documentation**: https://docs.pytest.org

## Getting Help

1. Check **CLAUDE.md** for development patterns
2. Review **skills** in `.claude/skills/` for examples
3. Use **Claude Code agents** for assistance:
   - `/streamlit-expert` for Streamlit questions
   - `/database-architect` for database help
   - `/security-reviewer` for security review
   - `/test-generator` for test creation

## Configuration Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Secrets file configured
- [ ] Password hashes generated
- [ ] Database setup (SQLite or PostgreSQL)
- [ ] Migrations applied
- [ ] Pre-commit hooks installed
- [ ] Application runs successfully
- [ ] Tests pass
- [ ] Code quality checks pass

Congratulations! Your Streamlit application is ready for development.
