from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Natural language question for DataForge",
    )


class QueryResponse(BaseModel):

    success: bool

    question: str

    intent: Optional[str] = None

    sql: Optional[str] = None

    response: Optional[str] = None

    error: Optional[str] = None


class HealthResponse(BaseModel):

    status: str

    service: str


class CatalogResponse(BaseModel):

    success: bool

    tables: List[Dict[str, Any]]


class QualityResponse(BaseModel):

    success: bool

    report: Dict[str, Any]