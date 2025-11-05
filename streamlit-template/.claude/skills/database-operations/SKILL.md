# Database Operations Skill

## Description

Database connection management, query patterns, and migrations using SQLAlchemy and Alembic.

Use this skill when implementing database operations, creating models, or managing schema changes.

## Patterns Included

1. **Connection Management**
2. **Query Patterns**
3. **Transaction Handling**
4. **Migration Management**
5. **Error Handling**

## Pattern Reference

### 1. Connection Management

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import streamlit as st
from contextlib import contextmanager

Base = declarative_base()

@st.cache_resource
def get_engine():
    """Create and cache database engine."""
    return create_engine(
        st.secrets["database"]["url"],
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections
        pool_recycle=3600,  # Recycle after 1 hour
        echo=False  # Set True for SQL logging
    )

@contextmanager
def get_session() -> Session:
    """Context manager for database sessions."""
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
from app.core.database import get_session

with get_session() as session:
    users = session.query(User).all()
```

### 2. Common Query Patterns

```python
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import and_, or_, func
from typing import List, Optional

# Get all
def get_all_users() -> List[User]:
    """Get all users."""
    with get_session() as session:
        return session.query(User).all()

# Get by ID
def get_user_by_id(user_id: int) -> Optional[User]:
    """Get user by ID."""
    with get_session() as session:
        return session.query(User).filter(User.id == user_id).first()

# Get with filter
def get_active_users() -> List[User]:
    """Get active users."""
    with get_session() as session:
        return session.query(User).filter(User.is_active == True).all()

# Complex filter
def search_users(search_term: str, is_active: bool = None) -> List[User]:
    """Search users by username or email."""
    with get_session() as session:
        query = session.query(User)

        # Add search filter
        if search_term:
            pattern = f"%{search_term}%"
            query = query.filter(
                or_(
                    User.username.ilike(pattern),
                    User.email.ilike(pattern)
                )
            )

        # Add active filter
        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        return query.limit(100).all()

# Eager loading (prevent N+1)
def get_users_with_posts() -> List[User]:
    """Get users with their posts (eager loaded)."""
    with get_session() as session:
        return session.query(User).options(
            joinedload(User.posts)  # Load posts in same query
        ).all()

# Pagination
def get_users_paginated(page: int = 1, per_page: int = 50) -> List[User]:
    """Get paginated users."""
    with get_session() as session:
        offset = (page - 1) * per_page
        return session.query(User)\
            .order_by(User.created_at.desc())\
            .limit(per_page)\
            .offset(offset)\
            .all()

# Aggregation
def get_user_stats():
    """Get user statistics."""
    with get_session() as session:
        return session.query(
            func.count(User.id).label('total'),
            func.count(User.id).filter(User.is_active == True).label('active'),
            func.max(User.created_at).label('latest')
        ).first()

# Create
def create_user(username: str, email: str, password_hash: str) -> User:
    """Create new user."""
    with get_session() as session:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        session.add(user)
        session.flush()  # Get ID before commit
        return user

# Update
def update_user(user_id: int, **kwargs) -> User:
    """Update user."""
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        for key, value in kwargs.items():
            setattr(user, key, value)

        session.flush()
        return user

# Delete
def delete_user(user_id: int):
    """Delete user."""
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)

# Bulk operations
def bulk_create_users(users_data: List[dict]):
    """Bulk insert users."""
    with get_session() as session:
        session.bulk_insert_mappings(User, users_data)
```

### 3. Transaction Handling

```python
def transfer_credits(from_user_id: int, to_user_id: int, amount: float):
    """Transfer credits between users (atomic transaction)."""
    with get_session() as session:
        try:
            # Get users
            from_user = session.query(User).filter(User.id == from_user_id).first()
            to_user = session.query(User).filter(User.id == to_user_id).first()

            if not from_user or not to_user:
                raise ValueError("User not found")

            if from_user.credits < amount:
                raise ValueError("Insufficient credits")

            # Perform transfer
            from_user.credits -= amount
            to_user.credits += amount

            # Create transaction records
            transaction = Transaction(
                from_user_id=from_user_id,
                to_user_id=to_user_id,
                amount=amount
            )
            session.add(transaction)

            # Commit happens automatically in context manager
            st.success("Transfer completed successfully")

        except Exception as e:
            # Rollback happens automatically in context manager
            st.error(f"Transfer failed: {str(e)}")
            raise
```

### 4. Migration Management

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add users table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View current revision
alembic current

# View SQL without executing
alembic upgrade head --sql
```

```python
# alembic/env.py configuration
from app.models import Base
import streamlit as st

# Get database URL from secrets
config.set_main_option('sqlalchemy.url', st.secrets["database"]["url"])

# Set target metadata for autogenerate
target_metadata = Base.metadata
```

```python
# Migration example: Add column
"""Add last_login column

Revision ID: abc123
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users',
        sa.Column('last_login', sa.DateTime(), nullable=True)
    )

def downgrade():
    op.drop_column('users', 'last_login')
```

### 5. Error Handling

```python
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
import streamlit as st

def safe_create_user(username: str, email: str, password_hash: str) -> Optional[User]:
    """Create user with comprehensive error handling."""
    try:
        with get_session() as session:
            user = User(
                username=username,
                email=email,
                password_hash=password_hash
            )
            session.add(user)
            session.flush()

            st.success(f"User '{username}' created successfully")
            return user

    except IntegrityError as e:
        # Duplicate username/email
        if 'username' in str(e):
            st.error("Username already exists")
        elif 'email' in str(e):
            st.error("Email already registered")
        else:
            st.error("Duplicate entry")
        return None

    except OperationalError as e:
        # Database connection issues
        st.error("Database connection failed. Please try again.")
        st.exception(e)  # Show details in dev mode
        return None

    except SQLAlchemyError as e:
        # Other database errors
        st.error(f"Database error: {str(e)}")
        return None

    except Exception as e:
        # Unexpected errors
        st.error(f"Unexpected error: {str(e)}")
        return None

# Usage with error display
if st.button("Create User"):
    user = safe_create_user(username, email, password_hash)
    if user:
        st.write(f"Created user with ID: {user.id}")
```

## Best Practices

1. **Always use context managers** for sessions
2. **Use parameterized queries** to prevent SQL injection
3. **Eager load relationships** to prevent N+1 queries
4. **Add indexes** for frequently queried columns
5. **Use transactions** for multi-step operations
6. **Handle errors gracefully** with user-friendly messages
7. **Review autogenerated migrations** before applying
8. **Use connection pooling** for performance
9. **Set appropriate pool sizes** based on load
10. **Test migrations** on development data first
