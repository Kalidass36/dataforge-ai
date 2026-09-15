import json

from app.llm.ollama_provider import (
    OllamaProvider,
)


class DescriptionGenerator:

    def __init__(self):

        self.llm = OllamaProvider()

    def generate(
        self,
        table_metadata,
        relationships,
    ):

        table_name = table_metadata[
            "table"
        ]

        relevant_relationships = [
            relationship
            for relationship in relationships
            if (
                relationship["from_table"]
                == table_name
                or
                relationship["to_table"]
                == table_name
            )
        ]

        prompt = f"""
You are the DataForge AI Data Catalog Generator.

Analyze the following database metadata.

TABLE METADATA:

{json.dumps(
    table_metadata,
    indent=2,
    default=str,
)}

RELATIONSHIPS:

{json.dumps(
    relevant_relationships,
    indent=2,
    default=str,
)}

Generate concise documentation.

Return exactly this format:

TABLE PURPOSE:
<one or two sentences>

COLUMN DESCRIPTIONS:
- column_name: description

RELATIONSHIPS:
<describe important relationships>

BUSINESS USE:
<explain how this table might be used>

IMPORTANT:
Do not invent information.
Base descriptions only on the available metadata,
column names, types, sample values and relationships.
"""

        return self.llm.generate(
            prompt
        )