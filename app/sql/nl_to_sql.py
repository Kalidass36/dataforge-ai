from app.intelligence.schema_context import (
    build_schema_context,
)

from app.sql.cleaner import clean_sql
from app.sql.corrector import SQLCorrector
from app.sql.executor import SQLExecutor
from app.sql.generator import SQLGenerator
from app.sql.schema_validator import SchemaValidator
from app.sql.validator import SQLValidator
from app.debugger.debugger import PipelineDebugger


class NaturalLanguageSQL:

    def __init__(self):

        self.generator = SQLGenerator()
        self.corrector = SQLCorrector()
        self.executor = SQLExecutor()
        self.schema_validator = SchemaValidator()
        self.debugger = PipelineDebugger()

    def ask(self, question: str):

        schema_context = build_schema_context()

        # --------------------------------
        # STEP 1: Generate SQL
        # --------------------------------

        raw_sql = self.generator.generate(
            question
        )

        sql = clean_sql(raw_sql)

        # --------------------------------
        # STEP 2: Safety validation
        # --------------------------------

        safe, safety_message = (
            SQLValidator.validate(sql)
        )

        if not safe:

            return {
                "success": False,
                "sql": sql,
                "error": safety_message,
            }

        # --------------------------------
        # STEP 3: Schema validation
        # --------------------------------

        valid, errors = (
            self.schema_validator.validate(sql)
        )

        # --------------------------------
        # STEP 4: Self-correction
        # --------------------------------

        if not valid:

            corrected_sql = (
                self.corrector.correct(
                    question=question,
                    sql=sql,
                    errors=errors,
                    schema_context=schema_context,
                )
            )

            sql = clean_sql(
                corrected_sql
            )

            # Validate corrected SQL safety
            safe, safety_message = (
                SQLValidator.validate(sql)
            )

            if not safe:

                return {
                    "success": False,
                    "sql": sql,
                    "error": safety_message,
                }

            # Validate corrected SQL schema
            valid, errors = (
                self.schema_validator.validate(
                    sql
                )
            )

            if not valid:

                return {
                    "success": False,
                    "sql": sql,
                    "error": (
                        "SQL remained invalid after "
                        "automatic correction: "
                        + "; ".join(errors)
                    ),
                }

        # --------------------------------
        # STEP 5: Execute
        # --------------------------------

        try:

            result = self.executor.execute(sql)

            return {
                "success": True,
                "sql": sql,
                "result": result,
            }

        except Exception as error:

            error_message = str(error)

            debug_result = self.debugger.debug(
                error_message
            )

            return {
                "success": False,
                "sql": sql,
                "error": error_message,
                "debug": debug_result,
            }