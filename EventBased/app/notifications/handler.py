def send_order_confirmation(event):
    print(
        f"Sending notification for done order for {event['user_name']} and product {event['product']}"
    )

