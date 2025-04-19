from plyer import notification

class Notifier:
    def __init__(self, notification_config):
        self.notification_config = notification_config

    def send_notification(self, active_players):
        message = f"Active players detected: {active_players}"
        notification.notify(
            title="Minecraft Server Checker",
            message=message,
            app_name="Minecraft Server Checker",
            timeout=10  # Notification will disappear after 10 seconds
        )