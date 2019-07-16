#!groovy

def branch
def commit
def tag
def opts

def owner_email = 'devopsfantv@tivo.com'
def whitelisted_branches = ['master', 'dev']

@Library('tivoPipeline') _

emailBreaks(owner_email) {
  node('docker') {
        stage('Git Checkout') {
            vars = checkout scm
            branch = vars.GIT_BRANCH
            commit = vars.GIT_COMMIT
            tag = branch.equals('master') ? 'stable' : branch.toLowerCase().replaceAll(/[^a-z0-9_\-]/, '')
            opts = "TAG='${tag}' SHELL='sh -x'"
            println( "branch=${branch}, tag=${tag}" )
        }

        stage('Build') {
            docker.withRegistry('http://docker.tivo.com', 'docker-registry') {
                sh "make pull build ${opts}"
            }
        }

        stage('Test') {
            sh "make test ${opts}"
        }

        stage('Deploy') {
            if( whitelisted_branches.contains(branch) ) {
                docker.withRegistry('http://docker.tivo.com', 'docker-registry') {
                    sh "make deploy ${opts}"
                }
            } else {
                println( "Branch [${branch}] not in deployment whitelist.  Skipping step." )
            }
        }
    }
}
