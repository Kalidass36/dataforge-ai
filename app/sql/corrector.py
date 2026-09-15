from app.llm.ollama_provider import OllamaProvider


class SQLCorrector:

    def __init__(self):

        self.llm = OllamaProvider()

    def correct(
        self,
        question: str,
        sql: str,
        errors: list[str],
        schema_context: str,
    ):

        error_text = "\n".join(
            f"- {error}"
            for error in errors
        )

        prompt = f"""
You are DataForge SQL Correction Agent.

The user asked:

{question}

The generated SQL was:

{sql}

The SQL failed schema validation.

Errors:

{error_text}

Available database schema:

{schema_context}

Correct the SQL.

Rules:

1. Return ONLY SQL.
2. Generate only SELECT or WITH queries.
3. Use only tables that exist.
4. Use only columns that exist.
5. Follow the provided schema.
6. Do not invent columns.
7. Do not invent tables.
8. Keep the original user's intent.
9. Use SQLite-compatible SQL.

Corrected SQL:
"""

        return self.llm.generate(prompt)