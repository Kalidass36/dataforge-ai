from app.agent.router import (
    classify_intent,
)


def test_sql_intent():

    result = classify_intent(
        "Show top customers"
    )

    assert result == "sql"


def test_quality_intent():

    result = classify_intent(
        "Find missing values"
    )

    assert result == "quality"


def test_catalog_intent():

    result = classify_intent(
        "Show database schema"
    )

    assert result == "catalog"