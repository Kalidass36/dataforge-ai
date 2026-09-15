from app.quality.profiler import DataProfiler
from app.quality.quality_report import QualityReport


def test_profiler_discovers_tables():

    profiler = DataProfiler()

    report = profiler.profile()

    tables = [
        item["table"]
        for item in report["tables"]
    ]

    assert "customers" in tables
    assert "orders" in tables
    assert "products" in tables


def test_profiler_has_expected_sections():

    profiler = DataProfiler()

    report = profiler.profile()

    assert "tables" in report
    assert "null_issues" in report
    assert "duplicate_issues" in report
    assert "anomalies" in report


def test_quality_report():

    profile = {
        "tables": [
            {"table": "customers"}
        ],
        "null_issues": [],
        "duplicate_issues": [],
        "anomalies": [],
    }

    report = QualityReport(
        profile
    ).build()

    assert report["quality_score"] == 100
    assert report["table_count"] == 1