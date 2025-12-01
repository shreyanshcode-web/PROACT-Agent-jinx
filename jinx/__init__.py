"""PROACT Agent - Jinx"""

__version__ = "0.1.0"

# Initialize DB on import
try:
    from jinx.db.session import init_db
    init_db()
except Exception as e:
    print(f"Warning: DB initialization failed: {e}")
