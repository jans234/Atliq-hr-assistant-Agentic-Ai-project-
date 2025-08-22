import os
import logging
from dotenv import load_dotenv
from typing import Dict, List, Optional
from datetime import datetime
from mcp.server.fastmcp import FastMCP

from HRMS import *
from utils import seed_services
from emails import EmailSender

# Load environment variables
load_dotenv()

# ----------------- Setup Logging -----------------
logging.basicConfig(
    filename="hrms.log",  # Log file
    level=logging.INFO,   # Log level (INFO, DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------- Email Setup -----------------
email_sender = EmailSender(
    smtp_server="smtp.gmail.com",
    port=587,
    username=os.getenv("CB_EMAIL"),
    password=os.getenv("CB_EMAIL_PWD"),
    use_tls=True
)

#  MCP Setup
mcp = FastMCP("Atliq-hr-assist")

EmployeeManager = EmployeeManager()
LeaveManager = LeaveManager()
MeetingManager = MeetingManager()
TicketManager = TicketManager()

seed_services(EmployeeManager, LeaveManager, MeetingManager, TicketManager)


# ----------------- Tools -----------------
@mcp.tool()
def add_employee(emp_name: str, manager_id: str, email: str) -> str:
    """
    Adds a new employee to HRMS system.
    """
    logging.info(f"Attempting to add employee: {emp_name}, Manager: {manager_id}, Email: {email}")
    emp = EmployeeCreate(
        emp_id=EmployeeManager.get_next_emp_id(),
        name=emp_name,
        manager_id=manager_id,
        email=email
    )
    EmployeeManager.add_employee(emp)
    logging.info(f"Employee successfully added: {emp}")
    return f"Employee {emp_name} added successfully"


@mcp.tool()
def get_employee_details(name: str) -> Dict[str, str]:
    """
    Retrieves details of an employee by name.
    """
    logging.info(f"Searching details for employee: {name}")
    emp_id = EmployeeManager.search_employee_by_name(name)
    if not emp_id:
        logging.warning(f"Employee search failed: {name}")
        return {"error": "Employee not found"}

    details = EmployeeManager.get_employee_details(emp_id[0])
    logging.info(f"Employee details retrieved: {name} -> {details}")
    return details


@mcp.tool()
def send_email(subject: str, body: str, to_emails: List[str]) -> str:
    """
    Sends an email.
    """
    logging.info(f"Preparing to send email: Subject='{subject}' To={to_emails}")
    try:
        email_sender.send_email(
            subject=subject,
            body=body,
            to_emails=to_emails,
            from_email=email_sender.username
        )
        logging.info(f"Email sent successfully: Subject='{subject}' To={to_emails}")
        return "Email sent Successfully"
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return f"Error: {e}"
    

@mcp.tool()
def create_ticket(emp_id: str, item: str, reason: str) -> str:
    logging.info(f"Creating ticket for Employee {emp_id}, Item={item}, Reason={reason}")
    ticket_req = TicketCreate(emp_id=emp_id, item=item, reason=reason)
    result = TicketManager.create_ticket(ticket_req)
    logging.info(f"Ticket created successfully: {result}")
    return result


@mcp.tool()
def update_ticket_status(ticket_id: str, status: str) -> str:
    logging.info(f"Updating ticket {ticket_id} to status '{status}'")
    ticket_status_update = TicketStatusUpdate(status=status)
    result = TicketManager.update_ticket_status(ticket_status_update, ticket_id)
    logging.info(f"Ticket {ticket_id} updated successfully to {status}")
    return result


@mcp.tool()
def list_tickets(employee_id: str, status: str) -> List[Dict[str, str]]:
    logging.info(f"Listing tickets for Employee {employee_id}, Status={status}")
    tickets = TicketManager.list_tickets(employee_id=employee_id, status=status)
    logging.info(f"Tickets retrieved for Employee {employee_id}: {tickets}")
    return tickets


@mcp.tool()
def schedule_meeting(employee_id: str, meeting_datetime: datetime, topic: str) -> str:
    logging.info(f"Scheduling meeting for Employee {employee_id} on {meeting_datetime} about '{topic}'")
    meeting_req = MeetingCreate(emp_id=employee_id, meeting_dt=meeting_datetime, topic=topic)
    result = MeetingManager.schedule_meeting(meeting_req)
    logging.info(f"Meeting scheduled successfully: {result}")
    return result


@mcp.tool()
def get_meetings(employee_id: str) -> List[Dict[str, str]]:
    logging.info(f"Fetching meetings for Employee {employee_id}")
    meetings = MeetingManager.get_meetings(employee_id)
    logging.info(f"Meetings retrieved for Employee {employee_id}: {meetings}")
    return meetings


@mcp.tool()
def cancel_meeting(employee_id: str, meeting_datetime: datetime, topic: Optional[str] = None) -> str:
    logging.info(f"Attempting to cancel meeting for Employee {employee_id} on {meeting_datetime}, Topic={topic}")
    cancel_req = MeetingCancelRequest(emp_id=employee_id, meeting_dt=meeting_datetime, topic=topic)
    result = MeetingManager.cancel_meeting(cancel_req)
    logging.info(f"Meeting cancelled successfully: {result}")
    return result


@mcp.tool()
def get_employee_leave_balance(employee_id: str) -> str:
    logging.info(f"Fetching leave balance for Employee {employee_id}")
    balance = LeaveManager.get_leave_balance(employee_id)
    logging.info(f"Leave balance retrieved: {balance}")
    return balance


@mcp.tool()
def apply_leave(employee_id: str, leave_type: str, start_date: datetime, end_date: datetime) -> str:
    logging.info(f"Applying leave for Employee {employee_id}, Type={leave_type}, From={start_date} To={end_date}")
    leave_req = LeaveApplyRequest(emp_id=employee_id, leave_type=leave_type, start_date=start_date, end_date=end_date)
    result = LeaveManager.apply_leave(leave_req)
    logging.info(f"Leave applied successfully: {result}")
    return result


@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    logging.info(f"Fetching leave history for Employee {employee_id}")
    history = LeaveManager.get_leave_history(employee_id)
    logging.info(f"Leave history retrieved: {history}")
    return history


@mcp.prompt("onboard_new_employee")
def onboard_new_employee(employee_name: str, manager_name: str):
    logging.info(f"Starting onboarding for new employee: {employee_name}, Manager: {manager_name}")
    message = f"""
    Onboard a new employee with following details:
    - Name : {employee_name}
    - Manager Name : {manager_name}
    Steps to follow:
    1. Add the employee to the HRMS system.
    2. Send a welcome email to the employee with login credentials. (Format: employee_name@atliq.com)
    3. Notify the manager about the new employee onboarding.
    4. Raise ticket for a new laptop, id card and other necessary equipment.
    5. Schedule an introductory meeting with the team.
    6. Get employee leave balance, apply for leave and get leave history.
    7. Don't schedule meeting by yourself.
    """
    logging.info(f"Onboarding steps generated for {employee_name}")
    return message


# ----------------- Run MCP -----------------
if __name__ == "__main__":
    logging.info("Starting MCP server: Atliq-hr-assist")
    mcp.run(transport="stdio")
