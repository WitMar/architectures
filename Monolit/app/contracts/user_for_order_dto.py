from dataclasses import dataclass

@dataclass
class UserForOrderDto:
    user_id: int
    user_name: str
    user_email: str