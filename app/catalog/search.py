class CatalogSearch:

    def __init__(self, catalog):

        self.catalog = catalog

    def search(self, query):

        query = query.lower().strip()

        results = []

        for table in self.catalog:

            table_name = table[
                "table"
            ].lower()

            if query in table_name:

                results.append(table)

                continue

            for column in table[
                "columns"
            ]:

                column_name = (
                    column["name"]
                    .lower()
                )

                if query in column_name:

                    results.append(table)

                    break

        return results