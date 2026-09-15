from app.llm.ollama_provider import OllamaProvider


class FixGenerator:

    def __init__(self):

        self.llm = OllamaProvider()

    def generate_fix(
        self,
        error_message: str,
        error_type: str,
        root_cause: str,
        schema_context: str,
    ):

        prompt = f"""
You are DataForge Pipeline Debugger.

Analyze the following pipeline/database failure.

ERROR TYPE:
{error_type}

ERROR MESSAGE:
{error_message}

LIKELY ROOT CAUSE:
{root_cause}

AVAILABLE DATABASE SCHEMA:
{schema_context}

Provide a concise debugging recommendation.

Return your answer using exactly this structure:

ROOT CAUSE:
<explanation>

SUGGESTED FIX:
<fix>

PREVENTION:
<how to prevent the problem>

Do not invent database tables or columns.
Use only information supported by the provided schema.
"""

        return self.llm.generate(prompt)