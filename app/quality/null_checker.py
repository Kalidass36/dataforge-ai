from sqlalchemy import text


class NullChecker:

    def __init__(self, engine):
        self.engine = engine

    def check_table(self, table_name, columns):

        results = []

        with self.engine.connect() as connection:

            for column in columns:

                query = text(
                    f'''
                    SELECT COUNT(*)
                    FROM "{table_name}"
                    WHERE "{column}" IS NULL
                    '''
                )

                null_count = connection.execute(
                    query
                ).scalar()

                total_query = text(
                    f'''
                    SELECT COUNT(*)
                    FROM "{table_name}"
                    '''
                )

                total_count = connection.execute(
                    total_query
                ).scalar()

                percentage = 0

                if total_count > 0:
                    percentage = (
                        null_count / total_count
                    ) * 100

                if null_count > 0:

                    results.append({
                        "table": table_name,
                        "column": column,
                        "null_count": null_count,
                        "total_rows": total_count,
                        "null_percentage": round(
                            percentage,
                            2
                        ),
                    })

        return results