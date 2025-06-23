pipeline {
    agent any

    tools {
        sonarScanner 'SonarScanner'
    }

    environment {
        SONARQUBE = 'SonarQube' 
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-creds', url: 'https://github.com/Cylia-845/TP3-Test.git'
            }
        }

        stage('Build') {
            steps {
                echo "No compilation needed, Python project."
            }
        }

        stage('Tests') {
            steps {
                sh 'pip install -r api/requirements.txt'
                sh 'pytest api/tests --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE}") {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=api-python \
                        -Dsonar.sources=api \
                        -Dsonar.python.version=3.10 \
                        -Dsonar.host.url=http://sonarqube2:9000
                    '''
                }
            }
        }

        stage('Static Analysis (Pylint)') {
            steps {
                sh '''
                    pip install pylint
                    pylint api/ --output-format=parseable > pylint-report.txt || true
                '''
                recordIssues(tools: [python()])
            }
        }

        stage('Docker Build & Deploy') {
            steps {
                sh 'docker build -t flask-api2 ./api'
                sh 'docker stop flask-api2 || true'
                sh 'docker rm flask-api2 || true'
                sh 'docker run -d -p 5000:5000 --name flask-api2 flask-api2'
            }
        }
    }
}
