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