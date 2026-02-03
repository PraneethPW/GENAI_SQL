import os
import asyncio
from app.core.config import settings

# ---------- Gemini setup (DEPRECATION SUPPRESSED + CORRECT MODEL) ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = None

if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        # Suppress deprecation warning
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        # ✅ CORRECT MODELS for old SDK (list them and pick first working one)
        candidate_models = [
            "gemini-1.5-flash",
            "gemini-pro",
            "gemini-1.0-pro",
            "gemini-1.5-pro"
        ]
        
        for model_name in candidate_models:
            try:
                gemini_model = genai.GenerativeModel(model_name)
                print(f"✅ Successfully loaded: {model_name}")
                break
            except Exception as model_error:
                print(f"❌ Model {model_name} failed: {model_error}")
                continue
        
        if not gemini_model:
            print("❌ No working Gemini models found")
            
    except ImportError:
        print("ERROR: Install google-generativeai: pip install google-generativeai")
    except Exception as e:
        print(f"Gemini init failed: {e}")

async def generate_sql(schema: str, question: str) -> str:
    from app.prompts import BASE_PROMPT

    if not gemini_model:
        return "ERROR: Gemini model not available"

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
