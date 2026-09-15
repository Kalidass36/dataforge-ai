from sqlalchemy import text

from app.database import get_engine


class RelationshipExtractor:

    def __init__(self):

        self.engine = get_engine()

    def get_relationships(
        self,
        table_name,
    ):

        query = text(
            f'PRAGMA foreign_key_list("{table_name}")'
        )

        with self.engine.connect() as connection:

            rows = connection.execute(
                query
            ).fetchall()

        relationships = []

        for row in rows:

            relationships.append({

                "from_table":
                    table_name,

                "from_column":
                    row[3],

                "to_table":
                    row[2],

                "to_column":
                    row[4],
            })

        return relationships

    def extract(self):

        query = text(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )

        with self.engine.connect() as connection:

            tables = [
                row[0]
                for row in connection.execute(
                    query
                ).fetchall()
            ]

        relationships = []

        for table in tables:

            relationships.extend(
                self.get_relationships(
                    table
                )
            )

        return relationships