# AtliQ HR Assistant (MCP)

An **AI-powered HR Assistant** built with **Model Context Protocol (MCP)** to streamline HR operations such as employee management, leave requests, ticketing, meeting scheduling, and onboarding.  

This project exposes HRMS operations as **MCP tools**, making them accessible to AI agents and assistants in a secure and structured way.

---

## ✨ Features

- **Employee Management**
  - Add new employees
  - Retrieve employee details  

- **Leave Management**
  - Check leave balance
  - Apply for leave
  - Get leave history  

- **Ticketing System**
  - Create tickets (e.g., laptop, ID card)
  - Update ticket status
  - List tickets by employee and status  

- **Meeting Management**
  - Schedule meetings
  - Fetch meetings
  - Cancel meetings  

- **Email Integration**
  - Send emails via Gmail SMTP  

- **Onboarding Workflow**
  - Auto-generates onboarding steps:
    - Add employee to HRMS
    - Send welcome email
    - Notify manager
    - Raise equipment tickets
    - Schedule intro meeting
    - Retrieve leave details  

- **Logging**
  - All actions logged in `hrms.log` with timestamps  

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastMCP** – MCP server framework
- **dotenv** – Load environment variables
- **logging** – For monitoring and debugging
- **Custom HRMS Modules** (`HRMS`, `utils`, `emails`)

---

## 📂 Project Structure
├── HRMS/ # HRMS logic (Employee, Leave, Ticket, Meeting managers)

├── utils.py # Helper for seeding services

├── emails.py # EmailSender class for Gmail SMTP

├── main.py # MCP server (this file)

├── .env # Environment variables (email credentials)

├── hrms.log # Log file (auto-created)

└── README.md # Project documentation

## ⚙️ Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/atliq-hr-assist.git
   cd atliq-hr-assist

