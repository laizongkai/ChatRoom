pipeline {
    agent any
    stages {
        stage('準備') {
            steps {
                sh 'mkdir -p output'
            }
        }
        stage('執行') {
            steps {
                sh '''
                    echo "開始執行"
                    ls -la
                    echo "done" > output/result.txt
                '''
                script{
                    echo "start sub job connect wsl system"
                }
                build job: 'Test2' 
            }
        }
        stage('結果') {
            steps {
                sh 'cat output/result.txt'
            }
        }
    }
}
