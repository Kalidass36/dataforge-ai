from sqlalchemy import MetaData, func, inspect, select

from app.database import get_engine


class SchemaIntelligence:
    """
    Automatically analyzes a database schema.

    Discovers:
    - tables
    - columns
    - data types
    - primary keys
    - nullable columns
    - null counts
    - row counts
    - foreign-key relationships
    """

    def __init__(self):
        self.engine = get_engine()
        self.inspector = inspect(self.engine)

    def get_tables(self):
        """Return all table names in the database."""
        return self.inspector.get_table_names()

    def analyze_table(self, table_name):
        """Analyze one database table."""

        metadata = MetaData()

        table = __import__(
            "sqlalchemy"
        ).Table(
            table_name,
            metadata,
            autoload_with=self.engine,
        )

        columns_info = []

        primary_keys = set(
            self.inspector.get_pk_constraint(table_name).get(
                "constrained_columns",
                []
            )
        )

        with self.engine.connect() as connection:

            row_count = connection.execute(
                select(func.count()).select_from(table)
            ).scalar_one()

            for column in table.columns:

                null_count = connection.execute(
                    select(func.count())
                    .select_from(table)
                    .where(column.is_(None))
                ).scalar_one()

                null_percentage = (
                    (null_count / row_count) * 100
                    if row_count > 0
                    else 0
                )

                columns_info.append(
                    {
                        "name": column.name,
                        "type": str(column.type),
                        "nullable": column.nullable,
                        "primary_key": column.name in primary_keys,
                        "null_count": null_count,
                        "null_percentage": round(
                            null_percentage,
                            2,
                        ),
                    }
                )

        return {
            "row_count": row_count,
            "columns": columns_info,
            "foreign_keys": self.get_foreign_keys(table_name),
        }

    def get_foreign_keys(self, table_name):
        """Discover foreign-key relationships."""

        foreign_keys = self.inspector.get_foreign_keys(
            table_name
        )

        relationships = []

        for fk in foreign_keys:

            relationships.append(
                {
                    "columns": fk.get(
                        "constrained_columns",
                        []
                    ),
                    "references_table": fk.get(
                        "referred_table"
                    ),
                    "references_columns": fk.get(
                        "referred_columns",
                        []
                    ),
                }
            )

        return relationships

    def discover_schema(self):
        """Analyze the complete database."""

        schema_report = {}

        for table_name in self.get_tables():

            schema_report[table_name] = (
                self.analyze_table(table_name)
            )

        return schema_report


def main():

    analyzer = SchemaIntelligence()

    report = analyzer.discover_schema()

    print("\n" + "=" * 70)
    print("DATAFORGE — SCHEMA INTELLIGENCE REPORT")
    print("=" * 70)

    for table_name, table_info in report.items():

        print(f"\nTABLE: {table_name}")
        print("-" * 70)

        print(
            f"Rows: {table_info['row_count']}"
        )

        print("\nColumns:")

        for column in table_info["columns"]:

            primary_key = (
                " PRIMARY KEY"
                if column["primary_key"]
                else ""
            )

            nullable = (
                "NULLABLE"
                if column["nullable"]
                else "NOT NULL"
            )

            print(
                f"  {column['name']:<20} "
                f"{column['type']:<15} "
                f"{nullable:<10}"
                f"{primary_key}"
                f" | NULLs: {column['null_count']} "
                f"({column['null_percentage']}%)"
            )

        if table_info["foreign_keys"]:

            print("\nRelationships:")

            for relationship in table_info[
                "foreign_keys"
            ]:

                print(
                    f"  {relationship['columns']} "
                    f"→ "
                    f"{relationship['references_table']}."
                    f"{relationship['references_columns']}"
                )

        else:

            print("\nRelationships: None")


if __name__ == "__main__":
    main()