class Notification:
        title: str
        body: str

        def __init__(self, notification_dict):
            self.title = notification_dict.get("title")
            self.body = notification_dict.get("body")
        
        def as_dict(self):
            return {
                "title": self.title,
                "body": self.body
            }

class RemoteMessage:
    notification: Notification = None # None when message originates from notification click
    data: dict = {}
    message_id: str = ""
    sent_time: int = 0
    from_: str = ""
    ttl: int = 0

    def __init__(self, push_notification: dict):
        # Check if it's a notification click
        if push_notification.get("notification") is None:
            self.sent_time = push_notification.pop("google.sent_time")
            self.from_ = push_notification.pop("from")
            self.message_id = push_notification.pop("google.message_id")
            self.ttl = push_notification.pop("google.ttl")
            # Remove the unused keys, leaving only user data
            for e in ["collapse_key", "google.original_priority", "google.delivered_priority", "gcm.n.analytics_data"]:
                push_notification.pop(e)
            self.data = push_notification
        else:
            self.notification = Notification(push_notification["notification"])
            self.data = push_notification.get("data")
            self.message_id = push_notification.get("messageId")
            self.from_ = push_notification.get("from")
            self.ttl = push_notification.get("ttl")
            self.sent_time = push_notification.get("sentTime")
    
    def as_dict(self):
        notif = {}
        if self.notification is not None:
            notif = self.notification.as_dict()
        return {
            "notification": notif,
            "data": self.data,
            "message_id": self.message_id,
            "sent_time": self.sent_time,
            "from": self.from_,
            "ttl": self.ttl
        }
    
    def __repr__(self):
        return str(self.as_dict())
