# long_poll_client.py
import requests
import time

SERVER_URL = 'http://127.0.0.1:5000'

def send_message(message):
    response = requests.post(f"{SERVER_URL}/send", json={"message": message})
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print("Failed to send message:", response.json())

def long_polling():
    last = 0
    while True:
        try:
            response = requests.get(f"{SERVER_URL}/long_poll", params={"since": last}, timeout=35)
            if response.status_code == 200:
                data = response.json()
                new_messages = data.get("messages", [])
                last = data.get("last", last)
                for msg in new_messages:
                    print(f"New message: {msg}")
            else:
                print("Error fetching messages:", response.status_code)
        except requests.exceptions.Timeout:
            print("Long polling request timed out. Retrying...")

if __name__ == '__main__':
    import threading

    # Start long polling in a separate thread
    polling_thread = threading.Thread(target=long_polling, daemon=True)
    polling_thread.start()

    # Allow user to send messages
    while True:
        msg = input("Enter message to send (or 'exit' to quit): ")
        if msg.lower() == 'exit':
            break
        send_message(msg)
