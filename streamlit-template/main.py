"""
Streamlit Application Entry Point

This is the main entry point for the Streamlit application.
It handles authentication and navigation.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Streamlit App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.authentication_status = False

# Title
st.title("🚀 Streamlit Application")

# Welcome message
st.markdown("""
Welcome to your production-ready Streamlit application!

This template includes:
- 🔐 Authentication with streamlit-authenticator
- 🗄️ Database integration with SQLAlchemy
- 📊 Data visualization with Plotly and Altair
- 🌐 API integration with httpx
- ✅ Testing with pytest
- 🎨 Code quality with Ruff and Black

## Getting Started

1. **Setup**: Follow the setup instructions in `setup_instructions.md`
2. **Configure**: Update `.streamlit/secrets.toml` with your credentials
3. **Run**: Use `/run` command or `streamlit run main.py`

## Available Pages

Navigate using the sidebar to access different features of the application.

## Authentication

To enable authentication, uncomment the authentication code below and configure
your credentials in `.streamlit/secrets.toml`.
""")

# Show authentication status
if st.session_state.get('authentication_status'):
    st.success(f"✅ Logged in as: {st.session_state.get('name')}")
else:
    st.info("👋 This is a demo template. Authentication is disabled by default.")

# Quick start section
with st.expander("📚 Quick Start Guide"):
    st.markdown("""
    ### Claude Code Commands

    - `/run` - Start the development server
    - `/test` - Run tests with coverage
    - `/lint` - Check code quality
    - `/format` - Format code
    - `/typecheck` - Run type checking
    - `/check` - Run all quality checks

    ### Creating Components

    - `/create-page <name>` - Create a new page
    - `/create-component <name>` - Create a reusable component
    - `/create-model <name>` - Create a database model

    ### Database Operations

    - `/db-migrate "<message>"` - Create migration
    - `/db-upgrade` - Apply migrations
    """)

# Example metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Template Version", "1.0.0")
with col2:
    st.metric("Python", "3.13+")
with col3:
    st.metric("Streamlit", "1.51.0+")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | See CLAUDE.md for development guidelines")

# Authentication code (commented out by default)
"""
# Uncomment to enable authentication:

from app.core.auth import get_authenticator

authenticator = get_authenticator()
name, authentication_status, username = authenticator.login()

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Welcome *{name}*")

    # Main app content here
    st.title("Protected Content")
    st.write("This content is only visible to authenticated users")

elif authentication_status == False:
    st.error("Username/password is incorrect")

elif authentication_status == None:
    st.warning("Please enter your username and password")
"""
