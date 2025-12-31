from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_sql(schema: str, question: str) -> str:
    from app.prompts import BASE_PROMPT

    prompt = BASE_PROMPT.format(schema=schema, question=question)

    resp =  client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write safe, read-only SQL for PostgreSQL."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )
    sql = resp.choices[0].message.content or ""
    return sql.strip().strip("```sql").strip("```").strip()
