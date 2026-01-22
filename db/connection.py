"""
Database connection setup (stub implementation).
"""
from contextlib import contextmanager


class MockSession:
    """Mock database session for when DB is not configured."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add(self, obj):
        """Mock add operation."""
        pass

    def commit(self):
        """Mock commit operation."""
        pass

    def query(self, *args, **kwargs):
        """Mock query operation."""
        return MockQuery()


class MockQuery:
    """Mock query result."""

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return []

    def first(self):
        return None


@contextmanager
def SessionLocal():
    """
    Provides a mock database session.
    Replace this with actual SQLAlchemy session if database is configured.
    """
    session = MockSession()
    try:
        yield session
    finally:
        pass
