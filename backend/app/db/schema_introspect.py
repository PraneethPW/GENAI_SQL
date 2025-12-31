from sqlalchemy import inspect
from sqlalchemy.engine import Engine

def get_schema_description(engine: Engine) -> str:
    inspector = inspect(engine)
    lines: list[str] = []

    for table_name in inspector.get_table_names():
        cols = inspector.get_columns(table_name)
        col_strs = [f"{c['name']} ({c['type']})" for c in cols]
        lines.append(f"Table {table_name}: " + ", ".join(col_strs))

    return "\n".join(lines)
