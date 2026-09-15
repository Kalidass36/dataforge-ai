from app.agent.router import (
    classify_intent,
)

from app.catalog.catalog import (
    DataCatalog,
)

from app.quality.monitor import (
    QualityMonitor,
)

from app.sql.nl_to_sql import (
    NaturalLanguageSQL,
)
from app.sql.executor import SQLExecutor


def router_node(state):

    intent = classify_intent(
        state["user_input"]
    )

    return {
        "intent": intent
    }


def catalog_node(state):

    catalog = DataCatalog()

    try:

        catalog.load()

    except FileNotFoundError:

        catalog.build()

        catalog.save()

    question = state[
        "user_input"
    ]

    words = question.lower().split()

    results = []

    for word in words:

        if len(word) < 3:
            continue

        matches = catalog.search(
            word
        )

        for match in matches:

            if match not in results:

                results.append(match)

    return {
        "catalog_result": results
    }


def quality_node(_state):

    monitor = QualityMonitor()

    result = monitor.run()

    return {
        "quality_report":
            result["report"]
    }


def sql_node(state):

    system = NaturalLanguageSQL()

    try:

        result = system.ask(state["user_input"])

        # `result` may be a dict with keys: success, sql, result, error
        if isinstance(result, dict):
            return {
                "sql": result.get("sql", ""),
                "nl_result": result.get("result"),
                "nl_success": result.get("success", False),
                "nl_error": result.get("error"),
            }

        # Fallback: if generator returned raw SQL string
        return {"sql": str(result)}

    except Exception as error:

        return {
            "error": str(error)
        }


def response_node(state):

    if state.get("error"):
        return {
            "response":
                "DataForge encountered an error: "
                + state["error"]
        }

    intent = state.get(
        "intent",
        "sql"
    )

    if intent == "catalog":

        results = state.get(
            "catalog_result",
            []
        )

        if not results:

            return {
                "response":
                    "No matching catalog information was found."
            }

        lines = [
            "DataForge Catalog Results:"
        ]

        for table in results:

            lines.append(
                f'\nTable: {table["table"]}'
            )

            lines.append(
                f'Rows: {table["row_count"]}'
            )

            lines.append(
                "Columns:"
            )

            for column in table[
                "columns"
            ]:

                lines.append(
                    f'- {column["name"]} '
                    f'({column["type"]})'
                )

        return {
            "response":
                "\n".join(lines)
        }

    if intent == "quality":

        report = state.get(
            "quality_report",
            {}
        )

        score = report.get(
            "quality_score",
            "N/A"
        )

        return {
            "response":
                f"DataForge Quality Score: "
                f"{score}/100"
        }

    # For SQL intent, try to execute the SQL and return rows
    sql = state.get("sql", "")

    if not sql:
        return {
            "response": "No SQL was generated for this request.",
        }

    try:
        executor = SQLExecutor()
        result = executor.execute(sql)

        return {
            "sql": sql,
            "result": result,
            # Also set a friendly response payload (rows) so the UI shows the answer
            "response": result.get("rows", []),
        }

    except Exception as error:
        return {
            "error": str(error),
        }