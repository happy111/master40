pipeline {

    agent any

    environment {

        ONTOLOGY_NAME = "commercial-domain-model"
        ONTOLOGY_TYPE = "commercial"
        ONTOLOGY_VERSION = "0.1.0"

        /*
         * Change this to your actual Git repository URL.
         *
         * Example:
         * https://github.company.com/team/ontology-poc
         */
        GIT_REPOSITORY_URL =
            "https://your-git-server/your-repository"
    }

    stages {

        // =====================================================
        // 1. CHECKOUT
        // =====================================================

        stage('Checkout') {

            steps {

                checkout scm

                script {

                    env.COMMIT_SHA = sh(
                        script: 'git rev-parse HEAD',
                        returnStdout: true
                    ).trim()

                    echo """
                    ==========================================
                    ONTOLOGY SUBMISSION
                    ==========================================
                    Ontology : ${env.ONTOLOGY_NAME}
                    Version  : ${env.ONTOLOGY_VERSION}
                    Commit   : ${env.COMMIT_SHA}
                    ==========================================
                    """
                }
            }
        }


        // =====================================================
        // 2. INSTALL PYTHON DEPENDENCIES
        // =====================================================

        stage('Install Dependencies') {

            steps {

                sh '''
                    set -e

                    python3 -m venv .venv

                    . .venv/bin/activate

                    pip install --upgrade pip

                    pip install -r requirements.txt
                '''
            }
        }


        // =====================================================
        // 3. VALIDATE ONTOLOGY
        // =====================================================

        stage('Validate Ontology') {

            steps {

                sh '''
                    set -e

                    . .venv/bin/activate

                    python scripts/validate_ontology.py
                '''
            }
        }


        // =====================================================
        // 4. IDENTIFY APPROVER
        // =====================================================

        stage('Identify Approver') {

            steps {

                script {

                    env.APPROVER = sh(
                        script: '''
                            . .venv/bin/activate

                            python scripts/identify_approver.py \
                                "$ONTOLOGY_TYPE"
                        ''',
                        returnStdout: true
                    ).trim()

                    /*
                     * If your Python script prints extra text,
                     * you can parse the email here.
                     *
                     * For the simple POC, we recommend making
                     * identify_approver.py print ONLY the email.
                     */

                    echo """
                    ==========================================
                    APPROVER IDENTIFIED
                    ==========================================
                    Approver: ${env.APPROVER}
                    ==========================================
                    """
                }
            }
        }


        // =====================================================
        // 5. SEND APPROVAL EMAIL
        // =====================================================

        stage('Send Approval Email') {

            steps {

                script {

                    /*
                     * Link directly to the submitted Git commit.
                     *
                     * Example:
                     * https://git.company.com/project/repo/commit/abc123
                     */

                    env.ONTOLOGY_URL =
                        "${env.GIT_REPOSITORY_URL}/commit/${env.COMMIT_SHA}"

                    echo """
                    ==========================================
                    SENDING APPROVAL EMAIL
                    ==========================================
                    To      : ${env.APPROVER}
                    Ontology: ${env.ONTOLOGY_NAME}
                    Version : ${env.ONTOLOGY_VERSION}
                    Commit  : ${env.COMMIT_SHA}
                    Link    : ${env.ONTOLOGY_URL}
                    ==========================================
                    """

                    sh '''
                        set -e

                        . .venv/bin/activate

                        python scripts/send_approval_email.py \
                            --approver "$APPROVER" \
                            --ontology "$ONTOLOGY_NAME" \
                            --version "$ONTOLOGY_VERSION" \
                            --commit "$COMMIT_SHA" \
                            --url "$ONTOLOGY_URL"
                    '''
                }
            }
        }


        // =====================================================
        // 6. APPROVAL GATE
        // =====================================================

        stage('Reviewer Approval') {

            steps {

                script {

                    timeout(
                        time: 24,
                        unit: 'HOURS'
                    ) {

                        input(
                            message:
                                "Has ${env.ONTOLOGY_NAME} version ${env.ONTOLOGY_VERSION} been reviewed and approved?",
                            ok:
                                "Approve and Continue"
                        )
                    }
                }
            }
        }


        // =====================================================
        // 7. RECORD APPROVAL
        // =====================================================

        stage('Record Approval') {

            steps {

                sh '''
                    set -e

                    . .venv/bin/activate

                    python scripts/approval.py \
                        --approve \
                        --approver "$APPROVER" \
                        --commit "$COMMIT_SHA"
                '''
            }
        }


        // =====================================================
        // 8. GENERATE MANIFEST
        // =====================================================

        stage('Generate Manifest') {

            steps {

                sh '''
                    set -e

                    . .venv/bin/activate

                    python scripts/generate_manifest.py
                '''
            }
        }


        // =====================================================
        // 9. DEPLOY TO S3
        // =====================================================
        /*
         * Keep this commented until your AWS/S3 configuration
         * is ready.
         */

        /*
        stage('Deploy to S3') {

            steps {

                sh '''
                    set -e

                    . .venv/bin/activate

                    python scripts/deploy_s3.py \
                        --bucket "$AWS_S3_BUCKET" \
                        --packet-id "ontology-${BUILD_NUMBER}"
                '''
            }
        }
        */
    }


    // =========================================================
    // POST ACTIONS
    // =========================================================

    post {

        success {

            echo """
            ==================================================
                    ONTOLOGY POC SUCCESS
            ==================================================

            Ontology : ${env.ONTOLOGY_NAME}
            Version  : ${env.ONTOLOGY_VERSION}
            Commit   : ${env.COMMIT_SHA}
            Approver : ${env.APPROVER}

            Approval email was sent successfully.

            Reviewer approval was received.

            Manifest was generated.

            ==================================================
            """
        }


        failure {

            echo """
            ==================================================
                    ONTOLOGY POC FAILED
            ==================================================

            Ontology : ${env.ONTOLOGY_NAME}
            Commit   : ${env.COMMIT_SHA}

            Please check the failed Jenkins stage.

            ==================================================
            """
        }


        aborted {

            echo """
            ==================================================
                    ONTOLOGY POC ABORTED
            ==================================================

            Ontology : ${env.ONTOLOGY_NAME}
            Commit   : ${env.COMMIT_SHA}

            Pipeline was aborted before deployment.

            ==================================================
            """
        }
    }
}
