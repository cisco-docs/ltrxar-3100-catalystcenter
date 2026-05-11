def setupLocalProvider(goVersion) {
    echo "Setting up local Catalyst Center provider with Go ${goVersion}..."

    sh """
        # Install Go
        curl -OL "https://go.dev/dl/go${goVersion}.linux-amd64.tar.gz"
        tar -C /usr/local -xzf "go${goVersion}.linux-amd64.tar.gz"

        # Set up Go environment
        export GOROOT=/usr/local/go
        export GOPATH=/go
        export PATH=\$GOPATH/bin:\$GOROOT/bin:\$PATH
        go version

        # Clone and build provider from source
        git clone https://github.com/CiscoDevNet/terraform-provider-catalystcenter.git /tmp/terraform-provider-catalystcenter
        cd /tmp/terraform-provider-catalystcenter
        git checkout main
        go install
    """

    // Create .terraformrc with dev_overrides
    sh '''
        cat > /root/.terraformrc << 'EOF'
provider_installation {
  # Use local provider binary built from source
  dev_overrides {
    "CiscoDevNet/catalystcenter" = "/go/bin"
  }

  # For all other providers, install them directly from their origin provider
  # registries as normal. If you omit this, Terraform will _only_ use
  # the dev_overrides block, and so no other providers will be available.
  direct {}
}
EOF
        cat /root/.terraformrc
    '''
}

pipeline {
    agent {
        docker {
            image 'danischm/nac:0.3.1-beta0'
            label 'digidev'
            args '-u root'
        }
    }

    triggers {
        cron(env.BRANCH_NAME == 'master' ? '0 5 * * *' : '')
    }

    environment {
        DD_GITHUB_TOKEN = credentials('DD_GITHUB_TOKEN')
        DD_INTERNAL_GITHUB_TOKEN = credentials('DD_INTERNAL_GITHUB_TOKEN')
        CC_USERNAME = credentials('CC_USERNAME')
        CC_PASSWORD = credentials('CC_PASSWORD')
        WEBEX_TOKEN = credentials('WEBEX_TOKEN')
        WEBEX_ROOM_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vNTFmMGNmODAtYjI0My0xMWU5LTljZjUtNWY0NGQ2ZTlmYWY0'
        GIT_COMMIT_MESSAGE = "${sh(returnStdout: true, script: 'git config --global --add safe.directory "*" && git log -1 --pretty=%B ${GIT_COMMIT}').trim()}"
        GIT_COMMIT_AUTHOR = "${sh(returnStdout: true, script: 'git show -s --pretty=%an').trim()}"
        GIT_EVENT = "${(env.CHANGE_ID != null) ? 'Pull Request' : 'Push'}"
    }

    options {
        disableConcurrentBuilds()
        newContainerPerStage()
        timeout(time: 2, unit: 'HOURS')
    }

    stages {
        stage('Lint') {
            steps {
                sh 'yamllint -s .'
                sh 'pytest -m validate'
            }
        }
        stage('Verify Netascode Documentation Impact') {
            steps {
                script {
                    dir('netascode-check') {
                        git url: 'https://wwwin-github.cisco.com/netascode/netascode.git',
                            branch: 'master',
                            credentialsId: 'DD_INTERNAL_GITHUB_TOKEN'
                        sh 'cd scripts && python3 generator.py --solution "catalyst_center" --versions all'
                    }
                }
            }
        }
        stage('Publish Documentation') {
            when {
                branch 'master'
            }
            steps {
                build job: '/netascode/netascode/master', wait: false
            }
        }
        stage('Generate Test Configurations') {
            steps {
                script {
                    def providerVersion = '0.5.11'  // Leave empty '' to use local build
                    def branchRef = env.CHANGE_TARGET ?: env.BRANCH_NAME
                    def scriptBranch = 'main'  // Change this to test different module branches

                    if (branchRef == 'dev' || providerVersion == '') {
                        // Build provider from source for dev branch or when version not specified
                        def goVersion = '1.25.4'
                        setupLocalProvider(goVersion)

                        // Generate test configs using local binary
                        sh """
                            python3 scripts/generate_test_configs.py \\
                                --branch ${scriptBranch} \\
                                --max-timeout 600 \\
                                --show-content
                        """
                    } else {
                        // Use published provider version
                        echo "Using published Catalyst Center provider version ${providerVersion}..."

                        sh """
                            python3 scripts/generate_test_configs.py \\
                                --branch ${scriptBranch} \\
                                --provider-version ${providerVersion} \\
                                --max-timeout 600 \\
                                --show-content
                        """
                    }
                }
            }
        }
        stage('Test CatalystCenter Terraform - NON_BULK') {
            parallel {
                stage('CatalystCenter 2.3.7.9 - NON_BULK') {
                    steps {
                        lock(resource: 'nac-ci-catalystcenter1') {
                            script {
                                def providerVersion = '0.5.11'  // Leave empty '' to use local build
                                def branchRef = env.CHANGE_TARGET ?: env.BRANCH_NAME

                                if (branchRef == 'dev' || providerVersion == '') {
                                    def goVersion = '1.25.4'
                                    setupLocalProvider(goVersion)
                                }

                                echo "Running tests WITHOUT use_bulk_api..."

                                echo "Running single-state deployment tests..."
                                sh 'pytest -m "cc_2379 and single_state and not use_bulk_api" -v'

                                sh '''
                                    mv catalystcenter_tf_2.3.7.9_xunit.xml catalystcenter_tf_2.3.7.9_single_state_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.9_report.html catalystcenter_tf_2.3.7.9_single_state_report.html || true
                                '''

                                echo "Running multi-state deployment tests..."
                                sh 'pytest -m "cc_2379 and multi_state and not use_bulk_api" -v'

                                sh '''
                                    mv catalystcenter_tf_2.3.7.9_multistate_global_xunit.xml catalystcenter_tf_2.3.7.9_multi_state_global_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_global_report.html catalystcenter_tf_2.3.7.9_multi_state_global_report.html || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_site_a_xunit.xml catalystcenter_tf_2.3.7.9_multi_state_site_a_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_site_a_report.html catalystcenter_tf_2.3.7.9_multi_state_site_a_report.html || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_site_b_xunit.xml catalystcenter_tf_2.3.7.9_multi_state_site_b_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_site_b_report.html catalystcenter_tf_2.3.7.9_multi_state_site_b_report.html || true
                                '''

                                echo "Cleaning up multi-state deployment..."
                                sh 'pytest -m "cc_2379 and multi_state and cleanup and not use_bulk_api" -v || true'

                                echo "Cleaning up terraform state files..."
                                sh '''
                                    find tests/integration/fixtures/catalystcenter/terraform_2379* -name "terraform.tfstate*" -delete || true
                                    find tests/integration/fixtures/catalystcenter/terraform_2379* -name ".terraform.lock.hcl" -delete || true
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            junit 'catalystcenter_tf_2.3.7.9_single_state_xunit.xml, catalystcenter_tf_2.3.7.9_multi_state_*_xunit.xml'
                            archiveArtifacts 'catalystcenter_tf_2.3.7.9_single_state_*.html, catalystcenter_tf_2.3.7.9_single_state_*.xml, catalystcenter_tf_2.3.7.9_multi_state_*.html, catalystcenter_tf_2.3.7.9_multi_state_*.xml'
                        }
                    }
                }
                stage('CatalystCenter 2.3.7.10 - NON_BULK') {
                    steps {
                        lock(resource: 'nac-ci-catalystcenter2') {
                            script {
                                def providerVersion = '0.5.11'  // Leave empty '' to use local build
                                def branchRef = env.CHANGE_TARGET ?: env.BRANCH_NAME

                                if (branchRef == 'dev' || providerVersion == '') {
                                    def goVersion = '1.25.4'
                                    setupLocalProvider(goVersion)
                                }

                                echo "Running tests WITHOUT use_bulk_api..."

                                echo "Running single-state deployment tests..."
                                sh 'pytest -m "cc_23710 and single_state and not use_bulk_api" -v'

                                sh '''
                                    mv catalystcenter_tf_2.3.7.10_xunit.xml catalystcenter_tf_2.3.7.10_single_state_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.10_report.html catalystcenter_tf_2.3.7.10_single_state_report.html || true
                                '''

                                echo "Running multi-state deployment tests..."
                                sh 'pytest -m "cc_23710 and multi_state and not use_bulk_api" -v'

                                sh '''
                                    mv catalystcenter_tf_2.3.7.10_multistate_global_xunit.xml catalystcenter_tf_2.3.7.10_multi_state_global_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_global_report.html catalystcenter_tf_2.3.7.10_multi_state_global_report.html || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_site_a_xunit.xml catalystcenter_tf_2.3.7.10_multi_state_site_a_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_site_a_report.html catalystcenter_tf_2.3.7.10_multi_state_site_a_report.html || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_site_b_xunit.xml catalystcenter_tf_2.3.7.10_multi_state_site_b_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_site_b_report.html catalystcenter_tf_2.3.7.10_multi_state_site_b_report.html || true
                                '''

                                echo "Cleaning up multi-state deployment..."
                                sh 'pytest -m "cc_23710 and multi_state and cleanup and not use_bulk_api" -v || true'

                                echo "Cleaning up terraform state files..."
                                sh '''
                                    find tests/integration/fixtures/catalystcenter/terraform_23710* -name "terraform.tfstate*" -delete || true
                                    find tests/integration/fixtures/catalystcenter/terraform_23710* -name ".terraform.lock.hcl" -delete || true
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            junit 'catalystcenter_tf_2.3.7.10_single_state_xunit.xml, catalystcenter_tf_2.3.7.10_multi_state_*_xunit.xml'
                            archiveArtifacts 'catalystcenter_tf_2.3.7.10_single_state_*.html, catalystcenter_tf_2.3.7.10_single_state_*.xml, catalystcenter_tf_2.3.7.10_multi_state_*.html, catalystcenter_tf_2.3.7.10_multi_state_*.xml'
                        }
                    }
                }
            }
        }
        stage('Regenerate Configs for Bulk API') {
            steps {
                script {
                    def providerVersion = '0.5.11'  // Leave empty '' to use local build
                    def branchRef = env.CHANGE_TARGET ?: env.BRANCH_NAME
                    def scriptBranch = 'main'

                    if (branchRef == 'dev' || providerVersion == '') {
                        sh """
                            python3 scripts/generate_test_configs.py \\
                                --branch ${scriptBranch} \\
                                --max-timeout 600 \\
                                --use-bulk-api \\
                                --show-content
                        """
                    } else {
                        sh """
                            python3 scripts/generate_test_configs.py \\
                                --branch ${scriptBranch} \\
                                --provider-version ${providerVersion} \\
                                --max-timeout 600 \\
                                --use-bulk-api \\
                                --show-content
                        """
                    }
                }
            }
        }
        stage('Test CatalystCenter Terraform - BULK') {
            parallel {
                stage('CatalystCenter 2.3.7.9 - BULK') {
                    steps {
                        lock(resource: 'nac-ci-catalystcenter1') {
                            script {
                                def providerVersion = '0.5.11'  // Leave empty '' to use local build
                                def branchRef = env.CHANGE_TARGET ?: env.BRANCH_NAME

                                if (branchRef == 'dev' || providerVersion == '') {
                                    def goVersion = '1.25.4'
                                    setupLocalProvider(goVersion)
                                }

                                echo "Running tests WITH use_bulk_api..."

                                echo "Running single-state deployment tests with bulk API..."
                                sh 'pytest -m "cc_2379 and single_state and use_bulk_api" -v'

                                sh '''
                                    mv catalystcenter_tf_2.3.7.9_bulk_xunit.xml catalystcenter_tf_2.3.7.9_single_state_bulk_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.9_bulk_report.html catalystcenter_tf_2.3.7.9_single_state_bulk_report.html || true
                                '''

                                echo "Running multi-state deployment tests with bulk API..."
                                sh 'pytest -m "cc_2379 and multi_state and use_bulk_api" -v'

                                sh '''
                                    mv catalystcenter_tf_2.3.7.9_multistate_global_bulk_xunit.xml catalystcenter_tf_2.3.7.9_multi_state_global_bulk_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_global_bulk_report.html catalystcenter_tf_2.3.7.9_multi_state_global_bulk_report.html || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_site_a_bulk_xunit.xml catalystcenter_tf_2.3.7.9_multi_state_site_a_bulk_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_site_a_bulk_report.html catalystcenter_tf_2.3.7.9_multi_state_site_a_bulk_report.html || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_site_b_bulk_xunit.xml catalystcenter_tf_2.3.7.9_multi_state_site_b_bulk_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.9_multistate_site_b_bulk_report.html catalystcenter_tf_2.3.7.9_multi_state_site_b_bulk_report.html || true
                                '''

                                echo "Cleaning up multi-state bulk deployment..."
                                sh 'pytest -m "cc_2379 and multi_state and cleanup and use_bulk_api" -v || true'

                                echo "Final cleanup of terraform state files..."
                                sh '''
                                    find tests/integration/fixtures/catalystcenter/terraform_2379* -name "terraform.tfstate*" -delete || true
                                    find tests/integration/fixtures/catalystcenter/terraform_2379* -name ".terraform.lock.hcl" -delete || true
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            junit 'catalystcenter_tf_2.3.7.9_*bulk_xunit.xml'
                            archiveArtifacts 'catalystcenter_tf_2.3.7.9_*bulk*.html, catalystcenter_tf_2.3.7.9_*bulk*.xml'
                        }
                    }
                }
                stage('CatalystCenter 2.3.7.10 - BULK') {
                    steps {
                        lock(resource: 'nac-ci-catalystcenter2') {
                            script {
                                def providerVersion = '0.5.11'  // Leave empty '' to use local build
                                def branchRef = env.CHANGE_TARGET ?: env.BRANCH_NAME

                                if (branchRef == 'dev' || providerVersion == '') {
                                    def goVersion = '1.25.4'
                                    setupLocalProvider(goVersion)
                                }

                                echo "Running tests WITH use_bulk_api..."

                                echo "Running single-state deployment tests with bulk API..."
                                sh 'pytest -m "cc_23710 and single_state and use_bulk_api" -v'

                                sh '''
                                    mv catalystcenter_tf_2.3.7.10_bulk_xunit.xml catalystcenter_tf_2.3.7.10_single_state_bulk_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.10_bulk_report.html catalystcenter_tf_2.3.7.10_single_state_bulk_report.html || true
                                '''

                                echo "Running multi-state deployment tests with bulk API..."
                                sh 'pytest -m "cc_23710 and multi_state and use_bulk_api" -v'

                                sh '''
                                    mv catalystcenter_tf_2.3.7.10_multistate_global_bulk_xunit.xml catalystcenter_tf_2.3.7.10_multi_state_global_bulk_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_global_bulk_report.html catalystcenter_tf_2.3.7.10_multi_state_global_bulk_report.html || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_site_a_bulk_xunit.xml catalystcenter_tf_2.3.7.10_multi_state_site_a_bulk_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_site_a_bulk_report.html catalystcenter_tf_2.3.7.10_multi_state_site_a_bulk_report.html || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_site_b_bulk_xunit.xml catalystcenter_tf_2.3.7.10_multi_state_site_b_bulk_xunit.xml || true
                                    mv catalystcenter_tf_2.3.7.10_multistate_site_b_bulk_report.html catalystcenter_tf_2.3.7.10_multi_state_site_b_bulk_report.html || true
                                '''

                                echo "Cleaning up multi-state bulk deployment..."
                                sh 'pytest -m "cc_23710 and multi_state and cleanup and use_bulk_api" -v || true'

                                echo "Final cleanup of terraform state files..."
                                sh '''
                                    find tests/integration/fixtures/catalystcenter/terraform_23710* -name "terraform.tfstate*" -delete || true
                                    find tests/integration/fixtures/catalystcenter/terraform_23710* -name ".terraform.lock.hcl" -delete || true
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            junit 'catalystcenter_tf_2.3.7.10_*bulk_xunit.xml'
                            archiveArtifacts 'catalystcenter_tf_2.3.7.10_*bulk*.html, catalystcenter_tf_2.3.7.10_*bulk*.xml'
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (env.TAG_NAME) {
                    sh 'cd scripts && python3 update_repos.py --release'
                } else if (env.BRANCH_NAME == "master") {
                    sh 'cd scripts && python3 update_repos.py'
                }
            }
            sh "BUILD_STATUS=${currentBuild.currentResult} python .ci/webex-notification-jenkins.py"
            cleanWs()
        }
    }
}