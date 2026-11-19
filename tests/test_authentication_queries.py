"""Exercise authentications.sql through aiosql on an in-memory SQLite database.

The server package needs a full environment (Postgres, Redis, ngrok) to import, so the
SQL and protocol files are loaded straight from disk.
"""
import importlib.util
import inspect
import os
import sqlite3

import aiosql
import pytest

DOMAIN_DIR = os.path.join(os.path.dirname(__file__), '..', 'server', 'queries', 'authentications')
SQL_PATH = os.path.join(DOMAIN_DIR, 'authentications.sql')

INSTALL = dict(
    key='pythia-addon', client_key='client-1', shared_secret='secret', plugins_version='1.0',
    base_url='https://example.atlassian.net', product_type='jira', description='Atlassian JIRA',
    service_entitlement_number=None, event_type='installed', public_key='pk',
    server_version='100', installed_by='admin',
)


def load_protocol():
    spec = importlib.util.spec_from_file_location('protocol', os.path.join(DOMAIN_DIR, 'protocol.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.AuthenticationQueries


@pytest.fixture
def queries():
    return aiosql.from_path(SQL_PATH, 'sqlite3')


@pytest.fixture
def conn():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.execute('''CREATE TABLE authentications (
        id INTEGER PRIMARY KEY, "key" TEXT, "clientKey" TEXT, "sharedSecret" TEXT,
        "pluginsVersion" TEXT, "baseUrl" TEXT, "productType" TEXT, "description" TEXT,
        "serviceEntitlementNumber" TEXT, "eventType" TEXT, "publicKey" TEXT,
        "serverVersion" TEXT, "installedBy" TEXT)''')
    yield conn
    conn.close()


def test_installed_tenant_is_found_by_base_url(queries, conn):
    queries.insert_authentication(conn, **INSTALL)

    tenant = dict(queries.get_authentication_by_base_url(conn, base_url='https://example.atlassian.net'))

    assert tenant['key'] == 'pythia-addon'
    assert tenant['sharedSecret'] == 'secret'
    assert tenant['baseUrl'] == 'https://example.atlassian.net'
    assert tenant['installedBy'] == 'admin'


def test_unknown_base_url_returns_none(queries, conn):
    queries.insert_authentication(conn, **INSTALL)

    assert queries.get_authentication_by_base_url(conn, base_url='https://other.atlassian.net') is None


def test_uninstall_removes_only_that_client(queries, conn):
    queries.insert_authentication(conn, **INSTALL)
    queries.insert_authentication(conn, **dict(INSTALL, client_key='client-2', base_url='https://other.atlassian.net'))

    queries.delete_authentications_by_client_key(conn, client_key='client-1')

    assert queries.get_authentication_by_base_url(conn, base_url='https://example.atlassian.net') is None
    assert queries.get_authentication_by_base_url(conn, base_url='https://other.atlassian.net') is not None


def test_protocol_matches_sql_file(queries):
    protocol = load_protocol()
    declared = {name for name, _ in inspect.getmembers(protocol, inspect.isfunction) if not name.startswith('_')}

    assert declared == set(queries.available_queries)
    for name in declared:
        expected = set(inspect.signature(getattr(protocol, name)).parameters) - {'self', 'conn'}
        assert expected == set(getattr(queries, name).parameters)
