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

from mcstatus import JavaServer

def check_server_status(server_address):
    try:
        server = JavaServer.lookup(server_address)
        status = server.status()
        player_count = status.players.online
        # player names may be None if the server doesn't expose them
        player_names = [player.name for player in status.players.sample] if status.players.sample else []
        print(f"{player_count} players online for server {server_address}")
        return player_count, player_names
    except Exception as e:
        print(f"Error checking server status: {e}")
        return 0, []