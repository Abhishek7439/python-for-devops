import requests
import json

# URLs
ACTIVE_URL = "https://www.githubstatus.com/api/v2/incidents/unresolved.json"
HISTORY_URL = "https://www.githubstatus.com/api/v2/incidents.json"


def get_incident_data(url):
    """API call + JSON parse with error handling."""
    try:
        response = requests.get(url=url, timeout=10)
        response.raise_for_status()  # raises HTTPError

        data = response.json()

        # json ke andar 'incidents' ek KEY hai
        return data.get("incidents", [])

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
        return []

    except ValueError:
        print("JSON parsing failed.")
        return []


def process_incidents(incidents):
    """Extract only useful fields."""
    cleaned_data = []

    for inc in incidents:
        record = {
            "name": inc.get("name"),
            "impact": inc.get("impact"),
            "status": inc.get("status"),
            "created_at": inc.get("created_at"),
            "link": inc.get("shortlink"),
        }
        cleaned_data.append(record)

    return cleaned_data


def save_to_file(data, filename):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")
    except OSError as error:
        print(f"File save failed: {error}")


def main():
    print("\nFetching ACTIVE incidents...")

    active = get_incident_data(ACTIVE_URL)
    active_processed = process_incidents(active)

    if len(active_processed) == 0:
        print("No active incidents  — sab theek chal raha hai")
    else:
        print(f"Active Incidents: {len(active_processed)}")

        for inc in active_processed[:5]:
            print("\nTitle:", inc["name"])
            print("Impact:", inc["impact"])
            print("Status:", inc["status"])
            print("Link:", inc["link"])

    save_to_file(active_processed, "active_incidents.json")

    print("\nFetching HISTORICAL incidents...")

    history = get_incident_data(HISTORY_URL)
    history_processed = process_incidents(history)

    print(f"Total historical incidents: {len(history_processed)}")

    for inc in history_processed[:5]:
        print("\nTitle:", inc["name"])
        print("Impact:", inc["impact"])
        print("Status:", inc["status"])
        print("Link:", inc["link"])

    save_to_file(history_processed, "historical_incidents.json")


if __name__ == "__main__":
    main()
