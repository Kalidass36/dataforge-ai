from app.intelligence.schema_context import (
    build_schema_context,
)
from app.llm.ollama_provider import OllamaProvider
from app.sql.prompt import build_prompt


class SQLGenerator:

    def __init__(self):

        self.llm = OllamaProvider()

    def generate(self, question: str):

        schema = build_schema_context()

        prompt = build_prompt(
            schema,
            question,
        )

        sql = self.llm.generate(prompt)

        return sql