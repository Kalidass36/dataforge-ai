from app.catalog.metadata import (
    MetadataExtractor,
)

from app.catalog.relationships import (
    RelationshipExtractor,
)

from app.catalog.search import (
    CatalogSearch,
)


def test_metadata_discovers_tables():

    extractor = MetadataExtractor()

    tables = extractor.get_tables()

    assert "customers" in tables
    assert "orders" in tables
    assert "products" in tables


def test_metadata_discovers_columns():

    extractor = MetadataExtractor()

    columns = extractor.get_columns(
        "customers"
    )

    column_names = [
        column["name"]
        for column in columns
    ]

    assert "customer_id" in column_names


def test_relationship_extractor():

    extractor = RelationshipExtractor()

    relationships = (
        extractor.extract()
    )

    assert isinstance(
        relationships,
        list,
    )


def test_catalog_search():

    catalog = [
        {
            "table": "customers",
            "columns": [
                {
                    "name": "customer_id"
                },
                {
                    "name": "name"
                },
            ],
        },
        {
            "table": "orders",
            "columns": [
                {
                    "name": "order_id"
                },
            ],
        },
    ]

    search = CatalogSearch(
        catalog
    )

    results = search.search(
        "customer"
    )

    assert len(results) == 1
    assert (
        results[0]["table"]
        == "customers"
    )


def test_catalog_search_column():

    catalog = [
        {
            "table": "customers",
            "columns": [
                {
                    "name": "email"
                },
            ],
        }
    ]

    search = CatalogSearch(
        catalog
    )

    results = search.search(
        "email"
    )

    assert len(results) == 1