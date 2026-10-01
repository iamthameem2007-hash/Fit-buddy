from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserInput
from app import crud
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app.config import ADMIN_USERNAME, ADMIN_PASSWORD

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"error": None})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = UserInput(username=username.strip(), user_id=user_id.strip(), age=age,
                         weight=weight, goal=goal, intensity=intensity)
        user = crud.save_user(db, data)
        workout = generate_workout_gemini(user)
        tip = generate_nutrition_tip_with_flash(user.goal)
        plan = crud.save_plan(db, user.user_id, workout, tip)
        return templates.TemplateResponse(request=request, name="result.html", context={
            "user": user, "plan": plan, "workout_plan": workout, "nutrition_tip": tip,
            "message": None, "error": None
        })
    except ValueError as exc:
        return templates.TemplateResponse(request=request, name="index.html",
            context={"error": str(exc)}, status_code=422)
    except Exception as exc:
        return templates.TemplateResponse(request=request, name="index.html",
            context={"error": f"Could not generate your plan: {exc}"}, status_code=500)

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str = Form(...),
                    feedback: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id.strip())
    plan = crud.get_latest_plan(db, user_id.strip())
    if not user or not plan:
        return templates.TemplateResponse(request=request, name="index.html",
            context={"error": "User ID or workout plan was not found. Generate a plan first."},
            status_code=404)
    try:
        updated = update_workout_plan(plan.original_plan, feedback.strip(), user)
        crud.update_plan(db, plan, updated, feedback.strip())
        return templates.TemplateResponse(request=request, name="result.html", context={
            "user": user, "plan": plan, "workout_plan": updated,
            "nutrition_tip": plan.nutrition_tip, "message": "Your plan has been updated.",
            "error": None
        })
    except Exception as exc:
        return templates.TemplateResponse(request=request, name="result.html", context={
            "user": user, "plan": plan, "workout_plan": plan.original_plan,
            "nutrition_tip": plan.nutrition_tip, "message": None,
            "error": f"Could not update plan: {exc}"
        }, status_code=500)

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    # Local-development dashboard. Protect this route with a real auth system before deployment.
    users = crud.get_all_users(db)
    plans = crud.get_all_plans(db)
    plans_by_user = {}
    for plan in plans:
        plans_by_user.setdefault(plan.user_id, []).append(plan)
    return templates.TemplateResponse(request=request, name="all_users.html",
        context={"users": users, "plans_by_user": plans_by_user})

@router.post("/delete-user/{user_id}")
def remove_user(user_id: str, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return RedirectResponse(url="/view-all-users", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/health")
def health():
    return {"status": "ok", "application": "FitBuddy"}
