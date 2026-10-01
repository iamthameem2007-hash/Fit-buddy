# FitBuddy — AI Fitness Plan Generator

A local FastAPI + Jinja2 + SQLite application based on the supplied FitBuddy project documentation. It generates 7-day workout plans, goal-based general nutrition/recovery tips, and feedback-based plan revisions with Google's Gemini API.

## Requirements
- Python 3.11 or newer (64-bit recommended)
- VS Code and Python extension
- Gemini API key from Google AI Studio

## VS Code setup (Windows PowerShell)
1. Extract the project ZIP and open the `FitBuddy` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```bat
   .venv\\Scripts\\activate.bat
   ```
   Or use the environment's Python directly: `.venv\\Scripts\\python.exe -m pip install -r requirements.txt`.
4. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` in the project root. Put your real key after `GOOGLE_API_KEY=`.
6. Start the app from the project root:
   ```powershell
   uvicorn app.main:app --reload
   ```
7. Open:
   - Web app: http://127.0.0.1:8000
   - API docs: http://127.0.0.1:8000/docs
   - Health check: http://127.0.0.1:8000/health
   - Local coach dashboard: http://127.0.0.1:8000/view-all-users

## Testing the features
1. On the homepage, enter a name, unique user ID (letters/numbers/underscore/hyphen), age, weight, goal and intensity.
2. Click **Generate my 7-day plan**. The first request calls Gemini for the plan and tip; internet access and a valid API key are required.
3. On the result page, enter feedback and submit to request a revised plan. The revised version is saved separately from the original.
4. Visit the coach dashboard to view user records and both plan versions.
5. Test `GET /health` and browse endpoints in `/docs`.

## Troubleshooting
- `GOOGLE_API_KEY is missing`: confirm `.env` exists in the project root and contains the key, then restart Uvicorn.
- Model/API errors: verify the key, billing/quota, network, and model availability in your Google AI Studio account. Set `GEMINI_WORKOUT_MODEL` and `GEMINI_TIP_MODEL` in `.env` to a model enabled for your key.
- `uvicorn is not recognized`: activate `.venv`, reinstall requirements, or run `python -m uvicorn app.main:app --reload`.
- Port 8000 busy: run `uvicorn app.main:app --reload --port 8001`.
- Database: SQLite file `fitbuddy.db` is created automatically in the project root.

## Security notes before deployment
This is a local educational starter project. The coach dashboard and delete route are intentionally unauthenticated to match the documentation's feature demonstration. Do not deploy publicly until you add admin authentication, authorization, CSRF protection, rate limiting, HTTPS, secure secret management, and privacy/retention controls. User IDs are identifiers, not authentication credentials.

Fitness output is general informational content and is not medical advice. Users should choose comfortable activities and consult qualified professionals for injuries or health concerns.
