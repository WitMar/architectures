from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserForOrderDto(BaseModel):
    user_id: int
    user_name: str

@app.get("/users/{user_id}", response_model=UserForOrderDto)
def get_user(user_id: int):
    return UserForOrderDto(
        user_id=user_id,
        user_name="Marcin"
    )