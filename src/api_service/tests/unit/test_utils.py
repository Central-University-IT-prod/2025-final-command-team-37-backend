from core.utils import is_valid_postgres_uri


def test_is_valid_postgres_uri():
    valid_uri_values = [
        "postgresql://user:password@localhost:5432/dbname",
        "postgresql+psycopg2://user:password@localhost:5432/dbname",
        "postgresql+asyncpg://user:password@localhost:5432/dbname",
        "postgresql+pg8000://user:password@localhost:5432/dbname"
        "postgresql+psycopg2cffi://user:password@localhost:5432/dbname"
    ]

    for uri in valid_uri_values:
        assert is_valid_postgres_uri(uri) is True

    invalid_uri_values = [
        "mysql://user:password@localhost:5432/dbname",
        "sqlite://user:password@localhost:5432/dbname",
        "asyncpg://user:password@localhost:5432/dbname",
        "pg8000://user:password@localhost:5432/dbname"
        "psycopg2://user:password@localhost:5432/dbname"
    ]

    for uri in invalid_uri_values:
        assert is_valid_postgres_uri(uri) is False
