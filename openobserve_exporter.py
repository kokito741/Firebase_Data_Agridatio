import time
import base64, json
import requests


def log_to_json(log_line):
    """
    Convert a log line to a JSON string
    :param log_line:
    :return:
    """
    # Split the log line into components
    parts = log_line.split(" - ")

    # Create a dictionary with the log components
    log_dict = {
        "timestamp": parts[0],
        "source": parts[1],
        "level": parts[2],
        "message": parts[3]
    }

    # Convert the dictionary to a JSON string
    json_str = json.dumps(log_dict)

    return json_str


def send_to_openobserve(line):
    """
    Send a log line to OpenObserve
    :param line:
    """
    try:
        user = "kokito741@gmail.com"
        password = "39pYiebC8mKgAxZe"
        bas64encoded_creds = base64.b64encode(bytes(user + ":" + password, "utf-8")).decode("utf-8")
        data = json.loads(log_to_json(line))
        print(data)
        headers = {"Content-type": "application/json", "Authorization": "Basic " + bas64encoded_creds}
        openobserve_host = "http://localhost:5080"
        openobserve_url = openobserve_host + "/api/default/default/_json"

        res = requests.post(openobserve_url, headers=headers, data=json.dumps(data))
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to OpenObserve: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def follow(thefile):
    """
    Generator function that yields new lines in a file
    :param thefile:
    """
    try:
        thefile.seek(0,2)
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line
    except IOError as e:
        print(f"Error reading file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    time.sleep(0.5)
    logfile = open("log.log","r")
    lowliness = follow(logfile)
    for line in lowliness:
        send_to_openobserve(line)
