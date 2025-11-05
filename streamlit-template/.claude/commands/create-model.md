---
description: Generate SQLAlchemy model
argument-hint: '<model_name>'
---

Create a new SQLAlchemy model in the `app/models/` directory.

$1 is required and should be the model name in CamelCase (e.g., "Product", "UserProfile").

Generate a new model file at `app/models/{lowercase_model_name}.py` with the following template:

```python
"""$1 model."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class $1(Base):
    """$1 model."""

    __tablename__ = "${lowercase_model_name}s"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<$1(id={self.id}, name='{self.name}')>"
```

After creating the model:
1. Import it in `app/models/__init__.py`
2. Create a migration: `/db-migrate "Add $1 model"`
3. Apply the migration: `/db-upgrade`
