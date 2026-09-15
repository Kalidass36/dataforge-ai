import sqlglot
from sqlalchemy import text
from sqlglot import exp

from app.database import get_engine


class SchemaValidator:

    def __init__(self):
        self.engine = get_engine()
        self.schema = self._load_schema()

    def _load_schema(self):

        schema = {}

        with self.engine.connect() as connection:

            tables = connection.execute(
                text(
                    """
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table'
                    AND name NOT LIKE 'sqlite_%'
                    ORDER BY name
                    """
                )
            ).fetchall()

            for table_row in tables:

                table_name = table_row[0]

                columns = connection.execute(
                    text(
                        f'PRAGMA table_info("{table_name}")'
                    )
                ).fetchall()

                schema[table_name] = {
                    column[1]
                    for column in columns
                }

        return schema

    def validate(self, sql: str):

        try:

            parsed = sqlglot.parse_one(
                sql,
                read="sqlite",
            )

        except Exception as error:

            return False, [
                f"SQL parsing error: {error}"
            ]

        errors = []

        # --------------------------------
        # Check tables
        # --------------------------------

        for table in parsed.find_all(exp.Table):

            table_name = table.name

            if table_name not in self.schema:

                errors.append(
                    f"Unknown table: {table_name}"
                )

        # --------------------------------
        # Check columns
        # --------------------------------

        known_tables = {
            table.name
            for table in parsed.find_all(exp.Table)
        }

        known_columns = set()

        for table_name in known_tables:

            if table_name in self.schema:

                known_columns.update(
                    self.schema[table_name]
                )

        for column in parsed.find_all(exp.Column):

            column_name = column.name

            if column_name == "*":
                continue

            if column_name not in known_columns:

                errors.append(
                    f"Unknown column: {column_name}"
                )

        if errors:

            return False, errors

        return True, []