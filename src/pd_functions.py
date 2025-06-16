"""PagerDuty incident management functions.

This module provides functions for managing PagerDuty incidents, including listing,
acknowledging, resolving incidents and adding notes.
"""

import json
import os
import subprocess
import tempfile
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pdpyras
import pytz
import requests

from src.pd_essentials import format_incident_table, get_the_date


def pd_list_all(service_ids: List[str], session: pdpyras.APISession) -> None:
    """List all acknowledged and triggered incidents.
    
    Args:
        service_ids: List of PagerDuty service IDs
        session: PagerDuty API session
    """
    response = session.list_all(
        "incidents",
        params={
            'service_ids[]': service_ids,
            'statuses[]': ['acknowledged', 'triggered']
        }
    )
    
    if response:
        print(format_incident_table(response))
    else:
        print("No [Acknowledged/Triggered] Incidents found on PagerDuty")


def pd_list_user(
    service_ids: List[str],
    session: pdpyras.APISession,
    user_id: str,
    user_name: str
) -> None:
    """List incidents assigned to a specific user.
    
    Args:
        service_ids: List of PagerDuty service IDs
        session: PagerDuty API session
        user_id: PagerDuty user ID
        user_name: User's display name
    """
    response = session.list_all(
        "incidents",
        params={
            'service_ids[]': service_ids,
            'statuses[]': ['acknowledged', 'triggered'],
            'user_ids[]': [user_id]
        }
    )
    
    if response:
        print(format_incident_table(response))
    else:
        print(
            f"No [Acknowledged/Triggered] Incidents assigned to {user_name} "
            "found on PagerDuty"
        )


def pd_acknowledge_all(session: pdpyras.APISession) -> None:
    """Acknowledge all triggered incidents.
    
    Args:
        session: PagerDuty API session
    """
    incidents = session.list_all(
        'incidents',
        params={'statuses[]': ['triggered']}
    )
    
    if not incidents:
        print(
            f"[ {get_the_date()} ] - No [Triggered] Incidents found on "
            "PagerDuty Currently!"
        )
        return
        
    for incident in incidents:
        incident['status'] = 'acknowledged'
    
    print(f"[ {get_the_date()} ] - Acknowledging the Incidents Now ...")
    updated_incidents = session.rput('incidents', json=incidents)
    print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now:")
    print(format_incident_table(updated_incidents))


def pd_acknowledge_user(
    user_id: str,
    session: pdpyras.APISession,
    user_name: str
) -> None:
    """Acknowledge all triggered incidents assigned to a specific user.
    
    Args:
        user_id: PagerDuty user ID
        session: PagerDuty API session
        user_name: User's display name
    """
    incidents = session.list_all(
        'incidents',
        params={
            'user_ids[]': [user_id],
            'statuses[]': ['triggered']
        }
    )
    
    if not incidents:
        print(
            f"[ {get_the_date()} ] - No [Triggered] Incidents assigned to "
            f"{user_name} found on PagerDuty Currently!"
        )
        return
        
    for incident in incidents:
        incident['status'] = 'acknowledged'
    
    print(
        f"[ {get_the_date()} ] - Acknowledging the Incidents assigned to "
        f"{user_name} now ..."
    )
    updated_incidents = session.rput('incidents', json=incidents)
    print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now:")
    print(format_incident_table(updated_incidents))


def pd_acknowledge_id(
    session: pdpyras.APISession,
    service_ids: List[str]
) -> None:
    """Acknowledge a specific incident by ID.
    
    Args:
        session: PagerDuty API session
        service_ids: List of PagerDuty service IDs
    """
    response = session.list_all(
        "incidents",
        params={
            'service_ids[]': service_ids,
            'statuses[]': ['triggered', 'acknowledged']
        }
    )

    if not response:
        print(
            f"[ {get_the_date()} ] - No [Triggered] Incidents found on "
            "PagerDuty currently!"
        )
        return

    print(format_incident_table(response))
    inc_id_input = input(
        "Please Enter the Incident ID you want to Acknowledge from the list "
        "above: "
    )

    target_incident = next(
        (inc for inc in response if inc['id'] == inc_id_input),
        None
    )

    if not target_incident:
        print(
            f"[ {get_the_date()} ] - No [Triggered] Incidents found with the "
            "provided Incident ID!"
        )
        return

    target_incident['status'] = 'acknowledged'
    session.rput(f'incidents/{inc_id_input}', json=target_incident)
    print(f"[ {get_the_date()} ] - Acknowledging {inc_id_input} now ...")
    print(
        f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now "
        "(UPDATED LIST):"
    )
    pd_list_all(service_ids, session)


def pd_acknowledge_all_loop(
    session: pdpyras.APISession,
    interval: int
) -> None:
    """Continuously acknowledge all triggered incidents at specified intervals.
    
    Args:
        session: PagerDuty API session
        interval: Time between checks in seconds
    """
    def input_listener(running: List[bool]) -> None:
        try:
            while True:
                user_input = input()
                if user_input.lower() == 'q':
                    running[0] = False
                    break
        except KeyboardInterrupt:
            running[0] = False

    running = [True]
    start_time = time.time()

    input_thread = threading.Thread(
        target=input_listener,
        args=(running,)
    )
    input_thread.daemon = True
    input_thread.start()

    try:
        while running[0]:
            print(
                f"[ {get_the_date()} ] - Checking for [Triggered] Incidents on "
                "PagerDuty Now ..."
            )
            incidents = session.list_all(
                'incidents',
                params={'statuses[]': ['triggered']}
            )
            
            if incidents:
                for incident in incidents:
                    incident['status'] = 'acknowledged'
                print(
                    f"[ {get_the_date()} ] - Acknowledging the Incidents Now ..."
                )
                updated_incidents = session.rput('incidents', json=incidents)
                print(
                    f"[ {get_the_date()} ] - Below are the Incidents in "
                    "PagerDuty Now:"
                )
                print(format_incident_table(updated_incidents))
            else:
                print(
                    f"[ {get_the_date()} ] - No [Triggered] Incidents found on "
                    "PagerDuty Currently!"
                )
            
            print("\n\n")
            time.sleep(interval)

    except KeyboardInterrupt:
        running[0] = False

    finally:
        end_time = time.time()
        total_time = end_time - start_time
        print(
            f"\n[ {get_the_date()} ] - The loop was terminated gracefully. "
            f"Total running time: {total_time:.2f} seconds.\n"
        )


def pd_acknowledge_user_loop(
    user_id: str,
    session: pdpyras.APISession,
    user_name: str,
    interval: int
) -> None:
    """Continuously acknowledge all triggered incidents assigned to a specific user
    at specified intervals.
    
    Args:
        user_id: PagerDuty user ID
        session: PagerDuty API session
        user_name: User's display name
        interval: Time between checks in seconds
    """
    def input_listener(running: List[bool]) -> None:
        try:
            while True:
                user_input = input()
                if user_input.lower() == 'q':
                    running[0] = False
                    break
        except KeyboardInterrupt:
            running[0] = False

    running = [True]
    start_time = time.time()

    input_thread = threading.Thread(
        target=input_listener,
        args=(running,)
    )
    input_thread.daemon = True
    input_thread.start()

    try:
        while running[0]:
            print(
                f"[ {get_the_date()} ] - Checking for [Triggered] Incidents assigned to "
                f"{user_name} on PagerDuty Now ..."
            )
            incidents = session.list_all(
                'incidents',
                params={'user_ids[]': [user_id], 'statuses[]': ['triggered']}
            )
            
            if incidents:
                for incident in incidents:
                    incident['status'] = 'acknowledged'
                print(
                    f"[ {get_the_date()} ] - Acknowledging the Incidents assigned to "
                    f"{user_name} now ..."
                )
                updated_incidents = session.rput('incidents', json=incidents)
                print(
                    f"[ {get_the_date()} ] - Below are the Incidents in "
                    "PagerDuty Now:"
                )
                print(format_incident_table(updated_incidents))
            else:
                print(
                    f"[ {get_the_date()} ] - No [Triggered] Incidents assigned to "
                    f"{user_name} found on PagerDuty Currently!"
                )
            
            print("\n\n")
            time.sleep(interval)

    except KeyboardInterrupt:
        running[0] = False

    finally:
        end_time = time.time()
        total_time = end_time - start_time
        print(
            f"\n[ {get_the_date()} ] - The loop was terminated gracefully. "
            f"Total running time: {total_time:.2f} seconds.\n"
        )


def pd_resolve_all(session: pdpyras.APISession) -> None:
    """Resolve all acknowledged incidents.
    
    Args:
        session: PagerDuty API session
    """
    incidents = session.list_all(
        'incidents',
        params={'statuses[]': ['acknowledged']}
    )

    if not incidents:
        print(f"[ {get_the_date()} ] - No [Acknowledged] Incidents found on PagerDuty Currently !")
        return

    for incident in incidents:
        incident['status'] = 'resolved'

    print(f"[ {get_the_date()} ] - Resolving all [Acknowledged] Incidents on PagerDuty Now ...")
    updated_incidents = session.rput('incidents', json=incidents)
    print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now (UPDATED LIST):")
    print(format_incident_table(updated_incidents))


def pd_resolve_id(
    session: pdpyras.APISession,
    service_ids: List[str]
) -> None:
    """Resolve specific incidents by ID.
    
    Args:
        session: PagerDuty API session
        service_ids: List of PagerDuty service IDs
    """
    incident_ids_input = input("Please Enter the Incident IDs you want to Resolve (comma-separated): ")
    incident_ids = incident_ids_input.split(',')
    
    response = session.list_all(
        "incidents",
        params={
            'service_ids[]': service_ids,
            'statuses[]': ['triggered', 'acknowledged']
        }
    )

    if not response:
        print(f"[ {get_the_date()} ] - No Incidents found on PagerDuty currently!")
        return

    print(format_incident_table(response))
    
    for inc_id_input in incident_ids:
        # Check if the incident with the provided ID is in the triggered state
        target_incident = None
        for incident in response:
            if incident['id'] == inc_id_input:
                target_incident = incident
                break

        if not target_incident:
            print(f"[ {get_the_date()} ] - No Incident found with the provided Incident ID: {inc_id_input}")
        else:
            # Acknowledge the specific incident
            target_incident['status'] = 'resolved'
            updated_incident = session.rput(f'incidents/{inc_id_input}', json=target_incident)
            print(f"[ {get_the_date()} ] - Resolving {inc_id_input} now ...")

    print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now (UPDATED LIST):")
    pd_list_all(service_ids, session)


def pd_resolve_user(
    user_id: str,
    session: pdpyras.APISession,
    user_name: str
) -> None:
    """Resolve all acknowledged incidents assigned to a specific user.
    
    Args:
        user_id: PagerDuty user ID
        session: PagerDuty API session
        user_name: User's display name
    """
    incidents = session.list_all(
        'incidents',
        params={
            'user_ids[]': [user_id],
            'statuses[]': ['acknowledged']
        }
    )

    if not incidents:
        print(f"[ {get_the_date()} ] - No Acknowledged Incidents assigned to {user_name} found on PagerDuty Currently !")
        return

    for incident in incidents:
        incident['status'] = 'resolved'

    print(f"[ {get_the_date()} ] - Resolving all Acknowledged Incidents assigned to {user_name} now ...")
    updated_incidents = session.rput('incidents', json=incidents)
    print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now (UPDATED LIST):")
    print(format_incident_table(updated_incidents))


def pd_resolve_like(session: pdpyras.APISession, service_ids: List[str]) -> None:
    """Resolve all incidents that match a specific keyword in the summary.
    
    Args:
        session: PagerDuty API session
        service_ids: List of PagerDuty service IDs
    """
    response = session.list_all(
        "incidents",
        params={
            'service_ids[]': service_ids,
            'statuses[]': ['triggered', 'acknowledged']
        }
    )

    if not response:
        print(f"[ {get_the_date()} ] - No Incidents found on PagerDuty currently!")
        return

    print("List of Incidents:")
    print(format_incident_table(response))

    keyword = input("Please enter the keyword you want to resolve all the incidents like: ").lower()  # Convert keyword to lowercase
    
    matching_incidents = [incident for incident in response if keyword in incident.get('summary', '').lower()]  # Convert summary to lowercase

    if not matching_incidents:
        print(f"[ {get_the_date()} ] - No Incidents found with the keyword '{keyword}' in the summary.")
        return

    print(f"Incidents with '{keyword}' in the summary:")
    print(format_incident_table(matching_incidents))

    for incident in matching_incidents:
        incident_id = incident['id']
        incident['status'] = 'resolved'
        updated_incident = session.rput(f'incidents/{incident_id}', json=incident)
        print(f"[ {get_the_date()} ] - Resolving incident {incident_id} with '{keyword}' in the summary.")
    
    print(f"[ {get_the_date()} ] - All matching incidents with '{keyword}' in the summary have been resolved.")






# Function to get service IDs and names
def get_service_ids(session: pdpyras.APISession) -> List[Tuple[str, str]]:
    """Get all service IDs and names.
    
    Args:
        session: PagerDuty API session
        
    Returns:
        List of tuples containing service ID and name
    """
    return [
        (service['id'], service['name'])
        for service in session.iter_all('services')
    ]


# Function to get schedules
def get_schedule_ids(session: pdpyras.APISession) -> List[Tuple[str, str]]:
    """Get all schedule IDs and names.
    
    Args:
        session: PagerDuty API session
        
    Returns:
        List of tuples containing schedule ID and name
    """
    return [
        (schedule['id'], schedule['name'])
        for schedule in session.iter_all('schedules')
    ]


def tabulate_info(info_list: List[Tuple[str, str]], headers: List[str]) -> None:
    """Display information in a tabulated format.
    
    Args:
        info_list: List of tuples containing ID and name
        headers: Column headers for the table
    """
    if not info_list:
        print("No information available.")
        return

    print(tabulate(info_list, headers, tablefmt="pretty", stralign="left"))


def check_vim_or_vi_installed() -> bool:
    """Check if Vim or Vi is installed on the system.
    
    Returns:
        bool: True if either Vim or Vi is installed
    """
    editors = ['vim', 'vi']
    for editor in editors:
        try:
            result = subprocess.run(
                [editor, '--version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return True
        except FileNotFoundError:
            continue
    return False


def open_vim_for_incident_note(incident_id: str) -> str:
    """Open Vim editor for incident note creation.
    
    Args:
        incident_id: PagerDuty incident ID
        
    Returns:
        str: Path to the temporary note file
    """
    temp_dir = tempfile.mkdtemp()
    return os.path.join(temp_dir, f"{incident_id}_Note.txt")


def read_note_from_file(note_path: str) -> str:
    """Read note content from a file.
    
    Args:
        note_path: Path to the note file
        
    Returns:
        str: Content of the note file
    """
    if not os.path.exists(note_path):
        return ""
        
    with open(note_path, "r", encoding="utf-8") as note_file:
        return note_file.read().strip()


def check_pagerduty_status() -> bool:
    """Check if PagerDuty API is accessible.
    
    Returns:
        bool: True if PagerDuty API is accessible
    """
    url = "https://api.pagerduty.com/"
    
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def check_pagerduty_company_url(url: str) -> bool:
    """Check if company's PagerDuty URL is accessible.
    
    Args:
        url: Company's PagerDuty URL
        
    Returns:
        bool: True if URL is accessible
    """
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def create_incident_for_service(
    api_token: str,
    user_email: str,
    service_id: str,
    title: str,
    description: str,
    company_domain: str
) -> Optional[str]:
    """Create a new PagerDuty incident.
    
    Args:
        api_token: PagerDuty API token
        user_email: User's email address
        service_id: PagerDuty service ID
        title: Incident title
        description: Incident description
        company_domain: Company's PagerDuty domain
        
    Returns:
        Optional[str]: Incident ID if created successfully
    """
    url = 'https://api.pagerduty.com/incidents'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': f'Token token={api_token}',
        'From': user_email
    }

    payload = {
        "incident": {
            "type": "incident",
            "title": title,
            "service": {
                "id": service_id,
                "type": "service_reference"
            },
            "incident_key": "baf7cf21b1da41b4b0221008339ff3571",
            "body": {
                "type": "incident_body",
                "details": description
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if 'incident' in data:
            incident_id = data['incident']['id']
            incident_url = f'{company_domain}/incidents/{incident_id}'
            print(f'Incident Created successfully with ID: {incident_id}')
            print(f'Please visit the URL for more details: {incident_url}')
            return incident_id
            
    except requests.exceptions.RequestException as exc:
        print(f'Failed to create incident: {exc}')
        
    return None
