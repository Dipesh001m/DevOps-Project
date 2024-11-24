# Built a CI/CD pipeline using AWS, Jenkins, SonarQube, Docker, and GitHub to automate code quality checks, containerization, and deployments.

## Project Overview
This project implements a CI/CD pipeline using **AWS**, **Jenkins**, **SonarQube**, **Docker**, and **GitHub** to automate code quality analysis, application containerization, and deployment workflows. The pipeline is designed to streamline deployment processes, enhance code quality, and reduce manual intervention.

---

## Tools Used

### 1. **AWS (Amazon Web Services)**
- **Purpose:** Hosting EC2 instances for Jenkins, SonarQube, and Docker.
- **Download Link:** [AWS Free Tier](https://aws.amazon.com/free/)
- **Key Steps:**
  - Launch three EC2 instances with Ubuntu or CentOS.
  - Ensure security groups allow necessary ports (e.g., 8080 for Jenkins, 9000 for SonarQube, and 2375 for Docker).

---

### 2. **Jenkins**
- **Purpose:** Automating build, test, and deployment processes.
- **Download Link:** [Jenkins Installation](https://www.jenkins.io/download/)
- **Key Steps:**
  1. SSH into the EC2 instance provisioned for Jenkins.
  2. Install Java (required for Jenkins):
     ```bash
     sudo apt update
     sudo apt install openjdk-11-jdk -y
     ```
  3. Add Jenkins repository and install Jenkins:
     ```bash
     curl -fsSL https://pkg.jenkins.io/debian/jenkins.io.key | sudo tee "/usr/share/keyrings/jenkins-keyring.asc" > /dev/null
     echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian binary/ | sudo tee "/etc/apt/sources.list.d/jenkins.list" > /dev/null
     sudo apt update
     sudo apt install jenkins -y
     ```
  4. Start Jenkins and access it on `http://<EC2-Public-IP>:8080`.

---

### 3. **SonarQube**
- **Purpose:** Static code analysis and quality checks.
- **Download Link:** [SonarQube Download](https://www.sonarsource.com/products/sonarqube/downloads/)
- **Key Steps:**
  1. SSH into the EC2 instance provisioned for SonarQube.
  2. Install prerequisites (Java, PostgreSQL):
     ```bash
     sudo apt update
     sudo apt install openjdk-11-jdk postgresql -y
     ```
  3. Download and configure SonarQube:
     ```bash
     wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-9.9.1.69595.zip
     unzip sonarqube-9.9.1.69595.zip
     mv sonarqube-9.9.1.69595 /opt/sonarqube
     ```
  4. Start SonarQube and access it on `http://<EC2-Public-IP>:9000`.

---

### 4. **Docker**
- **Purpose:** Application containerization for consistent deployment.
- **Download Link:** [Docker Installation](https://docs.docker.com/get-docker/)
- **Key Steps:**
  1. SSH into the EC2 instance provisioned for Docker.
  2. Install Docker:
     ```bash
     sudo apt update
     sudo apt install docker.io -y
     sudo systemctl start docker
     sudo systemctl enable docker
     ```
  3. Test Docker installation:
     ```bash
     docker run hello-world
     ```

---

### 5. **GitHub**
- **Purpose:** Version control and integration with Jenkins.
- **Link:** [GitHub](https://github.com/)
- **Key Steps:**
  1. Create a GitHub repository for the application.
  2. Push your application code to the repository.
  3. Configure a webhook in GitHub to trigger Jenkins builds automatically:
     - Navigate to `Settings > Webhooks > Add Webhook`.
     - Set the payload URL to `http://<Jenkins-EC2-Public-IP>:8080/github-webhook/`.
     - Choose `application/json` content type and select events for the webhook.

---

### 6. **Gmail Notifications**
- **Purpose:** Notify stakeholders of build successes or failures.
- **Configuration Steps:**
  1. In Jenkins, navigate to `Manage Jenkins > Configure System > E-mail Notification`.
  2. Set up SMTP configuration for Gmail:
     - SMTP server: `smtp.gmail.com`
     - Use SMTP authentication: Yes
     - Username: Your Gmail address
     - Password: Your app-specific password

---

## Workflow Summary
1. Jenkins monitors the GitHub repository for changes using webhooks.
2. Code changes trigger a build pipeline in Jenkins.
3. Jenkins invokes SonarQube for static code analysis and quality checks.
4. If successful, Jenkins builds a Docker image of the application and pushes it to Docker Hub.
5. Jenkins deploys the containerized application to the desired environment.
6. Build success or failure notifications are sent via Gmail.

---

## Example Pipeline Script
```groovy
pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/your-repo.git', branch: 'main'
            }
        }
        stage('Code Analysis') {
            steps {
                sh 'sonar-scanner'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t your-image-name .'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials']) {
                    sh 'docker push your-image-name'
                }
            }
        }
    }
    post {
        success {
            emailext subject: "Build Successful", body: "The build was successful!", recipientProviders: [[$class: 'DevelopersRecipientProvider']]
        }
        failure {
            emailext subject: "Build Failed", body: "The build failed!", recipientProviders: [[$class: 'DevelopersRecipientProvider']]
        }
    }
}
```


