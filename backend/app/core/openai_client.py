import os
import asyncio
from app.core.config import settings

# ---------- Gemini setup ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = None

if GEMINI_API_KEY:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- OpenAI setup ----------
from openai import OpenAI
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_sql(schema: str, question: str) -> str:
    from app.prompts import BASE_PROMPT

    prompt = BASE_PROMPT.format(schema=schema, question=question)

    # 🟢 Prefer Gemini if available (ASYNC SAFE)
    if gemini_model:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: gemini_model.generate_content(
                f"You write safe, read-only SQL for PostgreSQL.\n\n{prompt}"
            )
        )
        return response.text.strip().strip("```sql").strip("```").strip()

    # 🔵 Fallback to OpenAI
    resp = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write safe, read-only SQL for PostgreSQL."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    sql = resp.choices[0].message.content or ""
    return sql.strip().strip("```sql").strip("```").strip()
