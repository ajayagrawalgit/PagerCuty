"""Core functionality and utilities for PagerDuty operations.

This module provides essential functions for interacting with the PagerDuty API,
including configuration management, user authentication, and data formatting.
"""

from typing import Dict, List, Optional
import datetime
import yaml
import requests
from tabulate import tabulate


def read_config() -> Dict:
    """Read and parse the YAML configuration file.

    Returns:
        Dict: Configuration settings from the 'pagerduty' section

    Raises:
        FileNotFoundError: If config.yaml is not found
        yaml.YAMLError: If the YAML file is malformed
    """
    try:
        with open("config.yaml", "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            return config.get("pagerduty", {})
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file 'config.yaml' not found")
    except yaml.YAMLError as exc:
        raise yaml.YAMLError(f"Error parsing config.yaml: {exc}")


def format_incident_table(incidents: List[Dict]) -> str:
    """Format incident data into a pretty table.

    Args:
        incidents: List of incident dictionaries from PagerDuty API

    Returns:
        str: Formatted table string
    """
    incident_data = []
    for incident in incidents:
        assigned_to = ", ".join(
            assignment["assignee"]["summary"]
            for assignment in incident.get("assignments", [])
        )
        incident_data.append([
            incident['id'],
            incident['title'],
            incident['status'],
            assigned_to,
            incident['html_url']
        ])

    table_headers = ["Incident ID", "Title", "Status", "Assigned To", "URL"]
    return tabulate(
        incident_data,
        headers=table_headers,
        tablefmt="pretty",
        stralign="left"
    )


def get_user_id(user_email: str, headers: Dict) -> Optional[str]:
    """Retrieve PagerDuty user ID for a given email.

    Args:
        user_email: User's email address
        headers: API request headers

    Returns:
        Optional[str]: User ID if found, None otherwise
    """
    base_url = "https://api.pagerduty.com/users"
    params = {"query": user_email}

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()

        users = response.json().get("users", [])
        return users[0]["id"] if users else None

    except requests.exceptions.RequestException as exc:
        print(f"Failed to fetch user details for {user_email}: {exc}")
        return None


def authorize(api_token: str) -> Dict[str, str]:
    """Create authorization headers for PagerDuty API requests.

    Args:
        api_token: PagerDuty API token

    Returns:
        Dict[str, str]: Headers dictionary with authorization
    """
    return {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": f"Token token={api_token}",
    }


def get_user_name(user_email: str, headers: Dict) -> Optional[str]:
    """Retrieve PagerDuty user name for a given email.

    Args:
        user_email: User's email address
        headers: API request headers

    Returns:
        Optional[str]: User's name if found, None otherwise
    """
    base_url = "https://api.pagerduty.com/users"
    params = {"query": user_email}

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()

        users = response.json().get("users", [])
        return users[0]["name"] if users else None

    except requests.exceptions.RequestException as exc:
        print(f"Failed to fetch user details for {user_email}: {exc}")
        return None


def get_the_date() -> str:
    """Get current date and time formatted with timezone.

    Returns:
        str: Formatted date string (e.g., "16-June-2025 (14:30 UTC)")
    """
    current_datetime = datetime.datetime.now().astimezone()
    formatted_date = current_datetime.strftime('%d-%B-%Y')
    formatted_time = current_datetime.strftime('( %H:%M %Z )')
    return f"{formatted_date} {formatted_time}"

