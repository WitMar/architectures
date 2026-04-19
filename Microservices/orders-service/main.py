from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Orders Service")


class CreateOrderRequest(BaseModel):
    user_id: int
    user_name: str
    product: str


@app.post("/orders")
def create_order(request: CreateOrderRequest):
    return {
        "user_id": request.user_id,
        "user_name": request.user_name,
        "product": request.product,
    }

