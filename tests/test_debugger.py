from app.debugger.error_parser import ErrorParser
from app.debugger.root_cause import RootCauseAnalyzer


def test_schema_error():

    result = ErrorParser.classify(
        "no such column: customers.revenue"
    )

    assert result == "SCHEMA_ERROR"


def test_table_error():

    result = ErrorParser.classify(
        "no such table: customer_reviews"
    )

    assert result == "SCHEMA_ERROR"


def test_syntax_error():

    result = ErrorParser.classify(
        "syntax error near SELECT"
    )

    assert result == "SYNTAX_ERROR"


def test_connection_error():

    result = ErrorParser.classify(
        "connection refused"
    )

    assert result == "CONNECTION_ERROR"


def test_timeout_error():

    result = ErrorParser.classify(
        "operation timed out"
    )

    assert result == "TIMEOUT_ERROR"


def test_permission_error():

    result = ErrorParser.classify(
        "permission denied"
    )

    assert result == "PERMISSION_ERROR"


def test_unknown_error():

    result = ErrorParser.classify(
        "something completely unexpected"
    )

    assert result == "UNKNOWN_ERROR"


def test_root_cause():

    result = RootCauseAnalyzer.analyze(
        "SCHEMA_ERROR"
    )

    assert "column" in result.lower()