# onjoin.py

import requests

class OnJoinListener:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = "https://discord.com/api/v10"
        self.headers = {"Authorization": f"Bot {self.bot_token}"}

    def start_listening(self):
        print("Listening for member join events...")
        while True:
            event = self.get_event()
            if event and event['type'] == 'GUILD_MEMBER_ADD':
                guild_id = event['guild_id']
                member = event['member']
                print(f"{member['user']['username']} joined a guild with ID {guild_id}")

    def get_event(self):
        response = requests.get(f"{self.base_url}/gateway/bot", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            gateway_url = data['url']
            event_response = requests.get(f"{gateway_url}/events", headers=self.headers)
            if event_response.status_code == 200:
                return event_response.json()
        print("Failed to fetch event.")
        return None
