import os
import asyncio
from app.core.config import settings

# ---------- Gemini setup (NEW UNIFIED SDK) ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = None

if GEMINI_API_KEY:
    try:
        import google.genai as genai  # New SDK: pip install google-genai
        genai.configure(api_key=GEMINI_API_KEY)
        # Latest stable model (verify at https://ai.google.dev/gemini-api/docs/models/gemini)
        gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")
    except ImportError:
        print("ERROR: Install google-genai: pip install google-genai")
    except Exception as e:
        print(f"Gemini init failed: {e}")

async def generate_sql(schema: str, question: str) -> str:
    from app.prompts import BASE_PROMPT

    if not gemini_model:
        return "ERROR: Gemini not initialized (check GEMINI_API_KEY)"

    prompt = BASE_PROMPT.format(schema=schema, question=question)

    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: gemini_model.generate_content(
                f"You write safe, read-only SQL for PostgreSQL.\n\n{prompt}"
            )
        )
        return response.text.strip().strip("```sql").strip("```").strip()
    except Exception as e:
        print(f"Gemini SQL generation failed: {e}")
        return f"ERROR: SQL generation failed - {str(e)}"
