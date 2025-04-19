# Minecraft Server Checker

This project is a simple application that checks the status of a Minecraft server every 5 minutes using the mcsrvstat.us API. It sends notifications when there are active players on the server.

## Features

- Periodically checks the Minecraft server status.
- Sends notifications when players are online.
- Configurable server address and notification settings.

## Project Structure

```
minecraft-server-checker
├── src
│   ├── main.py          # Entry point of the application
│   ├── notifier.py      # Handles sending notifications
│   └── utils.py         # Utility functions for server status checks
├── requirements.txt     # Project dependencies
├── config.json          # Configuration settings
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd minecraft-server-checker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the `config.json` file with your Minecraft server address and notification settings.

## Usage

Run the application using:
```
python src/main.py
```

The application will check the server status every 5 minutes and send notifications if there are active players.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.