def mark_order_as_processed(event, order_repository, outbox_repository=None):
    order_repository.update_status(
        order_id=event["order_id"],
        status="PROCESSED",
    )

    if outbox_repository is None:
        return

    outbox_repository.save(
        {
            "event_name": "OrderProcessed",
            "payload": {
                "order_id": event["order_id"],
                "user_id": event["user_id"],
                "user_name": event["user_name"],
                "product": event["product"],
                "status": "PROCESSED",
            },
            "status": "NEW",
        }
    )


def retract_order(event, order_repository):
    order_repository.update_status(
        order_id=event["order_id"],
        status="RETRACTED",
    )
