from sqlalchemy import text

from app.database import get_engine
from app.sql.validator import SQLValidator


class SQLExecutor:

    def __init__(self):
        self.engine = get_engine()

    def execute(self, sql: str):
        """
        Execute a read-only SQL query and return rows.
        """

        valid, message = SQLValidator.validate(sql)

        if not valid:
            raise ValueError(message)

        with self.engine.connect() as connection:

            result = connection.execute(
                text(sql)
            )

            columns = list(result.keys())

            rows = [
                dict(row._mapping)
                for row in result.fetchall()
            ]

        return {
            "columns": columns,
            "rows": rows,
        }