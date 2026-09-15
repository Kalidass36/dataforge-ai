from sqlalchemy import text

from app.database import get_engine


class MetadataExtractor:

    def __init__(self):

        self.engine = get_engine()

    def get_tables(self):

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

            return [
                row[0]
                for row in connection.execute(
                    query
                ).fetchall()
            ]

    def get_columns(self, table_name):

        query = text(
            f'PRAGMA table_info("{table_name}")'
        )

        with self.engine.connect() as connection:

            rows = connection.execute(
                query
            ).fetchall()

        columns = []

        for row in rows:

            columns.append({
                "name": row[1],
                "type": row[2],
                "nullable": not bool(row[3]),
                "default": row[4],
                "primary_key": bool(row[5]),
            })

        return columns

    def get_row_count(self, table_name):

        query = text(
            f'''
            SELECT COUNT(*)
            FROM "{table_name}"
            '''
        )

        with self.engine.connect() as connection:

            return connection.execute(
                query
            ).scalar()

    def get_sample_values(
        self,
        table_name,
        column_name,
        limit=3,
    ):

        query = text(
            f'''
            SELECT "{column_name}"
            FROM "{table_name}"
            WHERE "{column_name}" IS NOT NULL
            LIMIT {limit}
            '''
        )

        try:

            with self.engine.connect() as connection:

                rows = connection.execute(
                    query
                ).fetchall()

            return [
                row[0]
                for row in rows
            ]

        except Exception:

            return []

    def extract(self):

        catalog = []

        for table_name in self.get_tables():

            columns = self.get_columns(
                table_name
            )

            for column in columns:

                column["sample_values"] = (
                    self.get_sample_values(
                        table_name,
                        column["name"],
                    )
                )

            catalog.append({

                "table": table_name,

                "row_count":
                    self.get_row_count(
                        table_name
                    ),

                "columns": columns,
            })

        return catalog