pipeline {
    agent any

    environment {
        IMAGE_NAME = 'student-feedback-app'
        CONTAINER_NAME = 'student-feedback-app'
        HOST_PORT = '5000'
        CONTAINER_PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
                    } else {
                        bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest .'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} python -m pytest -q tests'
                    } else {
                        bat 'docker run --rm %IMAGE_NAME%:%BUILD_NUMBER% python -m pytest -q tests'
                    }
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'ansible-playbook -i ansible/inventory ansible/deploy.yml --extra-vars "image_name=${IMAGE_NAME}:latest container_name=${CONTAINER_NAME} host_port=${HOST_PORT} container_port=${CONTAINER_PORT}"'
                    } else {
                        bat 'powershell -ExecutionPolicy Bypass -File scripts/deploy_ansible.ps1 -ImageName "%IMAGE_NAME%:latest" -ContainerName "%CONTAINER_NAME%" -HostPort "%HOST_PORT%" -ContainerPort "%CONTAINER_PORT%"'
                    }
                }
            }
        }

        stage('Smoke Test') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'curl -fsS http://localhost:${HOST_PORT} > /dev/null'
                    } else {
                        bat 'powershell -ExecutionPolicy Bypass -Command "$resp = Invoke-WebRequest -Uri http://localhost:%HOST_PORT% -UseBasicParsing; if ($resp.StatusCode -ne 200) { throw \"Smoke test failed with status $($resp.StatusCode)\" }"'
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
