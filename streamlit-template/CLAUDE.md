# Streamlit Project Context

## Project Overview

This is a production-ready Streamlit application template built with modern Python best practices for 2025. The template provides a solid foundation for building interactive data applications with authentication, database integration, API communication, and comprehensive testing.

## Technology Stack

- **Framework**: Streamlit 1.51.0+
- **Python**: 3.13.9+
- **Database**: SQLAlchemy 2.0+ with Alembic migrations
- **Authentication**: streamlit-authenticator
- **API Client**: httpx (async/sync HTTP client)
- **Testing**: pytest with Streamlit AppTest
- **Visualization**: Plotly + Altair
- **Dev Tools**: Ruff, Black, isort, mypy, pre-commit

## Project Structure

```
streamlit-template/
├── app/
│   ├── core/              # Core application logic
│   │   ├── auth.py        # Authentication manager
│   │   ├── config.py      # Application settings
│   │   └── database.py    # Database connection and session
│   ├── models/            # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py        # User model example
│   ├── services/          # Business logic layer
│   │   ├── __init__.py
│   │   └── api_client.py  # API integration service
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py     # Common helper functions
│   └── components/        # Reusable UI components
│       ├── __init__.py
│       └── charts.py      # Chart components
├── pages/                 # Multi-page app pages
│   ├── 01_dashboard.py
│   ├── 02_data_upload.py
│   └── 03_analytics.py
├── tests/                 # Test files
│   ├── __init__.py
│   ├── conftest.py        # pytest fixtures
│   └── test_*.py
├── .streamlit/
│   ├── config.toml        # Streamlit configuration
│   └── secrets.toml       # Secrets (not committed)
├── main.py                # Application entry point
└── alembic/               # Database migrations
```

## Streamlit Best Practices (2025)

### State Management

**Session State Initialization**:
```python
# Always check before accessing
if 'key' not in st.session_state:
    st.session_state.key = 'default_value'
```

**Important Rules**:
- Session state is NOT persisted across server restarts
- Use callbacks (`on_change`, `on_click`) for widget interactions
- Callbacks execute BEFORE the app reruns from top
- Cannot modify widget state after instantiation
- URL navigation creates new session and resets state

**Common Patterns**:
```python
# Store lists for conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Use callbacks for form handling
def handle_submit():
    st.session_state.submitted = True

st.button("Submit", on_click=handle_submit)
```

### Caching Strategies

**Use `@st.cache_data` for**:
- Data transformations
- Loading DataFrames from files
- API queries that return serializable data
- Computations that return primitive types

```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)
```

**Use `@st.cache_resource` for**:
- Database connections
- ML models
- Unserializable objects
- Resources shared across sessions

```python
@st.cache_resource
def get_database_connection():
    return create_engine("postgresql://...")
```

**Performance Notes**:
- `@st.cache_data` creates copies (thread-safe)
- `@st.cache_resource` shares instances (no copying)
- Use `max_entries` and `ttl` to manage cache size
- For 100M+ rows, prefer `@st.cache_resource`

### Multi-Page Applications

**Preferred Method (2025)**: Use `st.Page` and `st.navigation`

```python
# main.py
import streamlit as st

# Define pages
home = st.Page("pages/home.py", title="Home", icon="🏠")
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon="📊")
settings = st.Page("pages/settings.py", title="Settings", icon="⚙️")

# Create navigation
pg = st.navigation([home, dashboard, settings])

# Run selected page
pg.run()
```

**Benefits**:
- Dynamic page control
- Role-based access
- Custom navigation positioning
- Grouped pages with headers

**Alternative**: Traditional `pages/` directory (automatic discovery)

### Data Visualization

**Chart Library Selection**:

- **Plotly**: Complex, interactive visualizations with many chart types
  - Best for: Scientific plots, 3D charts, advanced interactivity
  - Use `use_container_width=True` for responsive sizing

- **Altair**: Fast, declarative visualizations
  - Best for: Standard charts with interaction grammar
  - Generally faster than Plotly
  - Inherently responsive via Vega-Lite

- **Native Streamlit**: Simple, quick charts
  - Best for: Basic line/bar/area charts
  - Least customization

**Performance Considerations**:
- For 100,000+ rows: Performance becomes challenging
- Consider data aggregation
- Use WebGL in Plotly when available
- Altair generally faster than Plotly

**Responsive Sizing**:
```python
# Plotly
fig = go.Figure(...)
fig.update_layout(autosize=True)
st.plotly_chart(fig, use_container_width=True)

# Altair (automatic)
chart = alt.Chart(data).mark_bar()...
st.altair_chart(chart, use_container_width=True)
```

### Form Handling

**Streamlit Forms**:
```python
with st.form("user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, max_value=120)

    submitted = st.form_submit_button("Submit")

    if submitted:
        # Validation
        if not name:
            st.error("Name is required")
        elif not email or "@" not in email:
            st.error("Valid email required")
        else:
            # Process form
            st.success("Form submitted successfully!")
```

**Validation Pattern**:
- No built-in validation framework
- Create custom validation functions
- Display errors with `st.error()`
- Show success with `st.success()`

### File Upload/Download

**Upload Best Practices**:
```python
uploaded_file = st.file_uploader(
    "Choose a file",
    type=["csv", "xlsx", "json"],  # Restrict types
    accept_multiple_files=False,
    help="Max file size: 10MB"
)

if uploaded_file:
    # Validate size
    if uploaded_file.size > 10_000_000:
        st.error("File too large (max 10MB)")
    else:
        try:
            # Process based on type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                st.success("File processed successfully")
        except Exception as e:
            st.error(f"Error processing file: {e}")
```

**Security Considerations**:
- Files stored in memory only (cleared on rerun)
- Always validate file type AND size
- Check MIME type, not just extension
- Sanitize file content
- Never execute uploaded code

**Download Pattern**:
```python
# Prepare data
csv_data = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Data",
    data=csv_data,
    file_name="export.csv",
    mime="text/csv"
)
```

### Progress Indicators

**Progress Bar**:
```python
progress_bar = st.progress(0)
status_text = st.empty()

for i in range(100):
    progress_bar.progress(i + 1)
    status_text.text(f"Processing: {i+1}%")
    # Do work

status_text.text("Complete!")
```

**Spinner**:
```python
with st.spinner("Loading data..."):
    data = expensive_computation()
```

**Status Messages**:
- `st.success()` - Success feedback
- `st.error()` - Error messages
- `st.warning()` - Warnings
- `st.info()` - Informational messages

### Error Handling

**Pattern**:
```python
try:
    result = perform_operation()
    st.success("Operation completed successfully")
except ValueError as e:
    st.error(f"Invalid input: {e}")
except ConnectionError as e:
    st.error(f"Connection failed: {e}")
except Exception as e:
    st.error("An unexpected error occurred")
    if st.secrets.get("debug_mode", False):
        st.exception(e)  # Show traceback in debug mode
```

## Database Integration

### SQLAlchemy Connection

**Setup with Caching**:
```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st

@st.cache_resource
def get_engine():
    """Create and cache database engine."""
    return create_engine(
        st.secrets["database"]["url"],
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True  # Verify connections before use
    )

def get_session():
    """Get database session."""
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()
```

**Usage Pattern**:
```python
from app.core.database import get_session

# In your Streamlit app
session = get_session()
try:
    users = session.query(User).all()
    # Use data
finally:
    session.close()
```

### Database Migrations

**Alembic Commands**:
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current revision
alembic current

# View SQL without executing
alembic upgrade head --sql
```

**Best Practices**:
- Always review autogenerated migrations
- Run migrations before starting app
- Use Docker entrypoint for automatic migrations
- Test migrations on development data first

## Authentication

### streamlit-authenticator

**Setup**:
```python
# app/core/auth.py
import streamlit_authenticator as stauth

def get_authenticator():
    """Initialize authenticator from config."""
    config = {
        'credentials': st.secrets["auth"]["credentials"],
        'cookie': st.secrets["auth"]["cookie"],
        'pre-authorized': st.secrets["auth"].get("pre_authorized", [])
    }
    return stauth.Authenticate(**config)

# In main.py
authenticator = get_authenticator()
name, auth_status, username = authenticator.login()

if auth_status:
    # User is authenticated
    authenticator.logout("Logout", "sidebar")
    st.write(f"Welcome {name}")
elif auth_status == False:
    st.error("Username/password is incorrect")
elif auth_status == None:
    st.warning("Please enter your username and password")
```

**Session State Access**:
```python
# Access auth info
name = st.session_state.get('name')
auth_status = st.session_state.get('authentication_status')
username = st.session_state.get('username')
roles = st.session_state.get('roles')
```

**Multi-Page Support**:
- Pass authenticator via session state
- Check auth status on each page
- Redirect to login if not authenticated

## API Integration

### httpx Async Client

**Setup**:
```python
# app/services/api_client.py
import httpx
import streamlit as st
from typing import Dict, Any

class APIClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key

    async def get(self, endpoint: str, params: Dict = None) -> Dict[Any, Any]:
        """Make GET request with error handling."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
                response = await client.get(
                    f"{self.base_url}{endpoint}",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            st.error("API request timed out")
            raise
        except httpx.HTTPStatusError as e:
            st.error(f"HTTP error: {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            raise
```

**Usage with Caching**:
```python
@st.cache_data(ttl=300)
def fetch_api_data(endpoint: str):
    """Fetch and cache API data."""
    client = APIClient(st.secrets["api"]["base_url"], st.secrets["api"]["key"])

    # Run async function
    import asyncio
    return asyncio.run(client.get(endpoint))
```

**Error Handling**:
- Always use try/except for API calls
- Implement timeouts (default: 10 seconds)
- Show user-friendly error messages
- Log errors for debugging
- Consider retry logic with exponential backoff

## Testing

### Streamlit AppTest

**Basic Test Structure**:
```python
# tests/test_main.py
from streamlit.testing.v1 import AppTest
import pytest

def test_app_runs():
    """Test that app runs without errors."""
    at = AppTest.from_file("main.py")
    at.run()
    assert not at.exception

def test_login_form():
    """Test login form appears."""
    at = AppTest.from_file("main.py")
    at.run()

    # Check for login elements
    assert len(at.text_input) >= 2  # Username and password
    assert len(at.button) >= 1  # Login button
```

**Testing with Mocks**:
```python
# tests/conftest.py
import pytest
from unittest.mock import Mock
import streamlit as st

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear Streamlit cache between tests."""
    st.cache_data.clear()
    st.cache_resource.clear()

@pytest.fixture
def mock_database():
    """Mock database connection."""
    return Mock()

# tests/test_app.py
def test_with_mock(mock_database):
    """Test with mocked database."""
    at = AppTest.from_function(app_function)
    at.session_state.db = mock_database
    at.run()
    assert not at.exception
```

**Coverage Best Practices**:
- Aim for 80%+ coverage on business logic
- UI components may have lower coverage
- Test error handling paths
- Mock external dependencies
- Test authentication flows

## Code Quality

### Ruff Configuration

**pyproject.toml**:
```toml
[tool.ruff]
line-length = 88
target-version = "py313"
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "W",   # pycodestyle warnings
    "UP",  # pyupgrade
]
ignore = []

[tool.ruff.lint]
fixable = ["ALL"]
unfixable = []
```

**Usage**:
```bash
# Check code
ruff check .

# Fix automatically
ruff check --fix .

# Format code
ruff format .
```

### Type Checking

**mypy Configuration**:
```toml
[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
plugins = ["sqlalchemy.ext.mypy.plugin"]
```

**Type Hints Best Practices**:
```python
from typing import List, Dict, Optional, Any
import pandas as pd

def process_data(
    df: pd.DataFrame,
    columns: List[str],
    config: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """Process dataframe with type hints."""
    ...
```

### Pre-commit Hooks

**Setup**:
```bash
# Install
pre-commit install

# Run manually
pre-commit run --all-files
```

**Configuration** (.pre-commit-config.yaml):
- Ruff linting and formatting
- mypy type checking
- Runs automatically on git commit

## Deployment

### Environment Configuration

**Secrets Management**:
```toml
# .streamlit/secrets.toml (DO NOT COMMIT)
[database]
url = "postgresql://user:pass@localhost/db"

[api]
base_url = "https://api.example.com"
key = "secret-api-key"

[auth]
cookie_name = "auth_cookie"
cookie_key = "random-secret-key"
cookie_expiry_days = 30
```

**Access Secrets**:
```python
# Attribute notation
db_url = st.secrets.database.url

# Dict notation
api_key = st.secrets["api"]["key"]
```

**Production**:
- Use environment variables with `STREAMLIT_` prefix
- Store secrets in platform-specific secret managers
- Never commit `.streamlit/secrets.toml`

### Docker Deployment

**Dockerfile**:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run app
CMD streamlit run main.py \
    --server.port=${PORT:-8501} \
    --server.address=0.0.0.0 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=true
```

**Important Settings**:
- `--server.address=0.0.0.0` - Allow external connections
- `--server.enableCORS=false` - Disable CORS for production
- `--server.enableXsrfProtection=true` - Enable XSRF protection
- Use environment variable for dynamic port binding

## Common Patterns

### Page Navigation Guard

```python
# Check authentication on each page
if not st.session_state.get('authentication_status'):
    st.warning("Please login to access this page")
    st.stop()

# Proceed with page content
st.title("Protected Page")
```

### Data Loading Pattern

```python
@st.cache_data(ttl=600)
def load_data(source: str) -> pd.DataFrame:
    """Load data with caching."""
    with st.spinner(f"Loading data from {source}..."):
        df = pd.read_csv(source)
    return df

# Usage
try:
    df = load_data("data/file.csv")
    st.dataframe(df)
except FileNotFoundError:
    st.error("Data file not found")
except Exception as e:
    st.error(f"Error loading data: {e}")
```

### Async Operation Pattern

```python
import asyncio
from app.services.api_client import APIClient

async def fetch_multiple_endpoints():
    """Fetch data from multiple endpoints concurrently."""
    client = APIClient(base_url="https://api.example.com")

    # Concurrent requests
    results = await asyncio.gather(
        client.get("/endpoint1"),
        client.get("/endpoint2"),
        client.get("/endpoint3"),
        return_exceptions=True
    )

    return results

# In Streamlit app
with st.spinner("Fetching data..."):
    results = asyncio.run(fetch_multiple_endpoints())
```

## Development Workflow

### Local Development

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Setup pre-commit**: `pre-commit install`
3. **Configure secrets**: Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
4. **Run migrations**: `alembic upgrade head`
5. **Start app**: `streamlit run main.py`

### Code Quality Checks

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
mypy .

# Test
pytest --cov=app --cov-report=html

# Run all checks
./scripts/check_all.sh
```

### Creating New Components

**Page**:
```python
# pages/05_new_page.py
import streamlit as st

st.set_page_config(page_title="New Page", page_icon="📄")

# Check authentication
if not st.session_state.get('authentication_status'):
    st.warning("Please login to access this page")
    st.stop()

st.title("New Page")
# Page content...
```

**Component**:
```python
# app/components/new_component.py
import streamlit as st
import plotly.graph_objects as go

def render_custom_chart(data, title: str):
    """Render custom chart component."""
    fig = go.Figure(data=[...])
    fig.update_layout(title=title, autosize=True)
    st.plotly_chart(fig, use_container_width=True)
```

**Model**:
```python
# app/models/new_model.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class NewModel(Base):
    __tablename__ = "new_table"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## Security Best Practices

1. **Input Validation**: Always validate and sanitize user input
2. **Authentication**: Use secure password hashing (bcrypt)
3. **Secrets Management**: Never commit secrets, use environment variables
4. **API Security**: Use HTTPS, validate SSL certificates
5. **Database**: Use parameterized queries, prevent SQL injection
6. **File Uploads**: Validate types and sizes, sanitize filenames
7. **CORS**: Disable in production, enable XSRF protection
8. **Dependencies**: Keep packages updated, run security audits

## Performance Optimization

1. **Caching**: Use `@st.cache_data` and `@st.cache_resource` appropriately
2. **Data Loading**: Load data once, cache aggressively
3. **Large Datasets**: Consider pagination, aggregation, or sampling
4. **Database**: Use connection pooling, optimize queries
5. **API Calls**: Cache responses, use async for concurrent requests
6. **Visualization**: Aggregate data before plotting large datasets
7. **Session State**: Store only necessary data in session state

## Troubleshooting

### Common Issues

**Cache Not Clearing**:
```python
# Clear cache manually
st.cache_data.clear()
st.cache_resource.clear()
```

**Session State Lost**:
- Check if page navigation creates new session
- Ensure authenticator passed via session state
- Verify server hasn't restarted

**Database Connection Errors**:
- Check connection string
- Verify database is running
- Check pool settings
- Use `pool_pre_ping=True`

**API Timeouts**:
- Increase timeout value
- Check network connectivity
- Implement retry logic
- Use async for multiple requests

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [httpx Documentation](https://www.python-httpx.org)
- [pytest Documentation](https://docs.pytest.org)
- [Ruff Documentation](https://docs.astral.sh/ruff)
