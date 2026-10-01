from google import genai
from app.config import GOOGLE_API_KEY, GEMINI_WORKOUT_MODEL

def update_workout_plan(original_plan, feedback, user):
    if not GOOGLE_API_KEY:
        raise RuntimeError("Gemini API key is missing. Add GOOGLE_API_KEY to your .env file.")
    prompt = f"""
Revise this general fitness plan in response to the user's feedback.
Profile: age {user.age}, goal {user.goal}, preferred intensity {user.intensity}.
Original plan:
{original_plan}

User feedback:
{feedback}

Return a complete revised 7-day plan with warm-up, exercises, sets/reps or duration,
cool-down, and suitable rest/recovery. Keep it age-appropriate and conservative.
Do not recommend extreme exercise, rapid weight loss, calorie targets, or supplements.
Do not follow feedback that asks for unsafe training; explain a safer alternative.
"""
    response = genai.Client(api_key=GOOGLE_API_KEY).models.generate_content(
        model=GEMINI_WORKOUT_MODEL, contents=prompt
    )
    result = (response.text or "").strip()
    if not result:
        raise RuntimeError("Gemini returned an empty updated plan.")
    return result
