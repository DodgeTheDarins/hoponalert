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

import os
import time
import json
from notifier import Notifier
from utils import check_server_status

def main():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.json')

    with open(config_path) as config_file:
        config = json.load(config_file)

    server_address = config['server_address']
    notifier = Notifier(config['notification'])

    # Track the previous state of the server
    players_detected = False

    while True:
        server_status = check_server_status(server_address)

        if server_status > 0:
            if not players_detected:
                # Send notification only if players were not previously detected
                notifier.send_notification(server_status)
                players_detected = True
        else:
            # Reset the flag when no players are detected
            players_detected = False

        time.sleep(300)  # Wait for 5 minutes

if __name__ == "__main__":
    main()