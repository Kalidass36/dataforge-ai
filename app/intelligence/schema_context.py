from app.intelligence.schema_engine import SchemaIntelligence


def build_schema_context():

    analyzer = SchemaIntelligence()

    report = analyzer.discover_schema()

    lines = []

    lines.append(
        "DATABASE SCHEMA"
    )

    lines.append(
        "=" * 50
    )

    for table_name, table_info in report.items():

        lines.append(
            f"\nTABLE: {table_name}"
        )

        lines.append(
            f"ROWS: {table_info['row_count']}"
        )

        lines.append(
            "COLUMNS:"
        )

        for column in table_info["columns"]:

            flags = []

            if column["primary_key"]:
                flags.append("PRIMARY KEY")

            if not column["nullable"]:
                flags.append("NOT NULL")

            flag_text = (
                f" ({', '.join(flags)})"
                if flags
                else ""
            )

            lines.append(
                f"  - {column['name']}: "
                f"{column['type']}"
                f"{flag_text}"
            )

        for relationship in table_info[
            "foreign_keys"
        ]:

            lines.append(
                f"  FK: "
                f"{relationship['columns']} → "
                f"{relationship['references_table']}."
                f"{relationship['references_columns']}"
            )

    return "\n".join(lines)


if __name__ == "__main__":

    print(build_schema_context())