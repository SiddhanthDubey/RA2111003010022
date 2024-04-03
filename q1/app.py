import requests
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Global variables
window_size = 10
stored_numbers = []
start_time = time.time()


def fetch_numbers(number_id, access_token):
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"http://20.244.56.144/numbers/{number_id}", headers=headers)
        response.raise_for_status()
        return response.json().get("numbers", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching numbers from test server: {e}")
        return []


def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def update_stored_numbers(new_numbers):
    global stored_numbers
    if len(stored_numbers) >= window_size:
        stored_numbers.pop(0)  # Remove oldest number
    stored_numbers.extend(new_numbers)


def get_window_prev_state():
    global stored_numbers
    return stored_numbers[:]


@app.route('/numbers/<number_id>')
def numbers(number_id):
    global start_time
    # Reset stored_numbers if more than 500 ms elapsed
    if time.time() - start_time > 0.5:
        start_time = time.time()
        stored_numbers.clear()
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzEyMTUyODMwLCJpYXQiOjE3MTIxNTI1MzAsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjJmNTNmMzhkLTQ5MjMtNDAzZC05YjI0LWQ0ZDhhZDEzZmI5MSIsInN1YiI6InNzOTk0MUBzcm1pc3QuZWR1LmluIn0sImNvbXBhbnlOYW1lIjoiS2FudGhpIiwiY2xpZW50SUQiOiIyZjUzZjM4ZC00OTIzLTQwM2QtOWIyNC1kNGQ4YWQxM2ZiOTEiLCJjbGllbnRTZWNyZXQiOiJua3h1U05Cb1NUQUxuZHJHIiwib3duZXJOYW1lIjoiU2lkZGhhbnRoIER1YmV5Iiwib3duZXJFbWFpbCI6InNzOTk0MUBzcm1pc3QuZWR1LmluIiwicm9sbE5vIjoiUkEyMTExMDAzMDEwMDIyIn0.HPwF53a4HRtWal8x6KCI5-Oml_wBkgcaoIGnXsqS4j8"
    numbers = fetch_numbers(number_id, access_token)
    update_stored_numbers(numbers)
    window_prev_state = get_window_prev_state()
    window_curr_state = stored_numbers[:]
    average = calculate_average(window_curr_state)
    response_data = {
        "numbers": window_curr_state,
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "avg": average
    }
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
