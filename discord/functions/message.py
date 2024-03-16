# myrax/functions/message.py

import requests

class MessageSender:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = "https://discord.com/api/v10"
        self.headers = {"Authorization": f"Bot {self.bot_token}"}

    def send_message(self, channel_id, content):
        url = f"{self.base_url}/channels/{channel_id}/messages"
        data = {"content": content}
        response = requests.post(url, json=data, headers=self.headers)
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

# Example usage:
# Assuming you have already retrieved the channel ID
# and initialized the bot with a token
# channel_id = "123456789"
# bot_token = "YOUR_BOT_TOKEN"
# message_sender = MessageSender(bot_token)
# message_sender.send_message(channel_id, "Hello, world!")
