---
description: Generate reusable UI component
argument-hint: '<component_name>'
---

Create a new reusable UI component in the `app/components/` directory.

$1 is required and should be the component name (e.g., "sidebar_filters", "data_table").

Generate a new component file at `app/components/{component_name}.py` with the following template:

```python
"""$1 component."""
import streamlit as st
from typing import Any, Optional


def render_$1(
    data: Any,
    title: Optional[str] = None,
    **kwargs
) -> None:
    """
    Render the $1 component.

    Args:
        data: The data to display
        title: Optional title for the component
        **kwargs: Additional configuration options
    """
    if title:
        st.subheader(title)

    # Component implementation
    st.write(data)

    # Add your component logic here
```

The component can then be imported and used in your pages:
```python
from app.components.$1 import render_$1

render_$1(my_data, title="My Component")
```
