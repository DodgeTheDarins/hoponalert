# This file is part of Minecraft Server Checker.
#
# Minecraft Server Checker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Minecraft Server Checker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Minecraft Server Checker. If not, see <https://www.gnu.org/licenses/>.


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
        ) # type: ignore