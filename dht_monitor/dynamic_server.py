import json
import time
from collections import defaultdict

import requests
import send_data
from flask import Flask, request

app = Flask(__name__)

data_dict = defaultdict(int)
# uuid_dict = defaultdict(int)
last_update_time = time.time()


@app.route("/topic", methods=["POST"])
def receive_data():
    global last_update_time, data_dict  # uuid_dict
    data = request.get_json()
    print("\nDATA:")
    print(data)
    name = data.get("topic_name", None)
    # uuid = data.get('topic_uuid', None)

    if name is not None:
        data_dict[name] += 1
    """
    if uuid is not None:
        uuid_dict[uuid] += 1
    """
    if time.time() - last_update_time >= 10:
        with open("log_name.json", "a") as f:
            try:
                requests.post(
                    "http://localhost:4545/dht_data",
                    json=json.dumps(data_dict),
                )
            except:
                pass
            json.dump(dict(data_dict), f)
            f.write("\n")
            print("Sending DATA to SYSTEM PROTECTION MANAGER ...")
            send_data.send_data(data_dict)
        """
        with open('log_uuid.json', 'a') as u:
            json.dump(dict(uuid_dict), u)
            u.write('\n')
        """
        data_dict = defaultdict(int)
        # uuid_dict = defaultdict(int)
        last_update_time = time.time()

    # return response
    return "OK"


if __name__ == "__main__":
    app.run("0.0.0.0", port="4747")
