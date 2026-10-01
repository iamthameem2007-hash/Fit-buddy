from pydantic import BaseModel, Field, field_validator

GOALS = {"Weight loss", "Muscle gain", "General wellness", "Flexibility"}
INTENSITIES = {"Low", "Medium", "High"}

class UserInput(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    user_id: str = Field(min_length=3, max_length=80, pattern=r"^[A-Za-z0-9_-]+$")
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=0, le=350)
    goal: str
    intensity: str

    @field_validator("goal")
    @classmethod
    def valid_goal(cls, value):
        if value not in GOALS:
            raise ValueError("Choose a listed fitness goal.")
        return value

    @field_validator("intensity")
    @classmethod
    def valid_intensity(cls, value):
        if value not in INTENSITIES:
            raise ValueError("Choose low, medium, or high intensity.")
        return value

class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str = Field(min_length=3, max_length=1000)
