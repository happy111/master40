pipeline {

    agent any

    environment {
        ONTOLOGY_VERSION = "0.1.0"
        ONTOLOGY_TYPE = "commercial"
        PACKET_ID = "ontology-${BUILD_NUMBER}"

        // Configure these in Jenkins Credentials / environment.
        AWS_REGION = credentials('aws-region')
        AWS_S3_BUCKET = credentials('ontology-s3-bucket')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Validate Ontology') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python scripts/validate_ontology.py
                '''
            }
        }

        stage('Identify Approver') {
            steps {
                sh '''
                    . .venv/bin/activate

                    python scripts/identify_approver.py \
                        "$ONTOLOGY_TYPE"
                '''
            }
        }

        stage('Approval Gate') {
            steps {
                input(
                    message: 'Has the ontology been reviewed and approved?',
                    ok: 'Approve and Continue',
                    submitter: 'ontology-reviewers'
                )
            }
        }

        stage('Record Approval') {
            steps {
                script {
                    def commitSha = sh(
                        script: 'git rev-parse HEAD',
                        returnStdout: true
                    ).trim()

                    sh """
                        . .venv/bin/activate

                        python scripts/approval.py \
                            --approve \
                            --approver ontology-reviewer@example.com \
                            --commit ${commitSha}
                    """
                }
            }
        }

        stage('Generate Manifest') {
            steps {
                sh '''
                    . .venv/bin/activate

                    python scripts/generate_manifest.py
                '''
            }
        }

        stage('Deploy to S3') {
            steps {
                sh '''
                    . .venv/bin/activate

                    export AWS_DEFAULT_REGION="$AWS_REGION"

                    python scripts/deploy_s3.py \
                        --bucket "$AWS_S3_BUCKET" \
                        --packet-id "$PACKET_ID"
                '''
            }
        }
    }

    post {
        success {
            echo 'Ontology approval and deployment completed successfully.'
        }

        failure {
            echo 'Ontology approval/deployment pipeline FAILED.'
        }
    }
}
