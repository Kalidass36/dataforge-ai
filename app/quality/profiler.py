from sqlalchemy import text

from app.database import get_engine
from app.quality.null_checker import NullChecker
from app.quality.duplicate_checker import (
    DuplicateChecker,
)
from app.quality.anomaly_checker import (
    AnomalyChecker,
)


class DataProfiler:

    def __init__(self):

        self.engine = get_engine()

        self.null_checker = NullChecker(
            self.engine
        )

        self.duplicate_checker = (
            DuplicateChecker(
                self.engine
            )
        )

        self.anomaly_checker = (
            AnomalyChecker(
                self.engine
            )
        )

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

        return [
            {
                "name": row[1],
                "type": row[2],
                "primary_key": bool(row[5]),
            }
            for row in rows
        ]

    def profile(self):

        report = {
            "tables": [],
            "null_issues": [],
            "duplicate_issues": [],
            "anomalies": [],
        }

        tables = self.get_tables()

        for table_name in tables:

            columns = self.get_columns(
                table_name
            )

            column_names = [
                column["name"]
                for column in columns
            ]

            report["tables"].append({
                "table": table_name,
                "columns": columns,
            })

            # NULL analysis
            null_results = (
                self.null_checker.check_table(
                    table_name,
                    column_names,
                )
            )

            report["null_issues"].extend(
                null_results
            )

            # Duplicate analysis
            duplicate_results = (
                self.duplicate_checker.check_table(
                    table_name,
                    column_names,
                )
            )

            report["duplicate_issues"].extend(
                duplicate_results
            )

            # Numeric anomaly analysis
            for column in columns:

                column_type = (
                    column["type"] or ""
                ).upper()

                if any(
                    data_type in column_type
                    for data_type in [
                        "INT",
                        "REAL",
                        "FLOAT",
                        "DOUBLE",
                        "DECIMAL",
                        "NUMERIC",
                    ]
                ):

                    result = (
                        self.anomaly_checker.check_column(
                            table_name,
                            column["name"],
                        )
                    )

                    report["anomalies"].append(
                        result
                    )

        return report