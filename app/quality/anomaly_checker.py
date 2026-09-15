from sqlalchemy import text
import statistics


class AnomalyChecker:

    def __init__(self, engine):
        self.engine = engine

    def check_column(
        self,
        table_name,
        column_name,
    ):

        query = text(
            f'''
            SELECT "{column_name}"
            FROM "{table_name}"
            WHERE "{column_name}" IS NOT NULL
            '''
        )

        try:

            with self.engine.connect() as connection:

                rows = connection.execute(
                    query
                ).fetchall()

            values = []

            for row in rows:

                value = row[0]

                if isinstance(
                    value,
                    (int, float)
                ):

                    values.append(
                        float(value)
                    )

            if len(values) < 5:

                return {
                    "table": table_name,
                    "column": column_name,
                    "checked": False,
                    "reason": (
                        "Not enough numeric values"
                    ),
                }

            mean = statistics.mean(values)

            stdev = statistics.stdev(values)

            if stdev == 0:

                return {
                    "table": table_name,
                    "column": column_name,
                    "checked": True,
                    "anomaly_count": 0,
                }

            anomalies = []

            for value in values:

                z_score = abs(
                    (value - mean) / stdev
                )

                if z_score > 3:

                    anomalies.append(value)

            return {
                "table": table_name,
                "column": column_name,
                "checked": True,
                "mean": round(mean, 2),
                "standard_deviation": round(
                    stdev,
                    2
                ),
                "anomaly_count": len(
                    anomalies
                ),
            }

        except Exception as error:

            return {
                "table": table_name,
                "column": column_name,
                "checked": False,
                "reason": str(error),
            }