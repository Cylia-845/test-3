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
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                dir('api') {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        ./venv/bin/pip install -r requirements.txt
                        ./venv/bin/python -m unittest discover tests
                    '''
                }
            }
        }


        stage('SonarQube Analysis') {
            steps {
                dir('api') {
                    withSonarQubeEnv("${SONARQUBE_SERVER}") {
                        script {
                            def scannerHome = tool 'SonarScanner'
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=tp3-api \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=http://sonarqube2:9000
                            """
                        }
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
                sh '''
                    docker rm -f tp3_api_container || true
                    docker run -d -p 5000:5000 --name tp3_api_container tp3-api:latest
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline terminé."
        }
    }
}
