class RootCauseAnalyzer:

    ROOT_CAUSES = {

        "SCHEMA_ERROR":
            "The query references a table or column "
            "that does not exist in the available schema.",

        "SYNTAX_ERROR":
            "The generated SQL contains invalid SQL syntax.",

        "CONNECTION_ERROR":
            "The application could not connect to the database.",

        "TIMEOUT_ERROR":
            "The database operation took longer than the "
            "allowed execution time.",

        "PERMISSION_ERROR":
            "The operation was rejected because of insufficient "
            "database permissions.",

        "TYPE_ERROR":
            "The query attempted an operation using incompatible "
            "data types.",

        "UNKNOWN_ERROR":
            "The system encountered an error that could not "
            "be classified automatically.",
    }

    @classmethod
    def analyze(cls, error_type: str):

        return cls.ROOT_CAUSES.get(
            error_type,
            cls.ROOT_CAUSES["UNKNOWN_ERROR"],
        )