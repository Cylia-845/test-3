pipeline {
  agent any
  
  environment {
    SONARQUBE_SCANNER_HOME = tool 'SonarScanner' // install Jenkins
    SONAR_HOST_URL = 'http://sonarqube:9000' // l’URL SonarQube
    SONAR_AUTH_TOKEN = credentials('sonar-token') // credential Jenkins SonarQube
  }
  
  stages {
    
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    
    stage('Install dependencies') {
      steps {
        sh '''
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pylint selenium pytest
        '''
      }
    }
    
    stage('Run tests') {
      steps {
        sh 'pytest test_app.py'
      }
    }
    
    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('SonarQube') {
          sh '''
            sonar-scanner \
              -Dsonar.projectKey=TP3-TESTS \
              -Dsonar.sources=. \
              -Dsonar.host.url=${SONAR_HOST_URL} \
              -Dsonar.login=${SONAR_AUTH_TOKEN}
          '''
        }
      }
    }
    
    stage('Pylint Analysis') {
      steps {
        sh '''
          pylint *.py > pylint-report.txt || true
        '''
      }
      post {
        always {
          recordIssues tools: [python(pattern: 'pylint-report.txt')]
        }
      }
    }
    
    stage('Build Docker Image') {
      steps {
        sh '''
          docker build -t tp3-api:latest .
        '''
      }
    }
    
    stage('Deploy Docker Container') {
      steps {
        sh '''
          docker stop tp3-api || true
          docker rm tp3-api || true
          docker run -d -p 8000:5000 --name tp3-api tp3-api:latest
        '''
      }
    }
    
    stage('Run Selenium Tests') {
      steps {
        sh '''
          python selenium_test.py
        '''
      }
    }
  }
  
  post {
    always {
      echo 'Pipeline terminé'
    }
  }
}
