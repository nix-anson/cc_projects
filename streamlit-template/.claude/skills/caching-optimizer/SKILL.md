# Caching Optimizer Skill

## Description

Performance optimization strategies using Streamlit's caching mechanisms (`@st.cache_data` and `@st.cache_resource`).

Use this skill when optimizing app performance, reducing load times, or managing expensive computations.

## Caching Strategies

1. **Data Caching** (`@st.cache_data`)
2. **Resource Caching** (`@st.cache_resource`)
3. **Cache Invalidation**
4. **Conditional Caching**
5. **Cache Monitoring**

## When to Use Each Cache Type

### Use `@st.cache_data` for:
- Loading DataFrames from files
- API responses (serializable data)
- Data transformations
- Computations returning primitive types
- Any serializable data

### Use `@st.cache_resource` for:
- Database connections
- ML models
- Unserializable objects
- Shared global resources
- Very large datasets (100M+ rows)

## Pattern Reference

### 1. Basic Data Caching

```python
import streamlit as st
import pandas as pd
import time

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Load data with caching."""
    # Simulate expensive operation
    time.sleep(2)
    return pd.read_csv(file_path)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data_with_ttl(file_path: str) -> pd.DataFrame:
    """Load data with time-to-live."""
    return pd.read_csv(file_path)

@st.cache_data(max_entries=10)  # Keep only 10 most recent
def load_data_with_limit(file_path: str) -> pd.DataFrame:
    """Load data with cache size limit."""
    return pd.read_csv(file_path)

# Usage
df = load_data("data.csv")  # First call: slow
df = load_data("data.csv")  # Subsequent calls: instant
```

### 2. Resource Caching

```python
import streamlit as st
from sqlalchemy import create_engine
import pickle

@st.cache_resource
def get_database_connection():
    """Cache database connection."""
    return create_engine(
        st.secrets["database"]["url"],
        pool_size=5,
        max_overflow=10
    )

@st.cache_resource
def load_ml_model():
    """Cache ML model."""
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

@st.cache_resource
def initialize_api_client():
    """Cache API client."""
    from app.services.api_client import APIClient
    return APIClient(
        base_url=st.secrets["api"]["base_url"],
        api_key=st.secrets["api"]["key"]
    )

# Usage
engine = get_database_connection()
model = load_ml_model()
api_client = initialize_api_client()
```

### 3. Cache with Parameters

```python
import streamlit as st
import pandas as pd
from typing import List, Dict

@st.cache_data
def filter_data(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    """Cache filtered data based on parameters."""
    return df[df[column] == value]

@st.cache_data
def aggregate_data(
    df: pd.DataFrame,
    group_by: str,
    agg_func: str = "mean"
) -> pd.DataFrame:
    """Cache aggregated data."""
    if agg_func == "mean":
        return df.groupby(group_by).mean()
    elif agg_func == "sum":
        return df.groupby(group_by).sum()
    elif agg_func == "count":
        return df.groupby(group_by).count()

@st.cache_data(ttl=600)
def fetch_api_data(endpoint: str, params: Dict) -> Dict:
    """Cache API responses with parameters."""
    import httpx
    import asyncio

    async def fetch():
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, params=params)
            return response.json()

    return asyncio.run(fetch())

# Usage - different parameters = different cache entries
df = load_data("data.csv")
filtered1 = filter_data(df, "category", "A")  # Cached separately
filtered2 = filter_data(df, "category", "B")  # Different cache entry
```

### 4. Cache Invalidation

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_and_process_data(file_path: str) -> pd.DataFrame:
    """Load and process data with caching."""
    df = pd.read_csv(file_path)
    # Expensive processing
    df['processed'] = df['value'].apply(lambda x: x ** 2)
    return df

# Manual cache clearing
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.success("Cache cleared!")

# Clear specific function cache
if st.button("Clear Data Cache Only"):
    load_and_process_data.clear()
    st.success("Data cache cleared!")

# Conditional caching based on user preference
use_cache = st.checkbox("Enable caching", value=True)

if use_cache:
    df = load_and_process_data("data.csv")
else:
    # Bypass cache
    df = pd.read_csv("data.csv")
    df['processed'] = df['value'].apply(lambda x: x ** 2)
```

### 5. Hash Functions for Complex Types

```python
import streamlit as st
import pandas as pd
from typing import List

def hash_dataframe(df: pd.DataFrame) -> str:
    """Custom hash function for DataFrames."""
    return hash(df.to_json())

@st.cache_data(hash_funcs={pd.DataFrame: hash_dataframe})
def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Process DataFrame with custom hashing."""
    # Expensive processing
    return df.apply(lambda x: x ** 2)

# For mutable objects that can't be hashed
@st.cache_data
def process_list_data(data: List[int]) -> List[int]:
    """Process list data."""
    # Lists are converted to tuples automatically for hashing
    return [x ** 2 for x in data]
```

### 6. Lazy Loading with Caching

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_chunk(file_path: str, chunk_index: int, chunk_size: int = 1000) -> pd.DataFrame:
    """Load data chunk with caching."""
    skiprows = chunk_index * chunk_size
    return pd.read_csv(
        file_path,
        skiprows=range(1, skiprows + 1) if skiprows > 0 else None,
        nrows=chunk_size
    )

# Pagination with cached chunks
def display_paginated_data(file_path: str, total_rows: int, chunk_size: int = 1000):
    """Display paginated data with cached chunks."""
    total_pages = (total_rows + chunk_size - 1) // chunk_size

    page = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        value=1
    )

    # Load only requested chunk (cached)
    df_chunk = load_chunk(file_path, page - 1, chunk_size)

    st.dataframe(df_chunk, use_container_width=True)

    st.caption(f"Showing page {page} of {total_pages}")
```

### 7. Cache Performance Monitoring

```python
import streamlit as st
import time
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time

        # Store in session state for display
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = {}

        st.session_state.performance_metrics[func.__name__] = {
            'execution_time': execution_time,
            'cached': execution_time < 0.01  # Fast = likely from cache
        }

        return result

    return wrapper

@st.cache_data
@monitor_performance
def expensive_computation(n: int) -> int:
    """Expensive computation with performance monitoring."""
    time.sleep(2)  # Simulate expensive operation
    return sum(range(n))

# Usage
result = expensive_computation(1000000)

# Display performance metrics
if st.checkbox("Show Performance Metrics"):
    if 'performance_metrics' in st.session_state:
        for func_name, metrics in st.session_state.performance_metrics.items():
            st.write(f"**{func_name}**")
            st.write(f"- Execution time: {metrics['execution_time']:.4f}s")
            st.write(f"- From cache: {metrics['cached']}")
```

### 8. Background Cache Refresh

```python
import streamlit as st
import pandas as pd
import time
from datetime import datetime

@st.cache_data(ttl=60)  # Refresh every minute
def load_live_data() -> pd.DataFrame:
    """Load data with automatic background refresh."""
    # This function will be called every 60 seconds automatically
    current_time = datetime.now().strftime("%H:%M:%S")

    return pd.DataFrame({
        'timestamp': [current_time],
        'value': [time.time()]
    })

# Usage
df = load_live_data()
st.write(f"Data loaded at: {df['timestamp'].iloc[0]}")
st.write("This data refreshes automatically every minute")
```

### 9. Conditional Cache by User

```python
import streamlit as st
import pandas as pd

def get_cache_key() -> str:
    """Generate cache key based on user."""
    username = st.session_state.get('username', 'anonymous')
    return f"user_{username}"

@st.cache_data
def load_user_data(username: str) -> pd.DataFrame:
    """Load data specific to user (cached per user)."""
    # Different users get different cached data
    return pd.read_csv(f"data/{username}_data.csv")

# Usage - cache is per user
if st.session_state.get('authentication_status'):
    username = st.session_state['username']
    df = load_user_data(username)
```

### 10. Efficient Multi-Level Caching

```python
import streamlit as st
import pandas as pd

# Level 1: Cache raw data loading
@st.cache_data
def load_raw_data(file_path: str) -> pd.DataFrame:
    """Cache raw data loading."""
    return pd.read_csv(file_path)

# Level 2: Cache data cleaning
@st.cache_data
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cache data cleaning."""
    df = df.dropna()
    df = df.drop_duplicates()
    return df

# Level 3: Cache transformations
@st.cache_data
def transform_data(df: pd.DataFrame, operation: str) -> pd.DataFrame:
    """Cache data transformations."""
    if operation == "normalize":
        return (df - df.mean()) / df.std()
    elif operation == "log":
        return df.apply(lambda x: x.log() if pd.api.types.is_numeric_dtype(x) else x)
    return df

# Usage - each level is cached independently
raw = load_raw_data("data.csv")  # Cached
cleaned = clean_data(raw)  # Cached
transformed = transform_data(cleaned, "normalize")  # Cached

# Clearing level 1 doesn't affect level 2 or 3 unless they depend on new level 1 data
```

## Performance Best Practices

1. **Cache expensive operations**: I/O, API calls, computations
2. **Use appropriate cache type**: Data vs Resource
3. **Set TTL for time-sensitive data**: Use `ttl` parameter
4. **Limit cache size**: Use `max_entries` to prevent memory issues
5. **Clear cache when needed**: Manual or automatic invalidation
6. **Monitor cache performance**: Track hit rates and execution times
7. **Cache at the right level**: Don't cache too high or too low in the call stack
8. **Consider cache key uniqueness**: Parameters determine cache entries
9. **Be careful with mutable objects**: They can cause unexpected behavior
10. **Test cache behavior**: Ensure cache is working as expected

## Common Pitfalls

### Don't cache Streamlit UI elements
```python
# BAD - Don't do this
@st.cache_data
def create_ui():
    st.title("Title")  # UI elements should not be cached
    return "done"

# GOOD - Cache only data/computations
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

# UI creation happens outside cache
st.title("Title")
df = load_data()
```

### Don't cache functions with side effects
```python
# BAD - Side effects in cached function
@st.cache_data
def process_and_save(data):
    result = expensive_computation(data)
    save_to_database(result)  # Side effect!
    return result

# GOOD - Separate caching from side effects
@st.cache_data
def expensive_computation(data):
    return compute(data)

result = expensive_computation(data)
save_to_database(result)  # Side effect outside cache
```

## Cache Size Estimation

```python
import sys
import streamlit as st

def estimate_cache_size(obj):
    """Estimate object size in memory."""
    size_bytes = sys.getsizeof(obj)
    size_mb = size_bytes / (1024 * 1024)
    return size_mb

# Monitor cache usage
if st.checkbox("Show Cache Info"):
    st.write("### Cache Statistics")

    # Estimate data sizes
    df = load_data("data.csv")
    size = estimate_cache_size(df)

    st.write(f"DataFrame size: {size:.2f} MB")
    st.write(f"Shape: {df.shape}")
```
