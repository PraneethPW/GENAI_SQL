from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db, engine
from app.db.schema_introspect import get_schema_description
from app.core.openai_client import generate_sql

router = APIRouter(prefix="/api", tags=["query"])


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    sql: str
    columns: list[str]
    rows: list[list[str]]


def is_safe_sql(sql: str) -> bool:
    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    lowered = sql.lower()
    return not any(word in lowered for word in forbidden)


@router.post("/query", response_model=QueryResponse)
async def run_query(payload: QueryRequest, db: Session = Depends(get_db)):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    schema_desc = get_schema_description(engine)

    sql = await generate_sql(schema_desc, payload.question)

    if not is_safe_sql(sql):
        raise HTTPException(status_code=400, detail="Generated SQL is not read-only.")

    try:
        result = db.execute(text(sql))
        columns = list(result.keys())
        rows = [list(map(str, row)) for row in result.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL execution error: {e}")

    return QueryResponse(sql=sql, columns=columns, rows=rows)
