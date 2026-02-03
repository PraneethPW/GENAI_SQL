import os
import asyncio
from app.core.config import settings

# ---------- Gemini setup (WORKING SDK) ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = None

if GEMINI_API_KEY:
    try:
        import google.generativeai as genai  # OLD but works: pip install google-generativeai
        genai.configure(api_key=GEMINI_API_KEY)
        # ✅ FIXED MODEL NAME - works with old SDK
        gemini_model = genai.GenerativeModel("gemini-1.5-flash-001")
    except ImportError:
        print("ERROR: Install google-generativeai: pip install google-generativeai")
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
