import json
from pathlib import Path

from app.intelligence.schema_engine import SchemaIntelligence


def export_schema():

    analyzer = SchemaIntelligence()

    report = analyzer.discover_schema()

    output_path = (
        Path(__file__).resolve().parent.parent.parent
        / "data"
        / "schema_report.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
        )

    print(
        f"Schema report saved to:\n{output_path}"
    )


if __name__ == "__main__":
    export_schema()