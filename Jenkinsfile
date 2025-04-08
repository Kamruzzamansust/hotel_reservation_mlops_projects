pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps { 
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(
                        branches: [[name: '*/main']], 
                        extensions: [], 
                        userRemoteConfigs: [[
                            credentialsId: 'github-token', 
                            url: 'https://github.com/Kamruzzamansust/hotel_reservation_mlops_projects.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting Up Virtual Environment and Installing Dependencies') {
            steps { 
                script {
                    echo 'Setting up virtual environment and installing dependencies............'
                    sh 'python -m venv $VENV_DIR'
                    sh '. $VENV_DIR/bin/activate && pip install -r requirements.txt'
                }
            }
        }
    }
}
