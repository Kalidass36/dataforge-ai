class ErrorParser:

    ERROR_PATTERNS = {

        "SCHEMA_ERROR": [
            "no such table",
            "no such column",
            "unknown column",
            "unknown table",
            "does not exist",
        ],

        "SYNTAX_ERROR": [
            "syntax error",
            "near",
            "parser error",
        ],

        "CONNECTION_ERROR": [
            "connection refused",
            "unable to connect",
            "connection error",
        ],

        "TIMEOUT_ERROR": [
            "timeout",
            "timed out",
        ],

        "PERMISSION_ERROR": [
            "permission denied",
            "access denied",
            "not authorized",
        ],

        "TYPE_ERROR": [
            "datatype mismatch",
            "type mismatch",
            "invalid type",
        ],
    }

    @classmethod
    def classify(cls, error_message: str):

        message = error_message.lower()

        for error_type, patterns in cls.ERROR_PATTERNS.items():

            for pattern in patterns:

                if pattern in message:

                    return error_type

        return "UNKNOWN_ERROR"