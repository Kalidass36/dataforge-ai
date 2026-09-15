from app.quality.monitor import (
    QualityMonitor,
)


def main():

    monitor = QualityMonitor()

    print("=" * 60)
    print("DATAFORGE AI DATA QUALITY MONITOR")
    print("=" * 60)

    print("\nProfiling database...")

    result = monitor.run()

    report = result["report"]

    print("\nQUALITY SCORE:")
    print(
        f'{report["quality_score"]}/100'
    )

    print("\nTABLE COUNT:")
    print(
        report["table_count"]
    )

    print("\nNULL ISSUES:")
    print(
        len(report["null_issues"])
    )

    for issue in report["null_issues"]:

        print(
            f'- {issue["table"]}.'
            f'{issue["column"]}: '
            f'{issue["null_count"]} NULL values'
        )

    print("\nDUPLICATE ISSUES:")
    print(
        len(report["duplicate_issues"])
    )

    for issue in report[
        "duplicate_issues"
    ]:

        print(
            f'- {issue["table"]}: '
            f'{issue["duplicate_rows"]} '
            'duplicate rows'
        )

    print("\nANOMALY CHECKS:")

    for anomaly in report[
        "anomalies"
    ]:

        if anomaly.get(
            "anomaly_count",
            0
        ) > 0:

            print(
                f'- {anomaly["table"]}.'
                f'{anomaly["column"]}: '
                f'{anomaly["anomaly_count"]} '
                'anomalies'
            )

    print("\nAI ANALYSIS:")
    print("-" * 60)

    print(
        result["analysis"]
    )


if __name__ == "__main__":
    main()