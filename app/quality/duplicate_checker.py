from sqlalchemy import text


class DuplicateChecker:

    def __init__(self, engine):
        self.engine = engine

    def check_table(self, table_name, columns):

        if not columns:
            return []

        column_list = ", ".join(
            f'"{column}"'
            for column in columns
        )

        query = text(
            f'''
            SELECT
                COUNT(*) AS total_rows,
                COUNT(DISTINCT ({column_list})) AS unique_rows
            FROM "{table_name}"
            '''
        )

        try:

            with self.engine.connect() as connection:

                result = connection.execute(
                    query
                ).fetchone()

                total_rows = result[0]
                unique_rows = result[1]

                duplicate_count = (
                    total_rows - unique_rows
                )

                if duplicate_count > 0:

                    return [{
                        "table": table_name,
                        "total_rows": total_rows,
                        "unique_rows": unique_rows,
                        "duplicate_rows": duplicate_count,
                    }]

        except Exception:

            return []

        return []