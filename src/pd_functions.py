from src.pd_essentials import *
import time
import subprocess
import tempfile
import os
import pdpyras
import pytz
import json
import sys
import threading
from datetime import datetime


# # # # # # # # # # # # # # # #  List Functionalities # # # # # # # # # # # # # # # #  

def pd_list_all(service_ids,session):
  response = session.list_all("incidents",
               params={'service_ids[]':service_ids,
                       'statuses[]':['acknowledged','triggered']})
  if response:
    print(format_incident_table(response))
  else:
     print("No [Acknowledged/Triggered] Incidents found on PagerDuty")




def pd_list_user(service_ids, session, user_id, user_name):
    response = session.list_all("incidents",
        params={
            'service_ids[]': service_ids,
            'statuses[]': ['acknowledged', 'triggered'],
            'user_ids[]': [user_id]
        }
    )

    if response:
        print(format_incident_table(response))
    else:
        print(f"No [Acknowledged/Triggered] Incidents assigned to {user_name} found on PagerDuty")





# # # # # # # # # # # # # # # #  Acknowledge Functionalities # # # # # # # # # # # # # # # #  

def pd_acknowledge_all(session):
  incidents = session.list_all(
    'incidents',
    params={'statuses[]':['triggered']}
  )
  for item in incidents:
    item['status'] = 'acknowledged'

  # PUT the updated list back up to the API
  if len(incidents) == 0:
      print(f"[ {get_the_date()} ] - No [Triggered] Incidents found on PagerDuty Currently !")
  else:
      print(f"[ {get_the_date()} ] - Acknowleding the Incidents Now ...")
      updated_incidents = session.rput('incidents', json=incidents)
      print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now:")
      print(format_incident_table(updated_incidents))


def pd_acknowledge_user(user_id,session,user_name):
  incidents = session.list_all(
    'incidents',
    params={'user_ids[]':[user_id],'statuses[]':['triggered']}
  )
  for item in incidents:
    item['status'] = 'acknowledged'

  # PUT the updated list back up to the API
  if len(incidents) == 0:
      print(f"[ {get_the_date()} ] - No [Triggered] Incidents assigned to {user_name} found on PagerDuty Currently !")
  else:
      print(f"[ {get_the_date()} ] - Acknowleding the Incidents assigned to {user_name} now ...")
      updated_incidents = session.rput('incidents', json=incidents)
      print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now:")
      print(format_incident_table(updated_incidents))


def pd_acknowledge_id(session, service_ids):
    response = session.list_all("incidents",
                                params={'service_ids[]': service_ids,
                                        'statuses[]': ['triggered','acknowledged']})

    if not response:
        print(f"[ {get_the_date()} ] - No [Triggered] Incidents found on PagerDuty currently!")
        return

    print(format_incident_table(response))
    inc_id_input = input("Please Enter the Incident ID you want to Acknowledge from the list above: ")

    # Check if the incident with the provided ID is in the triggered state
    target_incident = None
    for incident in response:
        if incident['id'] == inc_id_input:
            target_incident = incident
            break

    if not target_incident:
        print(f"[ {get_the_date()} ] - No [Triggered] Incidents found with the provided Incident ID!")
        return

    # Acknowledge the specific incident
    target_incident['status'] = 'acknowledged'
    updated_incident = session.rput(f'incidents/{inc_id_input}', json=target_incident)
    print(f"[ {get_the_date()} ] - Acknowledging {inc_id_input} now ...")
    print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now (UPDATED LIST):")
    pd_list_all(service_ids, session)


def pd_acknowledge_all_loop(session, interval):
    def input_listener():
        nonlocal running
        try:
            while True:
                user_input = input()
                if user_input.lower() == 'q':
                    running = False
                    break
        except KeyboardInterrupt:
            pass

    running = True
    start_time = time.time()

    # Start the input listener thread
    input_thread = threading.Thread(target=input_listener)
    input_thread.daemon = True
    input_thread.start()

    try:
        while running:
            print(f"[ {get_the_date()} ] - Checking for [Triggered] Incidents on PagerDuty Now ...")
            incidents = session.list_all(
                'incidents',
                params={'statuses[]': ['triggered']}
            )
            for item in incidents:
                item['status'] = 'acknowledged'

            # PUT the updated list back up to the API
            if len(incidents) == 0:
                print(f"[ {get_the_date()} ] - No [Triggered] Incidents found on PagerDuty Currently !")
            else:
                print(f"[ {get_the_date()} ] - Acknowledging the Incidents Now ...")
                updated_incidents = session.rput('incidents', json=incidents)
                print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now:")
                print(format_incident_table(updated_incidents))
            print("\n\n")
            time.sleep(interval)

    except KeyboardInterrupt:
        pass  # Allow graceful termination with Ctrl+C

    finally:
        end_time = time.time()
        total_time = end_time - start_time
        print(f"\n[ {get_the_date()} ] - The loop was terminated gracefully. Total running time: {total_time:.2f} seconds.\n")


def pd_acknowledge_user_loop(user_id, session, user_name, interval):
    def input_listener():
        nonlocal running
        try:
            while True:
                user_input = input()
                if user_input.lower() == 'q':
                    running = False
                    break
        except KeyboardInterrupt:
            pass

    running = True
    start_time = time.time()

    # Start the input listener thread
    input_thread = threading.Thread(target=input_listener)
    input_thread.daemon = True
    input_thread.start()

    try:
        while running:
            print(f"[ {get_the_date()} ] - Checking for [Triggered] Incidents assigned to {user_name} on PagerDuty Now ...")
            incidents = session.list_all(
                'incidents',
                params={'user_ids[]': [user_id], 'statuses[]': ['triggered']}
            )
            for item in incidents:
                item['status'] = 'acknowledged'

            # PUT the updated list back up to the API
            if len(incidents) == 0:
                print(f"[ {get_the_date()} ] - No [Triggered] Incidents assigned to {user_name} found on PagerDuty Currently !")
            else:
                print(f"[ {get_the_date()} ] - Acknowledging the Incidents assigned to {user_name} now ...")
                updated_incidents = session.rput('incidents', json=incidents)
                print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now:")
                print(format_incident_table(updated_incidents))
            print("\n\n")
            time.sleep(interval)

    except KeyboardInterrupt:
        pass  # Allow graceful termination with Ctrl+C

    finally:
        end_time = time.time()
        total_time = end_time - start_time
        print(f"\n[ {get_the_date()} ] - The loop was terminated gracefully. Total running time: {total_time:.2f} seconds.\n")





# # # # # # # # # # # # # # # #  Resolve Functionalities # # # # # # # # # # # # # # # #  

def pd_resolve_all(session):
    incidents = session.list_all(
        'incidents',
        params={'statuses[]': ['acknowledged']}
    )

    for item in incidents:
        item['status'] = 'resolved'

    # PUT the updated list back up to the API
    if len(incidents) == 0:
        print(f"[ {get_the_date()} ] - No [Acknowledged] Incidents found on PagerDuty Currently !")
    else:
        print(f"[ {get_the_date()} ] - Resolving all [Acknowledged] Incidents on PagerDuty Now ...")
        updated_incidents = session.rput('incidents', json=incidents)
        print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now (UPDATED LIST):")
        print(format_incident_table(updated_incidents))


def pd_resolve_id(session, service_ids):
    incident_ids_input = input("Please Enter the Incident IDs you want to Resolve (comma-separated): ")
    incident_ids = incident_ids_input.split(',')
    
    response = session.list_all("incidents",
                                params={'service_ids[]': service_ids,
                                        'statuses[]': ['triggered','acknowledged']})

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


def pd_resolve_user(user_id, session, user_name):
    incidents = session.list_all(
        'incidents',
        params={'user_ids[]': [user_id], 'statuses[]': ['acknowledged']}
    )

    for item in incidents:
        item['status'] = 'resolved'

    # PUT the updated list back up to the API
    if len(incidents) == 0:
        print(f"[ {get_the_date()} ] - No Acknowledged Incidents assigned to {user_name} found on PagerDuty Currently !")
    else:
        print(f"[ {get_the_date()} ] - Resolving all Acknowledged Incidents assigned to {user_name} now ...")
        updated_incidents = session.rput('incidents', json=incidents)
        print(f"[ {get_the_date()} ] - Below are the Incidents in PagerDuty Now (UPDATED LIST):")
        print(format_incident_table(updated_incidents))


def pd_resolve_like(session, service_ids):
    response = session.list_all("incidents",
                                params={'service_ids[]': service_ids,
                                        'statuses[]': ['triggered', 'acknowledged']})

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
def get_service_ids(session):
    service_info = []

    # Iterate through each service
    for service in session.iter_all('services'):
        service_id = service['id']
        service_name = service['name']
        service_info.append((service_id, service_name))

    return service_info

# Function to display service info in a table
def tabulate_service_info(service_info):
    if not service_info:
        print("No service information available.")
        return

    # Define the headers for the table
    headers = ["Service ID", "Service Name"]

    # Use the tabulate function to format and display the table
    table = tabulate(service_info, headers, tablefmt="pretty", stralign="left")

    print(table)



# Function to get schedules
def get_schedule_ids(session):
    schedule_info = []

    # Iterate through each schedule
    for schedule in session.iter_all('schedules'):
        schedule_id = schedule['id']
        schedule_name = schedule['name']
        schedule_info.append((schedule_id, schedule_name))

    return schedule_info

# Function to display schedule info in a table
def tabulate_schedule_info(schedule_info):
    if not schedule_info:
        print("No schedule information available.")
        return

    # Define the headers for the table
    headers = ["Schedule ID", "Schedule Name"]

    # Use the tabulate function to format and display the table
    table = tabulate(schedule_info, headers, tablefmt="pretty",stralign="left")

    print(table)









def check_vim_or_vi_installed():
    try:
        # Check if 'vim' is installed
        result_vim = subprocess.run(['vim', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check the return code. If Vim is installed, it should return 0.
        if result_vim.returncode == 0:
            return "Vim is installed on this system."

    except FileNotFoundError:
        pass  # 'vim' executable is not found, continue to check for 'vi'

    try:
        # Check if 'vi' is installed
        result_vi = subprocess.run(['vi', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check the return code. If Vi is installed, it should return 0.
        if result_vi.returncode == 0:
            return "Vi is installed on this system."

    except FileNotFoundError:
        return "Neither Vim nor Vi is installed on this system."
    

def open_vim_for_incident_note(incident_id):
    # Create a temporary directory to store the notes file
    temp_dir = tempfile.mkdtemp()

    # Define the file name based on the incident ID
    note_file = os.path.join(temp_dir, f"{incident_id}_Note.txt")

    # Open Vim editor
    subprocess.run(["vim", note_file])

    return note_file

def read_note_from_file(note_path):
    note_file_path = note_path
    note = ""
    
    if os.path.exists(note_file_path):
        with open(note_file_path, "r") as note_file:
            note = note_file.read().strip()
    
    return note



def add_note_to_incident(session, incident_id, note):
    endpoint = f'/incidents/{incident_id}/notes'

    # Generate the timestamp with the specified format and timezone
    current_time_utc = datetime.datetime.now(pytz.timezone('UTC'))
    formatted_time = current_time_utc.strftime('[ %d-%b-%Y - %H:%M IST ]')

    # Add the timestamp to the note content
    note_with_timestamp = f"{formatted_time} - Note Added\n\n{note}"

    payload = {
        "note": {
            "content": note_with_timestamp,
        }
    }

    try:
        response = session.post(endpoint, json=payload)
        response.raise_for_status()

        print(f"Note added to incident ID {incident_id}")
    except pdpyras.PDClientError as e:
        print(f"Failed to add note to incident ID {incident_id}: {e}")



def check_pagerduty_status():

    url = "https://api.pagerduty.com/"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def check_pagerduty_company_url(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    


# Function to create an incident for a specific service using pdpyras
def create_incident_for_service(api_token,user_email,service_id,title,description,company_domain):
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

    r = requests.post(url, headers=headers, data=json.dumps(payload))

    print(f'Status Code: {r.status_code}')
    response_data = r.json()

    if 'incident' in response_data:
        incident_id = response_data['incident']['id']
        incident_url = f'{company_domain}/incidents/{incident_id}'
        print(f'Incident Created successfully with ID: {incident_id}')
        print(f'Please visit the URL for more details: {incident_url}')
    else:
        print('Failed to create incident.')
        return None
