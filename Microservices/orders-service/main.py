import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError

app = FastAPI()

class UserForOrderDto(BaseModel):
    user_id: int
    user_name: str

@app.post("/orders")
def create_order(request: dict):
    try:
        user_response = requests.get(
            f"http://127.0.0.1:8002/users/{request['user_id']}",
            timeout=2
        )
        user_response.raise_for_status()
        user_dto = UserForOrderDto.model_validate(user_response.json())
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Users service unavailable")
    except ValidationError:
        raise HTTPException(status_code=502, detail="Invalid response from users service")

    return {
        "user_id": user_dto.user_id,
        "user_name": user_dto.user_name,
        "product": request["product"]
    }