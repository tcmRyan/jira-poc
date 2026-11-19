import os

import aiosql

from server.queries import CURSOR_KWARGS
from server.queries.authentications.protocol import AuthenticationQueries

SQL_PATH = os.path.join(os.path.dirname(__file__), 'authentications.sql')

queries: AuthenticationQueries = aiosql.from_path(SQL_PATH, 'psycopg2', kwargs=CURSOR_KWARGS)
