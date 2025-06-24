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
                withSonarQubeEnv('SonarQube') {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_AUTH_TOKEN')]) {
                        script {
                            // Récupérer le chemin du SonarScanner installé dans Jenkins
                            def scannerHome = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                            sh """
                                export PATH=\$PATH:${scannerHome}/bin
                                sonar-scanner \
                                    -Dsonar.projectKey=tp3-analyse \
                                    -Dsonar.sources=api \
                                    -Dsonar.exclusions=**/venv/**,**/__pycache__/** \
                                    -Dsonar.host.url=http://sonarqube:9000 \
                                    -Dsonar.login=\$SONAR_AUTH_TOKEN
                            """
                        }
                    }
                }
            }
        }



        stage('PMD / Warnings Next Gen') {
            steps {
                sh '''
                    python3 -m venv venv_pylint
                    . venv_pylint/bin/activate
                    pip install pylint
                    pylint api/app.py --output-format=parseable > pylint-output.txt || true
                '''
                recordIssues tools: [pylint(pattern: 'pylint-output.txt')]
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
