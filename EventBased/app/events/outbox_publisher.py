class OutboxPublisher:
    def __init__(self, outbox_repository, event_bus):
        self.outbox_repository = outbox_repository
        self.event_bus = event_bus

    def publish_pending_events(self):
        published_count = 0
        for message in self.outbox_repository.get_new_messages():
            print("Event published to BUS")
            self.event_bus.publish(message["event_name"], message["payload"])
            self.outbox_repository.mark_as_published(message)
            published_count += 1
        return published_count
