import json

from app.llm.ollama_provider import (
    OllamaProvider,
)

from app.quality.profiler import (
    DataProfiler,
)

from app.quality.quality_report import (
    QualityReport,
)


class QualityMonitor:

    def __init__(self):

        self.profiler = DataProfiler()

        self.llm = OllamaProvider()

    def run(self):

        profile = self.profiler.profile()

        report = QualityReport(
            profile
        ).build()

        prompt = f"""
You are DataForge AI Data Quality Analyst.

Analyze this database quality report.

REPORT:

{json.dumps(
    report,
    indent=2,
    default=str,
)}

Provide a concise professional analysis.

Use exactly this format:

OVERALL ASSESSMENT:
<assessment>

KEY ISSUES:
- <issue 1>
- <issue 2>

RECOMMENDATIONS:
- <recommendation 1>
- <recommendation 2>

PRIORITY:
<LOW / MEDIUM / HIGH>

Do not invent issues that are not supported
by the report.
"""

        analysis = self.llm.generate(
            prompt
        )

        return {
            "report": report,
            "analysis": analysis,
        }