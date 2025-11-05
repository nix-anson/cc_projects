---
description: Generate new Streamlit page
argument-hint: '<page_name>'
---

Create a new page file for the Streamlit multi-page app.

$1 is required and should be the page name (e.g., "settings", "analytics").

Generate a new page file at `pages/{next_number}_{page_name}.py` with the following template:

```python
import streamlit as st

st.set_page_config(
    page_title="$1",
    page_icon="📄",
    layout="wide"
)

# Check authentication
if not st.session_state.get('authentication_status'):
    st.warning("Please login to access this page")
    st.stop()

st.title("$1")

# Page content
st.write("Welcome to the $1 page!")

# Add your page implementation here
```

The file will be created with the next available page number (e.g., 04_settings.py).
