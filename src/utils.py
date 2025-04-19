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


def check_server_status(server_address):
    import requests

    try:
        # Use the correct API endpoint and include a User-Agent header
        headers = {"User-Agent": "MinecraftServerChecker/1.0"}
        response = requests.get(f'https://api.mcsrvstat.us/3/{server_address}', headers=headers)
        
        # Ensure the response is valid JSON
        response.raise_for_status()
        data = response.json()

        if data.get('online'):
            player_count = data['players'].get('online', 0)
            player_list = data['players'].get('list', [])
            
            # Extract player names if player_list contains dictionaries
            player_names = [player['name'] if isinstance(player, dict) and 'name' in player else str(player) for player in player_list]
            
            # Print player count and list
            print(f"{player_count} players online for server {server_address}")
            return player_count, player_names
        else:
            print(f"Server {server_address} is offline.")
            return 0, []
    except requests.exceptions.RequestException as e:
        print(f"Error checking server status: {e}")
        return 0, []