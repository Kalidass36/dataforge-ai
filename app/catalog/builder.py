from app.catalog.metadata import (
    MetadataExtractor,
)

from app.catalog.relationships import (
    RelationshipExtractor,
)

from app.catalog.descriptions import (
    DescriptionGenerator,
)


class CatalogBuilder:

    def __init__(self):

        self.metadata = MetadataExtractor()

        self.relationships = (
            RelationshipExtractor()
        )

        self.descriptions = (
            DescriptionGenerator()
        )

    def build(self):

        tables = self.metadata.extract()

        relationships = (
            self.relationships.extract()
        )

        catalog = []

        for table in tables:

            description = (
                self.descriptions.generate(
                    table,
                    relationships,
                )
            )

            catalog.append({

                "table":
                    table["table"],

                "row_count":
                    table["row_count"],

                "columns":
                    table["columns"],

                "relationships": [
                    relationship
                    for relationship
                    in relationships
                    if (
                        relationship[
                            "from_table"
                        ]
                        == table["table"]
                        or
                        relationship[
                            "to_table"
                        ]
                        == table["table"]
                    )
                ],

                "ai_description":
                    description,
            })

        return catalog
