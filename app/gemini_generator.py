from google import genai

from app.config import GOOGLE_API_KEY, GEMINI_WORKOUT_MODEL


def generate_workout_gemini(user):
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "Gemini API key is missing. Add GOOGLE_API_KEY to your .env file."
        )

    prompt = f"""
Create a safe, beginner-conscious, general wellness 7-day fitness plan.

User profile: age {user.age}, weight {user.weight} kg, goal {user.goal},
preferred intensity {user.intensity}.

Return readable plain text with Day 1 through Day 7. For each day include:
focus, 5-10 minute warm-up, exercises with sets/reps or duration, and cool-down.

Include appropriate recovery/rest days and low-impact alternatives.

Do not prescribe extreme exercise, rapid weight loss, calorie targets, supplements,
or medical treatment. Advise stopping if pain, dizziness, or unusual symptoms occur.

Keep the plan adaptable and mention that a qualified professional should advise users
with health concerns or injuries.
"""

    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model=GEMINI_WORKOUT_MODEL,
        contents=prompt,
    )

    text = (response.text or "").strip()

    if not text:
        raise RuntimeError("Gemini returned an empty workout plan.")

    return text