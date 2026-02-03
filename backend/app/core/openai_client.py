import os
import asyncio
import warnings
from app.core.config import settings

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_model = None

if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        
        # ✅ Use FIRST available Gemini model from your list (strip 'models/' prefix)
        available_models = genai.list_models()
        for model in available_models:
            model_name = model.name.replace("models/", "")  # Remove 'models/' prefix
            if "gemini" in model_name and "latest" not in model_name:  # Pick stable Gemini
                try:
                    gemini_model = genai.GenerativeModel(model_name)
                    print(f"🚀 Using model: {model_name}")
                    break
                except:
                    continue
        
        if not gemini_model:
            print("❌ No suitable Gemini model found")
            
    except Exception as e:
        print(f"❌ Init failed: {e}")

async def generate_sql(schema: str, question: str) -> str:
    from app.prompts import BASE_PROMPT

    if not gemini_model:
        return "ERROR: No Gemini model available"

    prompt = BASE_PROMPT.format(schema=schema, question=question)

    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: gemini_model.generate_content(prompt)
        )
        return response.text.strip().strip("```sql").strip("```").strip()
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return f"ERROR: {str(e)}"
