from google import genai
from app.config import GOOGLE_API_KEY, GEMINI_TIP_MODEL


def generate_nutrition_tip_with_flash(goal):
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "Gemini API key is missing. Add GOOGLE_API_KEY to your .env file."
        )

    prompt = f"""
Give one concise, practical, age-appropriate nutrition or recovery tip for the
fitness goal: {goal}. Use general balanced-food and hydration guidance.
Do not prescribe calorie restriction, supplements, or medical treatment.
Avoid weight-shaming and include no more than 100 words.
"""

    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model=GEMINI_TIP_MODEL,
        contents=prompt,
    )

    return (response.text or "").strip() or (
        "Choose balanced meals, drink water regularly, and allow time for recovery."
    )