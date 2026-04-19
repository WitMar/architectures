import json

import requests
from fastapi import HTTPException
from pydantic import ValidationError


def run(
        user_id: int = 1,
        product: str = "Laptop",
        orders_base_url: str = "http://127.0.0.1:8001",
) -> dict:
    try:
        order_payload = {
            "user_id": user_id,
            "product": product,
        }
        order_response = requests.post(
            f"{orders_base_url}/orders",
            json=order_payload,
            timeout=5,
        )
        order_response.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Users service unavailable")
    except ValidationError:
        raise HTTPException(status_code=502, detail="Invalid response from users service")

    return order_response.json()


def main() -> None:
    result = run(
        user_id=1,
        product="Laptop",
        orders_base_url="http://127.0.0.1:8001",
    )
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
