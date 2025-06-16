#!/usr/bin/env python3
"""PagerCuty - A Command-Line Utility for PagerDuty.

This module serves as the main entry point for the PagerCuty CLI tool,
providing command-line argument parsing and orchestration of PagerDuty operations.
"""

import argparse
import subprocess
import sys
from typing import Dict, List, Optional

import pdpyras

from src.pd_essentials import (
    authorize,
    get_user_id,
    get_user_name,
    read_config
)
from src.pd_functions import (
    check_pagerduty_company_url,
    check_pagerduty_status,
    check_vim_or_vi_installed,
    create_incident_for_service,
    get_schedule_ids,
    get_service_ids,
    open_vim_for_incident_note,
    pd_acknowledge_all,
    pd_acknowledge_all_loop,
    pd_acknowledge_id,
    pd_acknowledge_user,
    pd_list_all,
    pd_list_user,
    pd_resolve_all,
    pd_resolve_id,
    pd_resolve_like,
    pd_resolve_user,
    read_note_from_file,
    tabulate_info
)


def setup_argument_parser(
    user_name: str,
    ack_interval_secs: int
) -> argparse.ArgumentParser:
    """Create and configure the argument parser.
    
    Args:
        user_name: User's display name for help text
        ack_interval_secs: Acknowledgment interval in seconds
        
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="PagerCuty - A Command-Line Utility for PagerDuty."
    )
    
    parser.add_argument(
        "--check_pd_status", "-pds",
        action="store_true",
        help=(
            "Checks the Status of PagerDuty from both, Manual hit to Company's "
            "URL and from the Official PagerDuty Status Page"
        )
    )
    
    parser.add_argument(
        "--create_an_incident", "-crin",
        action="store_true",
        help="Lets you Create a PagerDuty Incident"
    )
    
    parser.add_argument(
        "-list",
        choices=["all", "user"],
        help=(
            f"all - Lists all Non-Resolved Incidents on PagerDuty, "
            f"user - Lists all Incidents on PagerDuty assigned to {user_name}"
        )
    )
    
    parser.add_argument(
        "-ack",
        choices=["all", "user", "id"],
        help=(
            f"all - Acknowledges all [Triggered] Incidents on PagerDuty, "
            f"user - Acknowledges all [Triggered] Incidents on PagerDuty "
            f"assigned to {user_name}, "
            f"id - Acknowledges a Specific Incident from Pagerduty"
        )
    )
    
    parser.add_argument(
        "-ackloop",
        choices=["all", "user"],
        help=(
            f"all - Acknowledges all [Triggered] Incidents on PagerDuty every "
            f"{ack_interval_secs} seconds, "
            f"user - Acknowledges all [Triggered] Incidents on PagerDuty "
            f"assigned to {user_name} every {ack_interval_secs} seconds"
        )
    )
    
    parser.add_argument(
        "--resolve", "-res",
        choices=["all", "user", "id", "like"],
        help=(
            f"all - Resolves all Incidents from PagerDuty, "
            f"user - Resolves all Incidents from PagerDuty assigned to "
            f"{user_name}, "
            f"id - Resolves a Specific Incident from Pagerduty, "
            f"like - Resolves all Incidents containing a keyword"
        )
    )
    
    parser.add_argument(
        "--add_note", "-an",
        action="store_true",
        help="Add note to an Incident (List will be Provided)"
    )
    
    parser.add_argument(
        "-get_service_ids",
        action="store_true",
        help="List all Service IDs and their Names"
    )
    
    parser.add_argument(
        "-get_schedule_ids",
        action="store_true",
        help="List all Schedule IDs and their Names"
    )
    
    return parser


def validate_config(
    config: Dict,
    session: pdpyras.APISession
) -> Optional[List[str]]:
    """Validate configuration and return service IDs.
    
    Args:
        config: Configuration dictionary
        session: PagerDuty API session
        
    Returns:
        List of service IDs if valid, None if invalid
    """
    api_token = config.get("api_token")
    service_ids_str = config.get("service_id")
    
    if not api_token:
        print("Missing API Token in config.yaml!")
        return None
        
    if not service_ids_str:
        print(
            "Missing Service ID in config.yaml.\n"
            "Below is the list of Service IDs you can mention in config.yaml "
            "(comma-separated)"
        )
        service_info = get_service_ids(session)
        tabulate_info(service_info, ["Service ID", "Service Name"])
        return None
        
    return service_ids_str.split(",")


def handle_check_pd_status(
    company_url_pd: str
) -> None:
    """Handle PagerDuty status check command.
    
    Args:
        company_url_pd: Company's PagerDuty URL
    """
    api_status = "Up" if check_pagerduty_status() else "Down"
    company_url_status = (
        "Up" if check_pagerduty_company_url(company_url_pd) else "Down"
    )
    print(f"API Status: {api_status}\nURL Status: {company_url_status}")


def handle_create_incident(
    api_token: str,
    user_email: str,
    session: pdpyras.APISession,
    company_domain: str
) -> None:
    """Handle incident creation command.
    
    Args:
        api_token: PagerDuty API token
        user_email: User's email address
        session: PagerDuty API session
        company_domain: Company's PagerDuty domain
    """
    if not check_vim_or_vi_installed():
        print(
            "vim/vi editor is not installed. This functionality requires "
            "vim/vi editor."
        )
        return

    service_info = get_service_ids(session)
    tabulate_info(service_info, ["Service ID", "Service Name"])
    
    inc_service_id = input(
        "Please enter the Service ID from the list above for the incident: "
    )
    inc_title = input("Please enter the Title for your Incident: ")
    
    inc_note_file_path = open_vim_for_incident_note(inc_service_id)
    inc_note = read_note_from_file(inc_note_file_path)
    
    create_incident_for_service(
        api_token,
        user_email,
        inc_service_id,
        inc_title,
        inc_note,
        company_domain
    )
    
    subprocess.run(["rm", "-rf", inc_note_file_path], check=True)


def main() -> None:
    """Main entry point for PagerCuty CLI tool."""
    config = read_config()
    api_token = config.get("api_token")
    session = pdpyras.APISession(api_token)
    
    service_ids = validate_config(config, session)
    if not service_ids:
        sys.exit(1)
    
    user_email = config.get("email")
    user_id = get_user_id(user_email, authorize(api_token))
    user_name = get_user_name(user_email, authorize(api_token))
    ack_interval_secs = config.get("time_interval")
    company_url_pd = config.get("company_pd_url")
    company_domain = config.get("company_domain")

    parser = setup_argument_parser(user_name, ack_interval_secs)
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    try:
        if args.check_pd_status:
            handle_check_pd_status(company_url_pd)

        if args.create_an_incident:
            handle_create_incident(
                api_token,
                user_email,
                session,
                company_domain
            )

        if args.get_service_ids:
            service_info = get_service_ids(session)
            tabulate_info(service_info, ["Service ID", "Service Name"])

        if args.get_schedule_ids:
            schedule_info = get_schedule_ids(session)
            tabulate_info(schedule_info, ["Schedule ID", "Schedule Name"])

        if args.list == "all":
            pd_list_all(service_ids, session)
        elif args.list == "user":
            pd_list_user(service_ids, session, user_id, user_name)

        if args.ack == "all":
            pd_acknowledge_all(session)
        elif args.ack == "user":
            pd_acknowledge_user(user_id, session, user_name)
        elif args.ack == "id":
            pd_acknowledge_id(session, service_ids)

        if args.ackloop == "all":
            print(
                f"Hi {user_name},\n"
                f"All [Triggered] Incidents will be Acknowledged every "
                f"{ack_interval_secs} seconds..."
            )
            pd_acknowledge_all_loop(session, ack_interval_secs)
        elif args.ackloop == "user":
            print(
                f"Hi {user_name},\n"
                f"Your [Triggered] Incidents will be Acknowledged every "
                f"{ack_interval_secs} seconds..."
            )
            pd_acknowledge_all_loop(session, ack_interval_secs)

        if args.resolve == "all":
            pd_resolve_all(session)
        elif args.resolve == "user":
            pd_resolve_user(user_id, session, user_name)
        elif args.resolve == "id":
            pd_resolve_id(session, service_ids)
        elif args.resolve == "like":
            pd_resolve_like(session, service_ids)

    except Exception as exc:
        print(f"An error occurred: {exc}")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
