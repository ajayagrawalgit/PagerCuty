import argparse
from src.pd_essentials import *
from src.pd_functions import *
import pdpyras
import sys


def main():
    config = read_config()
    api_token = config.get("api_token")
    service_ids = config.get("service_id")
    service_ids = service_ids.split(",") # Converting the Comma Separated Values to List

    user_email = config.get("email")
    user_id = get_user_id(user_email, authorize(api_token))
    user_name = get_user_name(user_email, authorize(api_token))
    ack_interval_secs=config.get("time_interval")
    company_url_pd=config.get("company_pd_url")
    company_domain=config.get("company_domain")

    # List of All the Available Arguments here ...
    parser = argparse.ArgumentParser(description="PagerCuty - A Command-Line Utility for PagerDuty.")
    parser.add_argument("--check_pd_status","-pds",action="store_true",help="Checks the Status of PagerDuty from both, Manual hit to Company's URL and from the Official PagerDuty Status Page")
    parser.add_argument("--create_an_incident","-crin",action="store_true",help="Lets you Create a PagerDuty Incident")
    parser.add_argument("-list", choices=["all", "user"], required=False, default=None, help=f"all - Lists all Non-Resolved Incidents on PagerDuty, user - Lists all Incidents on PagerDuty assigned to the {user_name}")
    parser.add_argument("-ack", choices=["all", "user", "id"], required=False, default=None, help=f"all - Acknowledges all [Triggered] Incidents on PagerDuty, user - Acknowledges all [Triggered] Incidents on PagerDuty assigned to the {user_name}, id - Acknowledges a Specific Incident from Pagerduty (List will be Provided)")
    parser.add_argument("-ackloop", choices=["all", "user"], required=False, default=None, help=f"all - Acknowledges all [Triggered] Incidents on PagerDuty every {ack_interval_secs} seconds, user - Acknowledges all [Triggered] Incidents on PagerDuty assigned to {user_name} every {ack_interval_secs} seconds")
    parser.add_argument("--resolve","-res", choices=["all", "user", "id", "like"], required=False, default=None, help=f"all - Resolves all Incidents from PagerDuty, user - Resolves all Incidents from PagerDuty assigned to {user_name}, id - Resolves a Specific Incident from Pagerduty (List will be Provided), like - Resolves all the Incidents from Pagerduty containing a certain keyword")
    parser.add_argument("--add_note","-an",action="store_true",help="Use this to add note to an Incident (List will be Provided)")
    parser.add_argument("-get_service_ids", action="store_true", required=False, default=None, help=f"This lists all the Service IDs and their Names")
    parser.add_argument("-get_schedule_ids", action="store_true", required=False, default=None, help=f"This lists all the Schedule IDs and their Names")





    args = parser.parse_args()

    # Initial Checks
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)
    
    if not api_token:
        print("Missing API Token in config.yaml !")
        sys.exit(1)

    if not service_ids:
        print("Service ID in the config.yaml.\nBelow is the list of Service IDs you can mention in config.yaml (comma-separated)")
        tabulate_service_info(get_service_ids(session))
        sys.exit(1)

    session = pdpyras.APISession(api_token)


    # PD Status
    if args.check_pd_status:
        api_status=check_pagerduty_status()
        company_url_status=check_pagerduty_company_url(company_url_pd)
        if api_status:
            api_status="Up"
        else:
            api_status="Down"
        
        if company_url_status:
            company_url_status="Up"
        else:
            company_url_status="Down"

        print(f"API Status: {api_status}\nURL Status: {company_url_status}")


    # Service ID Function
    if args.create_an_incident:
        vim_installed_or_not=check_vim_or_vi_installed()
        if vim_installed_or_not:
            tabulate_schedule_info(get_service_ids(session))
            inc_service_id_input=input("Please enter the Schedule ID from the list above you want to create an incident for: ")
            inc_title=input("Please enter the Title you want to give your Incident and press enter/Return\n")
            inc_note_file_path = open_vim_for_incident_note(inc_service_id_input)
            inc_note_to_create = read_note_from_file(inc_note_file_path)
            create_incident_for_service(api_token,user_email,inc_service_id_input,inc_title,inc_note_to_create,company_domain)
            subprocess.run(["rm", "-rf", inc_note_file_path])
            
        else:
            print("vim/vi editor is not installed on your machine. This functionality can only be used with systems that has vim/vi editor installed.")
    


    # Note Addition
    if args.add_note:
        vim_installed_or_not=check_vim_or_vi_installed()
        if vim_installed_or_not:
            pd_list_all(service_ids, session)
            inc_input=input("Enter the Incident ID to which you want to add note: ")
            note_file_path = open_vim_for_incident_note(inc_input)
            note_for_inc = read_note_from_file(note_file_path)
            add_note_to_incident(session,inc_input,note_for_inc)
            subprocess.run(["rm", "-rf", note_file_path])
            
        else:
            print("vim/vi editor is not installed on your machine. This functionality can only be used with systems that has vim/vi editor installed.")
    

    # Service ID Function
    if args.get_service_ids:
        tabulate_service_info(get_service_ids(session))
    
    # Service ID Function
    if args.get_schedule_ids:
        tabulate_schedule_info(get_schedule_ids(session))


    # List Functionalities
    if args.list is None:
        pass
    elif args.list == "all":
        pd_list_all(service_ids, session)
    elif args.list == "user":
        pd_list_user(service_ids, session, user_id, user_name)

    # Acknowledge Functionalities
    if args.ack is None:
        pass
    elif args.ack == "all":
        pd_acknowledge_all(session)
    elif args.ack == "user":
        pd_acknowledge_user(user_id,session,user_name)
    elif args.ack == "id":
        pd_acknowledge_id(session,service_ids)


    # Acknowledge on Loop Functionalities
    if args.ackloop is None:
        pass
    elif args.ackloop == "all":
        print(f"Hi {user_name},\nAll the [ Triggered ] Incidents on Pagerduty will now be Acknowledged every {ack_interval_secs} seconds...")
        pd_acknowledge_all_loop(session,ack_interval_secs)
    elif args.ackloop == "user":
        print(f"Hi {user_name},\nAll the [ Triggered ] Incidents assigned to you on Pagerduty will now be Acknowledged every {ack_interval_secs} seconds...")
        pd_acknowledge_user_loop(user_id,session,user_name,ack_interval_secs)



    # Resolve Functionalities
    if args.resolve is None:
        pass
    elif args.resolve == "all":
        pd_resolve_all(session)
    elif args.resolve == "user":
        pd_resolve_user(user_id,session,user_name)
    elif args.resolve == "id":
        pd_resolve_id(session,service_ids)
    elif args.resolve == "like":
        pd_resolve_like(session,service_ids)



    # Close the session
    session.close()






if __name__ == "__main__":
    main()
