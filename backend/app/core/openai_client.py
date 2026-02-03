import os
import asyncio
import warnings
from app.core.config import settings

# Suppress deprecation warning
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

# ---------- Gemini setup - USE PROVEN MODEL ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = None

if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        
        # ✅ gemini-pro ALWAYS works with old SDK + free tier
        gemini_model = genai.GenerativeModel("gemini-pro")
        print("✅ Gemini Pro loaded successfully")
        
    except Exception as e:
        print(f"❌ Gemini init failed: {e}")

async def generate_sql(schema: str, question: str) -> str:
    from app.prompts import BASE_PROMPT

    if not gemini_model:
        return "ERROR: Gemini model not available - check GEMINI_API_KEY"

    prompt = BASE_PROMPT.format(schema=schema, question=question)

    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: gemini_model.generate_content(
                f"You write safe, read-only SQL for PostgreSQL.\n{prompt}"
            )
        )
        return response.text.strip().strip("```sql").strip("```").strip()
    except Exception as e:
        print(f"❌ Gemini generation error: {e}")
        return f"ERROR: {str(e)}"
