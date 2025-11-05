# Streamlit Patterns Skill

## Description

Common UI patterns for Streamlit applications including forms, file handling, progress indicators, and user feedback.

Use this skill when implementing standard Streamlit UI patterns, handling user input, or creating interactive components.

## Patterns Included

1. **Form Validation**
2. **File Upload/Download**
3. **Progress Indicators**
4. **Error Handling**
5. **Data Display**
6. **Navigation Guards**

## Usage

Reference these patterns when:
- Creating forms with validation
- Implementing file upload features
- Showing progress for long operations
- Handling errors gracefully
- Displaying data to users
- Protecting routes with authentication

## Pattern Reference

### 1. Form with Validation

```python
import streamlit as st
import re

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    return True, "Password is strong"

# Form implementation
with st.form("registration_form"):
    st.subheader("User Registration")

    username = st.text_input("Username", max_chars=50)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    submitted = st.form_submit_button("Register")

    if submitted:
        # Validation
        errors = []

        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters")

        if not email or not validate_email(email):
            errors.append("Please enter a valid email address")

        is_valid_password, password_message = validate_password(password)
        if not is_valid_password:
            errors.append(password_message)

        if password != confirm_password:
            errors.append("Passwords do not match")

        # Display results
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.success("Registration successful!")
            # Process registration...
```

### 2. File Upload with Validation

```python
import streamlit as st
import pandas as pd
from typing import Optional

ALLOWED_TYPES = ['csv', 'xlsx', 'json']
MAX_FILE_SIZE = 10_000_000  # 10MB

def validate_file(uploaded_file) -> tuple[bool, Optional[str]]:
    """Validate uploaded file."""
    if uploaded_file is None:
        return False, "No file uploaded"

    # Check file size
    if uploaded_file.size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size: {MAX_FILE_SIZE / 1_000_000}MB"

    # Check file type
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension not in ALLOWED_TYPES:
        return False, f"Invalid file type. Allowed: {', '.join(ALLOWED_TYPES)}"

    return True, None

def process_uploaded_file(uploaded_file):
    """Process uploaded file based on type."""
    file_extension = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_extension == 'csv':
            return pd.read_csv(uploaded_file)
        elif file_extension == 'xlsx':
            return pd.read_excel(uploaded_file)
        elif file_extension == 'json':
            return pd.read_json(uploaded_file)
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

# File upload implementation
st.subheader("Upload Data File")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=ALLOWED_TYPES,
    help=f"Supported formats: {', '.join(ALLOWED_TYPES)}. Max size: {MAX_FILE_SIZE / 1_000_000}MB"
)

if uploaded_file:
    # Validate
    is_valid, error_message = validate_file(uploaded_file)

    if not is_valid:
        st.error(error_message)
    else:
        try:
            with st.spinner("Processing file..."):
                df = process_uploaded_file(uploaded_file)

            st.success(f"File uploaded successfully! Loaded {len(df)} rows.")

            # Display preview
            st.subheader("Data Preview")
            st.dataframe(df.head(10))

            # File info
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Rows", len(df))
            col2.metric("Total Columns", len(df.columns))
            col3.metric("File Size", f"{uploaded_file.size / 1024:.2f} KB")

        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

# Download processed data
if uploaded_file and 'df' in locals():
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Processed Data",
        data=csv,
        file_name="processed_data.csv",
        mime="text/csv"
    )
```

### 3. Progress Indicators

```python
import streamlit as st
import time
from typing import List, Callable

# Simple progress bar
def long_running_task_with_progress():
    """Task with progress bar."""
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(100):
        # Update progress
        progress = (i + 1) / 100
        progress_bar.progress(progress)
        status_text.text(f"Processing: {i + 1}%")

        # Simulate work
        time.sleep(0.05)

    status_text.text("Complete!")
    progress_bar.empty()

# Spinner for indeterminate progress
def fetch_data_with_spinner():
    """Task with spinner."""
    with st.spinner("Loading data from API..."):
        time.sleep(3)  # Simulate API call
        data = {"status": "success", "records": 100}

    st.success("Data loaded successfully!")
    return data

# Multi-step progress
def multi_step_process():
    """Process with multiple steps."""
    steps = [
        ("Validating input", lambda: time.sleep(1)),
        ("Processing data", lambda: time.sleep(2)),
        ("Generating report", lambda: time.sleep(1.5)),
        ("Saving results", lambda: time.sleep(0.5)),
    ]

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, (step_name, step_func) in enumerate(steps):
        status_text.text(f"Step {i + 1}/{len(steps)}: {step_name}")
        step_func()

        progress = (i + 1) / len(steps)
        progress_bar.progress(progress)

    status_text.text("All steps completed!")
    st.balloons()  # Celebration!

# Usage
if st.button("Run Task with Progress"):
    long_running_task_with_progress()

if st.button("Fetch Data"):
    data = fetch_data_with_spinner()
    st.json(data)

if st.button("Run Multi-Step Process"):
    multi_step_process()
```

### 4. Error Handling and User Feedback

```python
import streamlit as st
from typing import Optional

def safe_operation(value: str) -> tuple[bool, Optional[str], Optional[dict]]:
    """
    Safely perform operation with comprehensive error handling.

    Returns:
        (success, error_message, result)
    """
    try:
        # Validation
        if not value:
            return False, "Value cannot be empty", None

        if not value.isdigit():
            return False, "Value must be a number", None

        num = int(value)
        if num < 0:
            return False, "Value must be positive", None

        # Perform operation
        result = {"value": num, "squared": num ** 2, "cubed": num ** 3}
        return True, None, result

    except ValueError as e:
        return False, f"Invalid value: {str(e)}", None
    except Exception as e:
        return False, f"Unexpected error: {str(e)}", None

# Implementation with feedback
st.subheader("Error Handling Example")

user_input = st.text_input("Enter a positive number")

if st.button("Process"):
    if user_input:
        success, error, result = safe_operation(user_input)

        if success:
            st.success("Operation completed successfully!")
            st.json(result)
        else:
            st.error(error)
    else:
        st.warning("Please enter a value")

# Status messages
if st.button("Show Info"):
    st.info("This is an informational message")

if st.button("Show Warning"):
    st.warning("This is a warning message")

if st.button("Show Error"):
    st.error("This is an error message")

if st.button("Show Success"):
    st.success("This is a success message")

# Exception display (development only)
if st.checkbox("Show exception details (dev mode)"):
    try:
        # Intentional error
        result = 1 / 0
    except Exception as e:
        st.exception(e)
```

### 5. Data Display Patterns

```python
import streamlit as st
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame({
    'product': ['A', 'B', 'C', 'D', 'E'],
    'sales': [120, 250, 180, 300, 95],
    'profit': [30, 75, 45, 90, 20],
    'category': ['Electronics', 'Clothing', 'Electronics', 'Furniture', 'Clothing']
})

# Dataframe with configuration
st.subheader("Interactive Dataframe")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "sales": st.column_config.NumberColumn(
            "Sales ($)",
            format="$%d"
        ),
        "profit": st.column_config.ProgressColumn(
            "Profit Margin",
            format="$%d",
            min_value=0,
            max_value=100
        )
    }
)

# Metrics in columns
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${df['sales'].sum():,}",
    delta="+12%"
)
col2.metric(
    "Total Profit",
    f"${df['profit'].sum():,}",
    delta="-3%",
    delta_color="inverse"
)
col3.metric(
    "Avg Sales",
    f"${df['sales'].mean():.0f}"
)
col4.metric(
    "Products",
    len(df)
)

# Expandable sections
with st.expander("View Detailed Statistics"):
    st.write(df.describe())

# Tabs for organization
tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Export"])

with tab1:
    st.write("Overview content")

with tab2:
    st.write("Detailed content")

with tab3:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "data.csv", "text/csv")
```

### 6. Authentication Guard

```python
import streamlit as st
from functools import wraps

def require_authentication(func):
    """Decorator to require authentication for pages."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authentication_status'):
            st.warning("🔒 Please login to access this page")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def require_role(required_role: str):
    """Decorator to require specific role."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not st.session_state.get('authentication_status'):
                st.warning("🔒 Please login to access this page")
                st.stop()

            user_role = st.session_state.get('role')
            if user_role != required_role:
                st.error(f"⛔ Access denied. Required role: {required_role}")
                st.stop()

            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage in pages
@require_authentication
def protected_page():
    """Page that requires authentication."""
    st.title("Protected Page")
    st.write(f"Welcome, {st.session_state.get('name')}!")

@require_role('admin')
def admin_page():
    """Page that requires admin role."""
    st.title("Admin Dashboard")
    st.write("Admin-only content")

# Alternative inline guard
def page_with_guard():
    """Page with inline authentication guard."""
    # Check authentication
    if not st.session_state.get('authentication_status'):
        st.warning("🔒 Please login to access this page")
        st.stop()

    # Check role
    if st.session_state.get('role') not in ['admin', 'moderator']:
        st.error("⛔ Insufficient permissions")
        st.stop()

    # Page content
    st.title("Protected Content")
    st.write("Content for authenticated users with appropriate roles")
```

## Best Practices

1. **Always validate user input** before processing
2. **Provide clear error messages** that help users fix issues
3. **Show progress** for long-running operations
4. **Handle errors gracefully** without crashing the app
5. **Use appropriate feedback** (success, error, warning, info)
6. **Validate file uploads** (type, size, content)
7. **Protect routes** with authentication guards
8. **Use caching** for expensive operations
9. **Organize content** with columns, tabs, and expanders
10. **Test edge cases** and error conditions
