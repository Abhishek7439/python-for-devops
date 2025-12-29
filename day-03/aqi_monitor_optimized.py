import logging
import json
from datetime import datetime
import requests
from pathlib import Path


API_KEY = "17cb43569d35cbdaef8771376187499af800edf4925267b4a0513e9af202d54c"
BASE_URL = "https://api.ambeedata.com/latest/by-city"
LOG_FILE = "aqi_results.json"


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )


def fetch_aqi(city):
    try:
        headers = {
            "x-api-key": API_KEY,
            "Content-type": "application/json"
        }

        params = {"city": city}

        response = requests.get( BASE_URL, headers=headers, params=params, timeout=10 )

        response.raise_for_status()
        data = response.json()

        if not data.get("stations"):
            logging.warning("API returned no stations for this city.")
            return None

        return data["stations"][0]

    except requests.exceptions.Timeout:
        logging.error("Request timeout — network may be slow.")
    except requests.exceptions.ConnectionError:
        logging.error("Network error — please check your internet.")
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP Error: {err}")
    except ValueError:
        logging.error("Invalid JSON response from API.")
    except Exception as err:
        logging.error(f"Unexpected error: {err}")

    return None


def classify_aqi(aqi):
    if aqi is None:
        return "AQI unavailable"

    if aqi <= 50:
        return "🟢 Good — Safe to breathe"
    if aqi <= 100:
        return "🟡 Moderate — Acceptable"
    if aqi <= 200:
        return "🟠 Unhealthy for sensitive people"

    return "🔴 Unhealthy — Limit outdoor activity"


def save_to_json(record):
    """Append AQI data to a JSON file safely."""
    try:
        path = Path(LOG_FILE)

        if path.exists():
            with open(path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(record)

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Saved AQI record to {LOG_FILE}")

    except OSError as err:
        logging.error(f"File write error: {err}")
    except ValueError:
        logging.error("JSON formatting error while saving data.")


def print_report(city, station):
    if not station:
        print("\nUnable to fetch AQI data right now.")
        return

    aqi = station.get("AQI")
    state = station.get("state", "N/A")
    country = station.get("countryCode", "N/A")

    status = classify_aqi(aqi)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("\n========== AQI REPORT ==========")
    print(f"Location : {city.title()}, {state}, {country}")
    print(f"Time     : {timestamp}")
    print(f"AQI      : {aqi}")
    print(f"Status   : {status}")
    print("================================\n")

    # prepare data to store
    record = {
        "city": city.title(),
        "state": state,
        "country": country,
        "aqi": aqi,
        "status": status,
        "timestamp": timestamp,
    }

    save_to_json(record)


def main():
    setup_logging()

    print("\n🌍 Real-Time AQI Monitor\n")

    city = input("Enter city name : ").strip()

    if not city:
        print("Please enter a valid city name.")
        return

    logging.info(f"Fetching AQI for city: {city}")

    station = fetch_aqi(city)

    print_report(city, station)


if __name__ == "__main__":
    main()
