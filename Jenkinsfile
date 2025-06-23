pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SonarQube'   
        DOCKER_IMAGE = 'tp3-api:latest'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('api') {
                    script {
                        sh "docker build -t $DOCKER_IMAGE ."
                    }
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                dir('api') {
                    sh 'pip install -r requirements.txt'
                    sh 'python3 -m unittest discover tests'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    dir('api') {
                        sh '''
                            sonar-scanner \
                              -Dsonar.projectKey=tp3-api \
                              -Dsonar.sources=. \
                              -Dsonar.host.url=$SONAR_HOST_URL \
                              -Dsonar.login=$SONAR_AUTH_TOKEN
                        '''
                    }
                }
            }
        }

        stage('PMD / Warnings Next Gen') {
            steps {
                recordIssues tools: [python()]
            }
        }

        stage('Deploy API Docker Container') {
            steps {
                script {
                    // Arrêter et supprimer si existe déjà
                    sh 'docker rm -f tp3_api_container || true'
                    // Lancer nouveau conteneur
                    sh 'docker run -d -p 5000:5000 --name tp3_api_container tp3-api:latest'
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline terminé."
        }
    }
}
