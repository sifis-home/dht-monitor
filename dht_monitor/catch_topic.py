import json

import requests
import websocket


def on_message(ws, message):
    print("Received:")

    json_message = json.loads(message)

    if "Persistent" in json_message:
        json_message = json_message["Persistent"]

        print("\n\n")
        print("JSON-MESSAGE")
        print(json_message["topic_name"], json_message["topic_uuid"])
        # Send data to Flask server
        data = {
            "topic_name": json_message["topic_name"],
            "topic_uuid": json_message["topic_uuid"],
        }
        url = "http://localhost:4646/topic"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Data sent to Flask server")
        else:
            print("Failed to send data to Flask server")


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("### Connection established ###")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://domhomassistant.duckdns.org:17898/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()
