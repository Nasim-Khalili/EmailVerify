# EmailVerify
Asynchronous OTP Email Verification System with Django, Celery & Redis

## Project Overview
EmailVerify is a Django-based project designed to securely verify user emails via OTP (One-Time Password) codes sent asynchronously using Celery and Redis. The system generates unique OTPs, stores them temporarily, and sends them via email in the background to enhance user experience without blocking the main server process.

This project demonstrates:
- Django REST Framework for building API endpoints.
- Celery task queue for asynchronous processing.
- Redis as a message broker and caching backend.
- JWT authentication integration.
- Modular, clean project architecture.
- Elasticsearch integration for logging user activities on posts.
- Kibana support for visualizing logs.

## Features
- Generate and store OTP codes linked to user emails.
- Send OTP emails asynchronously using Celery workers.
- Secure API endpoints for requesting OTP.
- Configurable expiration time for OTP codes.
- Full CRUD operations on posts with owner-based permissions.
- Log all post-related CRUD activities to Elasticsearch for audit and monitoring.
- Docker and docker-compose setup for easy deployment.

## Requirements
- Python 3.10+
- Django 5.x
- Celery 5.x
- Redis Server 5+
- Elasticsearch 7.x
- Other Python dependencies (see `requirements.txt`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Nasim-Khalili/emailverify.git
   cd emailverify
   pip install -r requirements.txt


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Nasim-Khalili/emailverify.git
   cd emailverify

   pip install -r requirements.txt
  ```
  
  python manage.py runserver
  ```
Start Redis server (locally or Docker):
  ```
  redis-server
 ```
  Run Celery worker
  ```
  celery -A myproject worker -l info
  ```
---

## Dockerization & Deployment with Nginx and HTTPS

To simplify deployment and ensure scalability, this project supports full Docker containerization including:

- **Django app** and **Celery worker** running inside Docker containers.
- **Redis** as a service container for caching and Celery broker.
- **Nginx** as a reverse proxy server managing HTTP/HTTPS traffic and serving static files.
- HTTPS support through Nginx for secure communication.

### Running the project with Docker

1. Build and start all services using Docker Compose:

   ```bash
   docker-compose up --build



### 👩‍💻 Contributing & Support

If you like this project or found it useful, feel free to:

- ⭐ Star this repository  
- 🍴 Fork it and customize it  
- 🐛 Report bugs or request features via Issues  

---

### 📬 Contact

Made with  by **Nasim Khalili**  


