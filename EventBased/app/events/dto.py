from dataclasses import dataclass

@dataclass
class OrderCreatedDto:
    order_id: int
    user_id: int
    user_name: str
    product: str
    points_to_add: int

