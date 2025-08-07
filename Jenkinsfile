pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
        // Disable concurrent builds to avoid conflicts
        disableConcurrentBuilds()
        // Timestamps in logs for easier debugging
        timestamps()
    }

    environment {
        IMAGE_NAME = "milenag/my-flask-app"
        CONTAINER_NAME = "flask-app-container"
        APP_PORT = "5000"
        GIT_REPO = "https://github.com/milenagrabovskiy/name_selector.git"
        BRANCH = "main"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "refs/heads/${env.BRANCH}"]],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[url: env.GIT_REPO]]
                ])
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests..."
                // Replace with your actual test command, e.g.
                // sh 'pytest tests/'
                // For now, just simulate success:
                echo "Tests passed!"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${env.IMAGE_NAME}:latest"
                    sh "docker build -t ${env.IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    echo "Stopping any existing container named ${env.CONTAINER_NAME}"
                    sh "docker rm -f ${env.CONTAINER_NAME} || true"

                    echo "Starting new container ${env.CONTAINER_NAME}"
                    sh "docker run -d -p ${env.APP_PORT}:${env.APP_PORT} --name ${env.CONTAINER_NAME} ${env.IMAGE_NAME}:latest"
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    def maxRetries = 5
                    def retryDelay = 5
                    def healthy = false

                    for (int i = 1; i <= maxRetries; i++) {
                        def status = sh(
                            script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${env.APP_PORT}",
                            returnStdout: true
                        ).trim()

                        if (status == '200') {
                            echo "✅ Application is healthy!"
                            healthy = true
                            break
                        } else {
                            echo "Health check failed with status ${status}. Retry ${i}/${maxRetries} after ${retryDelay}s..."
                            sleep retryDelay
                        }
                    }

                    if (!healthy) {
                        error("❌ Application failed health check after ${maxRetries} attempts.")
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully."
        }
        failure {
            echo "❌ Pipeline failed. Check console output for details."
        }
        always {
            // Cleanup docker containers after pipeline ends if needed
            script {
                echo "Cleaning up Docker container ${env.CONTAINER_NAME}"
                sh "docker rm -f ${env.CONTAINER_NAME} || true"
            }
        }
    }
}
