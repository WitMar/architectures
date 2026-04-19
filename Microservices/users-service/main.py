from fastapi import FastAPI

app = FastAPI(title="Users Service")


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "user_name": "Marcin",
    }

