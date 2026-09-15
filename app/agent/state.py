from typing import TypedDict, List, Dict, Any


class DataForgeState(TypedDict, total=False):

    user_input: str

    intent: str

    sql: str

    validated_sql: str

    query_result: List[Dict[str, Any]]

    error: str

    retry_count: int

    response: str

    catalog_result: List[Dict[str, Any]]

    quality_report: Dict[str, Any]

    debug_result: Dict[str, Any]