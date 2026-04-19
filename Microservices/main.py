import argparse
import json

import requests


def run(
    user_id: int = 1,
    product: str = "Laptop",
    users_base_url: str = "http://127.0.0.1:8002",
    orders_base_url: str = "http://127.0.0.1:8001",
) -> dict:
    user_response = requests.get(f"{users_base_url}/users/{user_id}", timeout=5)
    user_response.raise_for_status()
    user_data = user_response.json()

    order_payload = {
        "user_id": user_data["user_id"],
        "user_name": user_data["user_name"],
        "product": product,
    }
    order_response = requests.post(
        f"{orders_base_url}/orders",
        json=order_payload,
        timeout=5,
    )
    order_response.raise_for_status()
    return order_response.json()


def main() -> None:
    result = run(
        user_id=1,
        product="Laptop",
        users_base_url="http://127.0.0.1:8002",
        orders_base_url="http://127.0.0.1:8001",
    )
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
