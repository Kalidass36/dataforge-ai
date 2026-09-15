from app.debugger.error_parser import ErrorParser
from app.debugger.fix_generator import FixGenerator
from app.debugger.root_cause import RootCauseAnalyzer
from app.intelligence.schema_context import (
    build_schema_context,
)


class PipelineDebugger:

    def __init__(self):

        self.fix_generator = FixGenerator()

    def debug(self, error_message: str):

        # --------------------------------
        # STEP 1: Classify error
        # --------------------------------

        error_type = ErrorParser.classify(
            error_message
        )

        # --------------------------------
        # STEP 2: Determine likely root cause
        # --------------------------------

        root_cause = RootCauseAnalyzer.analyze(
            error_type
        )

        # --------------------------------
        # STEP 3: Get schema
        # --------------------------------

        schema_context = build_schema_context()

        # --------------------------------
        # STEP 4: Generate AI fix
        # --------------------------------

        recommendation = (
            self.fix_generator.generate_fix(
                error_message=error_message,
                error_type=error_type,
                root_cause=root_cause,
                schema_context=schema_context,
            )
        )

        return {
            "error_type": error_type,
            "root_cause": root_cause,
            "recommendation": recommendation,
        }