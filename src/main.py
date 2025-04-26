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
import sys
import time
import json
import datetime
from notifier import Notifier
from utils import check_server_status

def main():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.json')
    log_path = os.path.join(base_dir, 'server_log.txt')

    with open(config_path) as config_file:
        config = json.load(config_file)

    server_address = config['server_address']
    timer = config.get('timer', 300)  # Default to 5 minutes if not specified
    notifier = Notifier(config['notification'])
    list_players = config.get('list_players', False)  # Default to False if not specified

    # Track the previous state of the server
    players_detected = False
    last_player_names = []
    latency_history = []
    max_graph_lines = 0  # Track the max number of lines printed for the graph
    last_logged_player_names = []
    last_logged_latency = None

    while True:
        server_status, player_list, latency = check_server_status(server_address)
        latency_history.append(latency)
        # Cap the ping (latency) list to 20 entries
        if len(latency_history) > 20:
            latency_history = latency_history[-20:]

        # Always extract player_names from player_list and sort alphabetically
        player_names = []
        for player in player_list:
            name = None  # Initialize name to avoid unbound variable
            if isinstance(player, dict):
                name = player.get('name')
            if name is not None:
                player_names.append(str(name))
            else:
                player_names.append(str(player))
        player_names.sort()  # Sort names alphabetically

        # Only log if players changed or latency changed by 200ms+
        log_this = False
        if set(player_names) != set(last_logged_player_names):
            log_this = True
        elif last_logged_latency is not None and abs(latency - last_logged_latency) >= 200:
            log_this = True

        if log_this:
            # Prepare log entry with timestamp
            log_entry = (
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Players: {server_status}, "
                f"Names: {', '.join(player_names) if player_names else 'None'}, "
                f"Latency: {latency} ms\n"
            )

            # Log to file
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
            last_logged_player_names = player_names.copy()
            last_logged_latency = latency

        # Notify if players appear, disappear, or the list changes
        if server_status > 0:
            players_detected = True
            # Compare sets so order doesn't matter
            if set(player_names) != set(last_player_names):
                notifier.send_notification(server_status, player_names if list_players else None)
                last_player_names = player_names.copy()
        else:
            if players_detected:
                players_detected = False
                last_player_names = []
            notifier.send_notification(server_status, None)

        # --- Clear previous graph output ONLY (not player status) ---
        current_graph_lines = len(latency_history) + 5 # 1 for header, 1 for separator
        # sys.stdout.write('\033[F')  # Move cursor up
        sys.stdout.write('\033[F')  # Move cursor up
        sys.stdout.write('\033[F')  # Move cursor up
        if current_graph_lines > max_graph_lines:
            max_graph_lines = current_graph_lines
        for _ in range(max_graph_lines):
            sys.stdout.write('\033[F')  # Move cursor up
            sys.stdout.write('\033[K')  # Clear line

        # --- Print the latest latency graph ---
        print("Latency graph (ms):")
        for l in latency_history:
            print(f"{l:4} ms | {'#' * (l // 10)}")
        console_width = os.get_terminal_size().columns
        print("-" * console_width)

        # Print player status after the graph so it remains visible
        if server_status > 0:
            if list_players and server_status > 1:
                print(f"Players online: {', '.join(player_names) if player_names else 'No players listed'}")
            elif server_status == 1:
                print(f"Player online: {', '.join(player_names) if player_names else 'No players listed'}")

        # Wait for the next check
        for i in range(timer):
            sys.stdout.write(f"\rWaiting {timer - i} seconds before checking again...   ")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write(f"\rChecking now...                                         \n")

if __name__ == "__main__":
    main()