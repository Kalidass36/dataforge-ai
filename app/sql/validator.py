import re


class SQLValidator:

    FORBIDDEN_KEYWORDS = {
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE",
    }

    @classmethod
    def validate(cls, sql: str):

        normalized = re.sub(
            r"\s+",
            " ",
            sql.strip().upper(),
        )

        if not normalized:
            return False, "SQL query is empty."

        if not normalized.startswith(("SELECT", "WITH")):
            return (
                False,
                "Only SELECT/WITH queries are allowed.",
            )

        for keyword in cls.FORBIDDEN_KEYWORDS:

            if re.search(
                rf"\b{keyword}\b",
                normalized,
            ):
                return (
                    False,
                    f"Forbidden SQL operation: {keyword}",
                )

        return True, "SQL query is valid."