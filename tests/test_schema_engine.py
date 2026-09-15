from app.intelligence.schema_engine import (
    SchemaIntelligence,
)


def test_tables_are_discovered():

    analyzer = SchemaIntelligence()

    tables = analyzer.get_tables()

    expected_tables = {
        "customers",
        "products",
        "orders",
        "order_items",
        "payments",
        "employees",
        "support_tickets",
    }

    assert expected_tables.issubset(
        set(tables)
    )


def test_customers_schema():

    analyzer = SchemaIntelligence()

    report = analyzer.discover_schema()

    customers = report["customers"]

    assert customers["row_count"] >= 0

    column_names = {
        column["name"]
        for column in customers["columns"]
    }

    assert "customer_id" in column_names
    assert "name" in column_names
    assert "email" in column_names


def test_orders_relationship():

    analyzer = SchemaIntelligence()

    report = analyzer.discover_schema()

    orders = report["orders"]

    relationships = orders["foreign_keys"]

    assert any(
        relationship["references_table"]
        == "customers"
        for relationship in relationships
    )