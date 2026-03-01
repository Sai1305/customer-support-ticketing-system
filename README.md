# Customer Support Ticketing System

A full-stack web application for managing customer support tickets, built with **Flask** and **MySQL**. Features role-based access control (Customer, Agent, Admin), real-time ticket tracking, agent assignment, and analytics reports.

---

## Features

- **User Authentication** — Register/Login with role-based access (Customer, Agent, Admin)
- **Ticket Management** — Create, view, and track support tickets with priority levels and categories
- **File Attachments** — Upload files (PNG, JPG, PDF, TXT) with tickets
- **Admin Dashboard** — Assign tickets to agents, update ticket statuses, view system-wide stats
- **Comments System** — Threaded comments on tickets with role-colored avatars
- **Reports & Analytics** — Interactive charts (doughnut + bar) showing ticket status breakdown
- **Email Notifications** — Console-based email alerts for ticket assignments and status changes
- **Responsive UI** — Professional sidebar layout with mobile support

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Flask 2.2.5, Flask-Login, Flask-SQLAlchemy |
| Database   | MySQL (via PyMySQL)                 |
| Frontend   | HTML5, CSS3 (custom), Font Awesome 6, Chart.js |
| Auth       | Werkzeug password hashing           |
| Config     | python-dotenv                       |

---

## Project Structure

```
customer_support/
├── app.py                  # App factory, admin seeding
├── config.py               # Configuration (env-based)
├── models.py               # User, Ticket, Comment models
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── routes/
│   ├── auth.py             # Login, Register, Logout
│   ├── tickets.py          # Ticket CRUD, file uploads
│   ├── admin.py            # Admin dashboard, assignment, status
│   └── reports.py          # Analytics data & overview
├── templates/
│   ├── base.html           # Layout (sidebar + topbar)
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── ticket_list.html    # Ticket listing with stats
│   ├── ticket_form.html    # New ticket form
│   ├── ticket_detail.html  # Ticket detail + comments
│   ├── admin_dashboard.html# Admin panel
│   └── reports.html        # Charts & analytics
├── static/
│   ├── css/style.css       # Custom stylesheet
│   ├── js/                 # JavaScript (if any)
│   └── uploads/            # User-uploaded files
└── utils/
    └── emailer.py          # Console email utility
```

---

## Prerequisites

- **Python** 3.8+
- **MySQL** 5.7+ running locally
- **pip** package manager

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sai1305/customer-support-ticketing-system.git
cd customer-support-ticketing-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

```sql
CREATE DATABASE flipkart_support;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/flipkart_support
```

### 6. Run the application

```bash
python app.py
```

The app will start at **http://127.0.0.1:5000**

---

## Default Credentials

| Role     | Email                  | Password    |
|----------|------------------------|-------------|
| Admin    | admin@flipkart.com     | Admin123    |

> The admin account is auto-created on first run. Register new Customer or Agent accounts via the registration page.

---

## User Roles

| Role       | Permissions                                                    |
|------------|----------------------------------------------------------------|
| **Customer** | Create tickets, view own tickets, add comments              |
| **Agent**    | View all tickets, add comments, view reports                |
| **Admin**    | All of the above + assign agents, change status, dashboard  |

---

## Screenshots

### Login Page
Professional gradient login with labeled form inputs.

### Ticket List
Data table with status/priority badges and summary stat cards.

### Admin Dashboard
Stats overview, agent assignment panel, and ticket management table.

### Reports
Interactive doughnut and bar charts with a percentage summary table.

---

## License

This project is for educational purposes.