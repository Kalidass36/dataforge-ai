from app.catalog.catalog import (
    DataCatalog,
)


def main():

    catalog = DataCatalog()

    print("=" * 60)
    print("DATAFORGE AI DATA CATALOG")
    print("=" * 60)

    print("\nBuilding catalog...")

    data = catalog.build()

    print(
        f"\nCataloged {len(data)} tables."
    )

    for table in data:

        print("\n" + "=" * 60)

        print(
            f'TABLE: {table["table"]}'
        )

        print(
            f'ROWS: {table["row_count"]}'
        )

        print("\nCOLUMNS:")

        for column in table[
            "columns"
        ]:

            print(
                f'  - {column["name"]} '
                f'({column["type"]})'
            )

        print("\nRELATIONSHIPS:")

        for relationship in table[
            "relationships"
        ]:

            print(
                f'  - '
                f'{relationship["from_table"]}.'
                f'{relationship["from_column"]}'
                f' → '
                f'{relationship["to_table"]}.'
                f'{relationship["to_column"]}'
            )

        print("\nAI DESCRIPTION:")

        print(
            table["ai_description"]
        )

    path = catalog.save()

    print(
        f"\nCatalog saved to: {path}"
    )


if __name__ == "__main__":
    main()