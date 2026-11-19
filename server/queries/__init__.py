from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor

from server import app

# Rows come back as dicts so callers can read columns by name.
CURSOR_KWARGS = {'cursor_factory': RealDictCursor}


@contextmanager
def connection():
    """Open a connection for aiosql queries, commit on success and roll back on error."""
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        with conn:
            yield conn
    finally:
        conn.close()
