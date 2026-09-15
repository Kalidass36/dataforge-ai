import pytest

from app.sql.executor import SQLExecutor
from app.sql.schema_validator import SchemaValidator
from app.sql.validator import SQLValidator


def test_existing_table():

    validator = SchemaValidator()

    valid, errors = validator.validate(
        "SELECT * FROM customers"
    )

    assert valid is True
    assert errors == []


def test_existing_table_and_column():

    validator = SchemaValidator()

    valid, errors = validator.validate(
        "SELECT name FROM customers"
    )

    assert valid is True
    assert errors == []


def test_unknown_table():

    validator = SchemaValidator()

    valid, errors = validator.validate(
        "SELECT * FROM customer_reviews"
    )

    assert valid is False

    assert any(
        "Unknown table" in error
        for error in errors
    )


def test_unknown_column():

    validator = SchemaValidator()

    valid, errors = validator.validate(
        "SELECT fake_column FROM customers"
    )

    assert valid is False

    assert any(
        "Unknown column" in error
        for error in errors
    )


def test_dangerous_sql_is_rejected_by_validator():

    for sql in [
        "DELETE FROM customers WHERE 1 = 1",
        "DROP TABLE customers",
        "UPDATE customers SET name = 'x'",
        "ALTER TABLE customers DROP COLUMN email",
        "INSERT INTO customers (name) VALUES ('bad')",
        "CREATE TABLE danger_test (id INTEGER)",
    ]:
        valid, message = SQLValidator.validate(sql)

        assert valid is False
        assert "Only SELECT/WITH queries are allowed." in message or "Forbidden SQL operation" in message


def test_executor_rejects_dangerous_sql():

    executor = SQLExecutor()

    with pytest.raises(ValueError, match="Only SELECT/WITH queries are allowed"):
        executor.execute("DELETE FROM customers WHERE 1 = 1")