pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DEPLOY_HOOK_URL = 'https://api.render.com/deploy/srv-cvqghsh5pdvs73acv2mg?key=YuAoYfC94b8'
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

        stage('Trigger Render Deployment') {
            steps {
                script {
                    echo 'Triggering deployment on Render...'
                    sh "curl -X POST '${DEPLOY_HOOK_URL}'"
                }
            }
        }
    }
}
