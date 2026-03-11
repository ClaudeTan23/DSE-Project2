# SmartStock Inventory Management System

## Project Overview
This project is a **web-based Inventory Management System** developed using **Python (Django Framework)**.  
It is designed to help businesses manage **products, stock levels, sales transactions, audit logs, and analytical reports** efficiently.

The system demonstrates the **effective application of programming languages, development frameworks, databases, and software development tools** to build a **robust and scalable software system**.

---

## Technology Stack

| Category | Technology |
|--------|------------|
| Programming Language | Python 3.14 |
| Backend Framework | Django |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Database | SQLite (Development), PostgreSQL (Production) |
| ORM | Django ORM |
| Authentication | Django Authentication System |
| Containerisation | Docker, Docker Compose |
| Web Server | Gunicorn |
| Version Control | Git, GitHub |
| Testing Framework | Django Test Framework |

---

# System Implementation & Core Functionalities

### Product Management
- Create, update, and delete products
- Category selection using dropdown menus
- Editable pricing and stock quantity
- Server-side validation and error handling

### Stock Management
- Stock IN and Stock OUT transactions
- Automatic stock adjustment
- Stock history tracking
- Low-stock alert notifications

### Sales Management
- Multi-item sales transactions
- Auto-generated invoice numbers
- Atomic transactions using `@transaction.atomic`
- Ensures data consistency and integrity

### Reporting & Analytics
- Daily, weekly, monthly, and yearly reports
- Query-based data aggregation
- No redundant reporting tables (computed dynamically)

### Audit Logging
- Tracks CREATE, UPDATE, and DELETE actions
- Stores:
  - User
  - HTTP method
  - Endpoint
  - Before & after data
- Improves accountability and traceability

## Development Environment (Docker)

A separate Docker configuration is provided for the development environment to allow easier testing and code updates.

### Run Development Containers

Build and start the development environment with:

```bash
docker compose -f docker-compose.dev.yml up --build
```

This command will:

- Build the development Docker image
- Start the **Django application**, **PostgreSQL database**, and **Nginx server**
- Mount the project folder into the container for development

### Restart Application Container

```bash
docker compose restart appseed-app
```
