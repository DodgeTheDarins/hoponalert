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
        # headers = ""
        response = requests.get(f'https://api.mcsrvstat.us/3/{server_address}', headers=headers)
        
        # Ensure the response is valid JSON
        response.raise_for_status()
        data = response.json()
        # print(data)

        if data.get('online'):
            player_count = data['players'].get('online')
            print(f"{player_count} players online for server {server_address}")
            # Check if the server is online and return the player count
            return player_count
        else:
            return 0
    except requests.exceptions.RequestException as e:
        print(f"Error checking server status: {e}")
        return 0