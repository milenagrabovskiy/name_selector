pipeline {
    agent any

    options {
        wipeWorkspace()
        timeout(time: 15, unit: 'MINUTES')
    }

    environment {
        IMAGE_NAME = "milenag/my-flask-app"
        CONTAINER_NAME = "flask-app-container"
        APP_PORT = "5000"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                // Manual git checkout without wiping workspace extension
                checkout([$class: 'GitSCM',
                    branches: [[name: 'refs/heads/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[url: 'https://github.com/milenagrabovskiy/name_selector.git']]
                ])
            }
        }

        stage('Debug Workspace') {
            steps {
                sh 'ls -la'
                sh 'git status || echo "Not a git repo"'
            }
        }

        stage('Mock Tests') {
            steps {
                echo "Running regression tests..."
                // sh 'pytest' or your test command here
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Run Container') {
            steps {
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d -p ${APP_PORT}:${APP_PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Health Check') {
            steps {
                script {
                    def retries = 5
                    def delay = 3
                    def success = false

                    for (int i = 0; i < retries; i++) {
                        def status = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${APP_PORT}", returnStdout: true).trim()
                        if (status == '200') {
                            success = true
                            echo "✅ App is healthy!"
                            break
                        } else {
                            echo "Health check failed (status: ${status}). Retrying in ${delay}s..."
                            sleep delay
                        }
                    }

                    if (!success) {
                        error("❌ App failed health check.")
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
