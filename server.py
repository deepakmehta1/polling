# server.py
from flask import Flask, request, jsonify
from threading import Event
import time

app = Flask(__name__)

# Shared data structure to hold messages
messages = []
new_message_event = Event()

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')
    if message:
        messages.append(message)
        new_message_event.set()  # Notify waiting long-polling clients
        return jsonify({"status": "Message received"}), 200
    return jsonify({"error": "No message provided"}), 400

@app.route('/short_poll', methods=['GET'])
def short_poll():
    since = int(request.args.get('since', 0))
    # Return messages after the 'since' timestamp/index
    new_msgs = messages[since:]
    return jsonify({"messages": new_msgs, "last": len(messages)}), 200

@app.route('/long_poll', methods=['GET'])
def long_poll():
    since = int(request.args.get('since', 0))
    timeout = 30  # seconds
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if len(messages) > since:
            new_msgs = messages[since:]
            return jsonify({"messages": new_msgs, "last": len(messages)}), 200
        # Wait for a new message or timeout
        if new_message_event.wait(timeout=1):
            new_message_event.clear()
    
    # Timeout without new messages
    return jsonify({"messages": [], "last": len(messages)}), 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
