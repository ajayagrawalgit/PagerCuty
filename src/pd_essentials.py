import yaml
import requests
import datetime
from tabulate import tabulate
import pdpyras


# Reading the Config file for all the Secret Details
def read_config():
    with open("config.yaml", "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        return config.get("pagerduty", {})
    

def format_incident_table(incidents):
    # Prepare incident data for tabulation
    incident_data = []
    for incident in incidents:
        assigned_to = ", ".join([assignment["assignee"]["summary"] for assignment in incident.get("assignments", [])])
        incident_data.append([
            incident['id'],
            incident['title'],
            incident['status'],
            assigned_to,
            incident['html_url']
        ])

    # Create a table with left-aligned contents
    table_headers = ["Incident ID", "Title", "Status", "Assigned To", "URL"]
    table = tabulate(incident_data, headers=table_headers, tablefmt="pretty", stralign="left")

    return table


# Getting User ID using the Email ID Provided in config.yaml
def get_user_id(user_email, headers):
    BASE_URL = f"https://api.pagerduty.com/users"
    params = {"query": user_email}
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        users = response.json().get("users", [])
        if users:
            return users[0]["id"]
    else:
        print(f"Failed to fetch user details for email {user_email}. Status code: {response.status_code}")
        print(response.text)
    return None


# Function to authorize requests and get headers
def authorize(api_token):
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": f"Token token={api_token}",
    }
    return headers


def get_user_name(user_email,headers):
    BASE_URL = "https://api.pagerduty.com/users"
    params = {"query": user_email}

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code == 200:
            users = response.json().get("users", [])
            if users:
                return users[0]["name"]
            else:
                print(f"No user found with email: {user_email}")
                return None
        else:
            print(f"Failed to fetch user details for email {user_email}. Status code: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_the_date():
    # Get the current date and time in the system's timezone
    current_datetime = datetime.datetime.now().astimezone()

    # Format the date
    formatted_date = current_datetime.strftime('%d-%B-%Y')

    # Format the time with TimeZone abbreviation
    formatted_time = current_datetime.strftime('( %H:%M %Z )')

    # Combine and return the formatted date and time
    formatted_datetime = f"{formatted_date} {formatted_time}"
    return formatted_datetime

