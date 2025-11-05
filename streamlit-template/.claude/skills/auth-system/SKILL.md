# Authentication System Skill

## Description

Authentication and session management patterns using streamlit-authenticator, including role-based access control.

Use this skill when implementing user authentication, managing sessions, or controlling access to application features.

## Patterns Included

1. **Basic Authentication Setup**
2. **Role-Based Access Control (RBAC)**
3. **Session Management**
4. **Multi-Page Authentication**
5. **Password Management**

## Pattern Reference

### 1. Basic Authentication Setup

```python
# app/core/auth.py
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def load_auth_config():
    """Load authentication configuration from secrets."""
    config = {
        'credentials': {
            'usernames': st.secrets["auth"]["credentials"]["usernames"].to_dict()
        },
        'cookie': {
            'name': st.secrets["auth"]["cookie"]["name"],
            'key': st.secrets["auth"]["cookie"]["key"],
            'expiry_days': st.secrets["auth"]["cookie"]["expiry_days"]
        },
        'pre-authorized': st.secrets["auth"].get("pre_authorized", {}).get("emails", [])
    }
    return config

def get_authenticator():
    """Initialize and return authenticator."""
    config = load_auth_config()
    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )

# main.py
from app.core.auth import get_authenticator

st.set_page_config(page_title="My App", page_icon="🔐")

# Initialize authenticator
authenticator = get_authenticator()

# Login widget
name, authentication_status, username = authenticator.login()

if authentication_status:
    # User authenticated
    st.sidebar.write(f"Welcome *{name}*")
    authenticator.logout("Logout", "sidebar")

    # Main app content
    st.title("Protected Application")
    st.write(f"Hello {name}!")

elif authentication_status == False:
    st.error("Username/password is incorrect")

elif authentication_status == None:
    st.warning("Please enter your username and password")
```

### 2. Role-Based Access Control

```python
# app/core/rbac.py
import streamlit as st
from functools import wraps
from typing import List

class Role:
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

# User roles configuration (in secrets.toml)
# [auth.roles]
# admin = ["admin_user"]
# user = ["user1", "user2"]
# guest = ["guest1"]

def get_user_role(username: str) -> str:
    """Get role for username."""
    roles = st.secrets["auth"].get("roles", {})

    for role, users in roles.items():
        if username in users:
            return role

    return Role.GUEST  # Default role

def has_permission(required_role: str) -> bool:
    """Check if current user has required role."""
    if not st.session_state.get('authentication_status'):
        return False

    username = st.session_state.get('username')
    user_role = get_user_role(username)

    # Role hierarchy: admin > user > guest
    role_hierarchy = {
        Role.ADMIN: 3,
        Role.USER: 2,
        Role.GUEST: 1
    }

    return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)

def require_role(required_role: str):
    """Decorator to require specific role."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not st.session_state.get('authentication_status'):
                st.warning("🔒 Please login to access this page")
                st.stop()

            if not has_permission(required_role):
                st.error(f"⛔ Access denied. Required role: {required_role}")
                st.stop()

            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage in pages
from app.core.rbac import require_role, Role

@require_role(Role.ADMIN)
def admin_dashboard():
    st.title("Admin Dashboard")
    st.write("Admin-only content")

@require_role(Role.USER)
def user_dashboard():
    st.title("User Dashboard")
    st.write("Content for authenticated users")

# Conditional UI based on role
if has_permission(Role.ADMIN):
    st.sidebar.button("Admin Settings")

if has_permission(Role.USER):
    st.sidebar.button("User Profile")
```

### 3. Session Management

```python
# app/core/session.py
import streamlit as st
from datetime import datetime, timedelta

class SessionManager:
    """Manage user sessions."""

    @staticmethod
    def initialize_session():
        """Initialize session state."""
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.login_time = None
            st.session_state.last_activity = None

    @staticmethod
    def start_session(username: str, name: str, role: str):
        """Start user session."""
        st.session_state.username = username
        st.session_state.name = name
        st.session_state.role = role
        st.session_state.login_time = datetime.now()
        st.session_state.last_activity = datetime.now()

    @staticmethod
    def update_activity():
        """Update last activity timestamp."""
        st.session_state.last_activity = datetime.now()

    @staticmethod
    def check_session_timeout(timeout_minutes: int = 30) -> bool:
        """Check if session has timed out."""
        if not st.session_state.get('authentication_status'):
            return False

        last_activity = st.session_state.get('last_activity')
        if not last_activity:
            return False

        timeout = timedelta(minutes=timeout_minutes)
        if datetime.now() - last_activity > timeout:
            return True

        return False

    @staticmethod
    def end_session():
        """End user session."""
        for key in ['username', 'name', 'role', 'login_time', 'last_activity', 'authentication_status']:
            if key in st.session_state:
                del st.session_state[key]

# Usage in main app
from app.core.session import SessionManager

SessionManager.initialize_session()

# Check timeout on every rerun
if SessionManager.check_session_timeout(timeout_minutes=30):
    st.warning("Session expired due to inactivity. Please login again.")
    SessionManager.end_session()
    st.rerun()

# Update activity on successful authentication
if st.session_state.get('authentication_status'):
    SessionManager.update_activity()

# Display session info
if st.sidebar.checkbox("Show Session Info"):
    st.sidebar.write(f"Logged in: {st.session_state.get('login_time')}")
    st.sidebar.write(f"Last activity: {st.session_state.get('last_activity')}")
```

### 4. Multi-Page Authentication

```python
# Create authentication guard for all pages
# app/core/guards.py
import streamlit as st

def require_auth():
    """Guard function for protected pages."""
    if not st.session_state.get('authentication_status'):
        st.warning("🔒 Please login to access this page")
        st.info("Return to home page to login")
        if st.button("Go to Login"):
            st.switch_page("main.py")
        st.stop()

# pages/01_dashboard.py
import streamlit as st
from app.core.guards import require_auth

st.set_page_config(page_title="Dashboard", page_icon="📊")

# Protect page
require_auth()

# Page content
st.title("Dashboard")
st.write(f"Welcome, {st.session_state['name']}!")

# pages/02_admin.py
import streamlit as st
from app.core.guards import require_auth
from app.core.rbac import has_permission, Role

st.set_page_config(page_title="Admin", page_icon="⚙️")

# Protect page
require_auth()

# Check admin role
if not has_permission(Role.ADMIN):
    st.error("⛔ Admin access required")
    st.stop()

# Admin page content
st.title("Admin Panel")
```

### 5. Password Management

```python
# app/core/password.py
import streamlit as st
import streamlit_authenticator as stauth
import re

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, "Password is strong"

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return stauth.Hasher([password]).generate()[0]

def create_password_reset_form():
    """Create password reset form."""
    with st.form("password_reset"):
        st.subheader("Reset Password")

        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        submitted = st.form_submit_button("Reset Password")

        if submitted:
            # Validate current password
            # (In production, verify against stored hash)

            # Validate new password
            is_strong, message = validate_password_strength(new_password)
            if not is_strong:
                st.error(message)
                return

            # Check passwords match
            if new_password != confirm_password:
                st.error("Passwords do not match")
                return

            # Hash new password
            new_hash = hash_password(new_password)

            st.success("Password reset successfully!")
            st.code(f"New password hash: {new_hash}")
            st.info("Update this hash in your secrets configuration")

# Usage in settings page
if st.session_state.get('authentication_status'):
    if st.sidebar.button("Change Password"):
        create_password_reset_form()
```

## Best Practices

1. **Never hardcode credentials** - use secrets management
2. **Hash passwords** with bcrypt or similar
3. **Implement session timeouts** for security
4. **Use HTTPS** in production
5. **Validate password strength** on registration/reset
6. **Implement role-based access** control
7. **Log authentication events** for security audit
8. **Handle session state** properly across pages
9. **Provide clear error messages** without revealing too much
10. **Test authentication flows** thoroughly
