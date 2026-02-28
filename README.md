# Personal Organizer (Flask + Docker)

A Dockerized Flask web application with user authentication, PostgreSQL backend, and production-ready setup using Gunicorn and Docker Compose.

This project is designed as a foundation for a personal organizer application where users can manage links(wishlist), tasks, and journal entries.
The focus of this repository is **clean backend architecture, containerization, and environment-based configuration**.

---

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** Session based authentication
- **Web Server:** Gunicorn
- **Containerization:** Docker & Docker Compose
- **Configuration:** Environment variables ('.env')
- **Persistence:** Docker volumes
- **Health Checks:** PostgreSQL service healthcheck

---

## Project Architecture
- **Web**
    Flask application running with Gunicorn inside a Docker container.

- **db**
    PostgreSQL database container with  persistent storage via Docker volumes.

- **Volumes**
    Used to persist database data across container restarts.
- **Environment Variables**
    All sensitive configuration (database credentials, secret key) is handled via environment variables.
---
## Installation & Setup
**Environment Configuation**
Create a '.env' file in the root directory:
```env
   SECRET_KEY=your_secret_key
   POSTGRES_USER=atahan
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=flask_db
   DATABASE_URL=postgresql+psycopg2://app_user:change_me@db:5432/flask_db
```
Run with Docker:
```
docker compose up --build
```

---
### Clone the repository
```bash
git clone <repo-url>
cd Personal-Organizer
```
---
### Roadmap
[x] Base Setup: Flask + PostgreSQL + Docker integration.

[x] Authentication: Secure session-based login/register system.

[x] Wishlist Manager: Store and track product links from different websites.

[ ] Task Board: A simple To-Do list to manage daily activities.

[ ] Daily Journal: A private area to write and save personal notes.

---
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
