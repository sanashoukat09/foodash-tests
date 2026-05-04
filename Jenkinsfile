pipeline {
    agent any
    stages {
        stage('Start App') {
            steps {
                sh 'sudo systemctl start nginx || true'
                sh 'pm2 start /home/ubuntu/foodash/backend/server.js --name foodash-api || pm2 restart foodash-api'
                sh 'sleep 5'
            }
        }
        stage('Clone Test Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/sanashoukat09/foodash-tests.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t foodash-selenium-tests .'
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    mkdir -p test-results
                    docker run --rm \
                        -v $(pwd)/test-results:/tests/test-results \
                        foodash-selenium-tests \
                        pytest tests/ -v --html=test-results/report.html --self-contained-html
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'test-results/report.html', allowEmptyArchive: true
            emailext(
                to: "sanashoukat099@gmail.com",
                subject: "FooDash Tests - Build #${BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
                    <h2>FooDash Selenium Test Results</h2>
                    <p>Build: #${BUILD_NUMBER}</p>
                    <p>Status: ${currentBuild.currentResult}</p>
                    <p>Triggered by push to: ${env.GIT_BRANCH}</p>
                    <p>View full report: ${BUILD_URL}</p>
                """,
                mimeType: 'text/html',
                attachmentsPattern: 'test-results/report.html'
            )
        }
    }
}
