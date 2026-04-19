from Heksagonal.app.ports.user_query_port import UserQueryPort


class InMemoryUserAdapter(UserQueryPort):
    def get_user_for_order(self, user_id: int):
        return {
            "user_id": user_id,
            "user_name": "Marcin",
        }

