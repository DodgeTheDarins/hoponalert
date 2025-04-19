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