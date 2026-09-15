import re


def clean_sql(sql: str) -> str:

    sql = sql.strip()

    # Remove markdown code fences
    sql = re.sub(
        r"```sql",
        "",
        sql,
        flags=re.IGNORECASE,
    )

    sql = sql.replace("```", "")

    # Remove common introductory text
    if "SELECT" in sql.upper():

        match = re.search(
            r"\b(SELECT|WITH)\b",
            sql,
            flags=re.IGNORECASE,
        )

        if match:
            sql = sql[match.start():]

    return sql.strip()