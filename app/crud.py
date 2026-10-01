from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User, WorkoutPlan

def save_user(db: Session, data):
    user = db.scalar(select(User).where(User.user_id == data.user_id))
    if user:
        user.username, user.age, user.weight = data.username, data.age, data.weight
        user.goal, user.intensity = data.goal, data.intensity
    else:
        user = User(**data.model_dump())
        db.add(user)
    db.commit()
    db.refresh(user)
    return user

def save_plan(db: Session, user_id, workout_plan, nutrition_tip):
    plan = WorkoutPlan(user_id=user_id, original_plan=workout_plan, nutrition_tip=nutrition_tip)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

def get_user(db: Session, user_id):
    return db.scalar(select(User).where(User.user_id == user_id))

def get_latest_plan(db: Session, user_id):
    return db.scalar(select(WorkoutPlan).where(WorkoutPlan.user_id == user_id).order_by(WorkoutPlan.id.desc()))

def get_original_plan(db: Session, user_id):
    plan = get_latest_plan(db, user_id)
    return plan.original_plan if plan else None

def update_plan(db: Session, plan, updated_text, feedback):
    plan.updated_plan = updated_text
    plan.feedback = feedback
    plan.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(plan)
    return plan

def get_all_users(db: Session):
    return db.scalars(select(User).order_by(User.created_at.desc())).all()

def get_all_plans(db: Session):
    return db.scalars(select(WorkoutPlan).order_by(WorkoutPlan.id.desc())).all()

def delete_user(db: Session, user_id):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
