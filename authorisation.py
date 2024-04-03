import requests
import json
import logging

# created logger to make the debugging easy
logging.basicConfig(level=logging.INFO)


def request_to_authorise(url, data):
    try:
        response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Error making POST request: %s", e)
        return None


def saving_response(response, notebook_filename):
    try:
        with open(notebook_filename, 'w') as notebook_file:
            json.dump(response, notebook_file, indent=4)
        logging.info("Response saved to %s", notebook_filename)
    except IOError as e:
        logging.error("Error saving response to notebook: %s", e)


def main():
    url = "http://20.244.56.144/test/auth"
    data = {
        "companyName": "Kanthi",
        "clientID": "2f53f38d-4923-403d-9b24-d4d8ad13fb91",
        "clientSecret": "nkxuSNBoSTALndrG",
        "ownerName": "Siddhanth Dubey",
        "ownerEmail": "ss9941@srmist.edu.in",
        "rollNo": "RA2111003010022"
    }
    response = request_to_authorise(url, data)
    if response:
        saving_response(response, "auth_notebook.json")


if __name__ == "__main__":
    main()
