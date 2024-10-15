# short_poll_client.py
import requests
import time

SERVER_URL = 'http://127.0.0.1:5000'
POLL_INTERVAL = 5  # seconds

def send_message(message):
    response = requests.post(f"{SERVER_URL}/send", json={"message": message})
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print("Failed to send message:", response.json())

def short_polling():
    last = 0
    while True:
        response = requests.get(f"{SERVER_URL}/short_poll", params={"since": last})
        if response.status_code == 200:
            data = response.json()
            new_messages = data.get("messages", [])
            last = data.get("last", last)
            for msg in new_messages:
                print(f"New message: {msg}")
        else:
            print("Error fetching messages:", response.status_code)
        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    import threading

    # Start short polling in a separate thread
    polling_thread = threading.Thread(target=short_polling, daemon=True)
    polling_thread.start()

    # Allow user to send messages
    while True:
        msg = input("Enter message to send (or 'exit' to quit): ")
        if msg.lower() == 'exit':
            break
        send_message(msg)
