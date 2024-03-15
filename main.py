import requests

class Myrax:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://discord.com/api/v10"
        self.headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }

    def send_message(self, channel_id, content):
        url = f"{self.base_url}/channels/{channel_id}/messages"
        data = {"content": content}
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
