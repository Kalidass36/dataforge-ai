from fastapi import APIRouter, Depends

from app.api.dependencies import get_graph

from app.api.schemas import (
    CatalogResponse,
    HealthResponse,
    QualityResponse,
    QueryRequest,
    QueryResponse,
)

from app.catalog.catalog import DataCatalog
from app.quality.monitor import QualityMonitor


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health():
    return {
        "status": "healthy",
        "service": "DataForge API",
    }


@router.post(
    "/query",
    response_model=QueryResponse,
)
def query_data(
    request: QueryRequest,
    graph=Depends(get_graph),
):
    state = {
        "user_input": request.question,
        "retry_count": 0,
    }

    try:
        # Execute the DataForge graph
        graph_result = graph.invoke(state)

        # Start with the complete graph result
        payload = graph_result

        # Sometimes the actual query output is inside "response"
        nested_response = graph_result.get("response")

        if isinstance(nested_response, dict):
            payload = nested_response

        # Extract SQL safely
        sql = payload.get("sql", "")

        # Extract database result safely
        database_result = payload.get("result", {})

        # Extract rows
        rows = []

        if isinstance(database_result, dict):
            rows = database_result.get("rows", [])

        # Try to use an existing readable response
        readable_response = payload.get("response")

        # If no readable response exists, create one from the rows
        if not (isinstance(readable_response, str) and readable_response.strip()):
            if rows:
                readable_response = "\n".join(
                    " | ".join(
                        f"{key}: {value}"
                        for key, value in row.items()
                    )
                    for row in rows
                )
            else:
                readable_response = "The query completed, but no rows were returned."

        return {
            "success": True,
            "question": request.question,
            "intent": graph_result.get("intent"),
            "sql": sql if isinstance(sql, str) else "",
            "response": readable_response,
            "error": graph_result.get("error"),
        }

    except Exception as error:
        return {
            "success": False,
            "question": request.question,
            "intent": None,
            "sql": "",
            "response": "",
            "error": str(error),
        }

@router.get(
    "/catalog",
    response_model=CatalogResponse,
)
def get_catalog():
    catalog = DataCatalog()

    try:
        data = catalog.load()

    except FileNotFoundError:
        data = catalog.build()
        catalog.save()

    return {
        "success": True,
        "tables": data,
    }


@router.get(
    "/quality",
    response_model=QualityResponse,
)
def get_quality():
    monitor = QualityMonitor()

    result = monitor.run()

    return {
        "success": True,
        "report": result["report"],
    }