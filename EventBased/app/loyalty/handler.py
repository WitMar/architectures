saved_points = []
should_fail_to_save_points = False


def points_were_already_added(order_id):
    return any(point["source_order_id"] == order_id for point in saved_points)


def save_points(user_id, points, source_order_id):
    if should_fail_to_save_points:
        raise RuntimeError("Could not save loyalty points")

    print(f"Saving points for user {user_id} order id {source_order_id}")
    saved_points.append(
        {
            "user_id": user_id,
            "points": points,
            "source_order_id": source_order_id,
        }
    )


def register_loyalty_points(event, outbox_repository=None):
    order_id = event["order_id"]
    if points_were_already_added(order_id):
        return

    user_id = event["user_id"]
    points_to_add = event["points_to_add"]

    try:
        save_points(
            user_id=user_id,
            points=points_to_add,
            source_order_id=order_id,
        )
    except RuntimeError as error:
        if outbox_repository is None:
            return

        outbox_repository.save(
            {
                "event_name": "LoyaltyPointsSaveFailed",
                "payload": {
                    "order_id": order_id,
                    "user_id": user_id,
                    "user_name": event["user_name"],
                    "product": event["product"],
                    "reason": str(error),
                },
                "status": "NEW",
            }
        )
        return

    if outbox_repository is None:
        return

    outbox_repository.save(
        {
            "event_name": "LoyaltyPointsAdded",
            "payload": {
                "order_id": order_id,
                "user_id": user_id,
                "user_name": event["user_name"],
                "product": event["product"],
                "points_added": points_to_add,
            },
            "status": "NEW",
        }
    )
