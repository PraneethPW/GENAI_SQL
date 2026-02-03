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
        
        # 🔍 LIST ALL AVAILABLE MODELS FOR YOUR API KEY
        print("🔍 Available models:")
        for model in genai.list_models():
            print(f"  - {model.name}")
        
        # Try the OLDEST, most universal model names
        working_models = []
        for model_name in ["gemini-1.0-pro", "models/gemini-1.0-pro", "gemini-pro", "text-bison"]:
            try:
                test_model = genai.GenerativeModel(model_name)
                working_models.append(model_name)
                print(f"✅ WORKING: {model_name}")
                gemini_model = test_model
                break
            except:
                continue
        
        if gemini_model:
            print(f"🚀 Using model: {working_models[0]}")
        else:
            print("❌ NO MODELS WORK - Check GEMINI_API_KEY permissions")
            
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
