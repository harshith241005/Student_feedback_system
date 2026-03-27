# Student Feedback System with Local CI/CD Pipeline

This project demonstrates a complete local DevOps workflow on one machine:

GitHub -> Jenkins -> Docker -> Ansible -> Running Flask Application

## 1. Project Structure

student-feedback-system/
- app/
  - app.py
  - database.py
  - requirements.txt
- templates/
  - index.html
  - feedback.html
- static/
  - style.css
- tests/
  - test_app.py
- ansible/
  - inventory
  - deploy.yml
- Dockerfile
- Jenkinsfile

## 2. Prerequisites

Install on the same machine:
- Git
- Python 3.11+
- Docker
- Jenkins
- Ansible

Install Docker collection for Ansible:

ansible-galaxy collection install community.docker

For Windows lab setup, install:
- Docker Desktop (with WSL2 backend recommended)
- Ansible (inside WSL Ubuntu, or via Git Bash-compatible environment)
- Jenkins (Windows service or Docker container)

## 3. Run Application Locally (without Docker)

1. Create and activate virtual environment.
2. Install dependencies:

pip install -r app/requirements.txt

3. Run app:

python app/app.py

4. Open:

http://localhost:5000

PowerShell shortcut scripts:

./scripts/setup_python.ps1
./scripts/run_tests.ps1
./scripts/run_app.ps1

## 4. Run with Docker

Build image:

docker build -t student-feedback-app .

Run container:

docker run --rm -p 5000:5000 -v ${PWD}/data:/app/data --name student-feedback-app student-feedback-app

PowerShell alternative:

docker run --rm -p 5000:5000 -v ${PWD}.Path/data:/app/data --name student-feedback-app student-feedback-app

Open:

http://localhost:5000

## 5. Deploy via Ansible

Run:

ansible-playbook -i ansible/inventory ansible/deploy.yml

This starts (or recreates) the feedback container and maps port 5000.

If Ansible is installed in WSL, run from Ubuntu terminal in the project folder.

Windows fallback command (uses host Ansible if available, else containerized Ansible):

powershell -ExecutionPolicy Bypass -File ./scripts/deploy_ansible.ps1

## 6. Jenkins Pipeline

The Jenkinsfile contains these stages:
1. Checkout
2. Build Docker Image
3. Run Tests
4. Deploy with Ansible
5. Smoke Test (checks http://localhost:5000)

To use in Jenkins:
1. Create a Pipeline job.
2. Connect to your GitHub repository.
3. Configure webhook from GitHub to Jenkins.
4. On each push, Jenkins will build, test, and deploy locally.

Note:
- Jenkinsfile supports both Linux and Windows agents.
- On Windows agents, Jenkins runs scripts/deploy_ansible.ps1, which falls back to containerized Ansible when ansible-playbook is not on PATH.

## 7. Functional Flow

1. Student submits name + feedback.
2. Flask receives POST request.
3. Feedback is stored in SQLite database.
4. Recent feedback is shown on homepage.
5. Full feedback list is available at /feedback.

## 8. Learning Outcomes

Students practice:
- Web development using Flask
- Database integration (SQLite)
- Containerization with Docker
- CI/CD with Jenkins
- Deployment automation with Ansible
