class User:
    def __init__(self, user_id: int, name: str, email: str, roles: list[str]):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.roles = roles

