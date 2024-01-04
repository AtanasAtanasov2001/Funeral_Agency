# Funeral Agency Project Documentation
Introduction
The Funeral Agency project is a Flask-based web application designed to provide funeral-related services. The project utilizes Flask for the backend, Docker for containerization, and GitHub Actions for Continuous Integration/Continuous Deployment (CI/CD) to ensure a streamlined development process.

# Technologies Used
Python 

Flask: A lightweight Python web framework.

Docker: A platform for automating application deployment and managing containerized applications.

GitHub Actions: A CI/CD platform integrated with GitHub repositories.

SonarCloud: A cloud-based code quality and security analysis tool.

Grype: A vulnerability scanner for container images.

Snyk: A security platform that helps find and fix vulnerabilities in dependencies.

Trivy: A simple and comprehensive vulnerability scanner for containers.

# Project Structure
The project structure follows the typical Flask application structure with additional files for Docker configuration and GitHub Actions workflows.

# CI/CD Pipeline

There are three concecutive pipelines that are executed one after the other (Dependent on each other)
That is used by utilized the 'workflow_run: ' attribute in Github Actions
# Pipeline 1 ->  Tests


![image](https://github.com/AtanasAtanasov2001/Funeral_Agency/assets/73695057/57c5c641-3452-413e-9399-831b4d444664)

# Jobs in the Pipeline:
  1. Execute tests -> Using the pytest-coverage testing to verify the code is valid

# Pipeline 2 -> Build and Publish image (Dependant on the 'Tests' pipeline)


![image](https://github.com/AtanasAtanasov2001/Funeral_Agency/assets/73695057/7b7ec093-5dc6-4f15-8251-f90c27d0e517)

# Jobs in the pipeline:
  1. Scan-With-SonarCloud \
  2. Scan-With-Grype       - -> uses the integrated action to perform security scan over the code
  3. Scan-With-Snyk       /
  4. Build-Image -> builds the Docker image from the Dockerfile that is provided in the repository and utilizes the docker login action to login into Dockerhub via secrets and push the created image there
  5. Scan-With-Trivy -> Installing trivy scanning tool on the running agent and scanning the docker image, which is located in the Dockerhub
     

# Pipeline 3 -> Deploy image to Minikube
# Jobs in the pipeline:
  1. Deploy-To-Minikube -> uses the integrated action to start minikube on the running agent (ubuntu-latest)
                          Pulls the docker image from Dockerhub and applies the kubernetes manifests from the repository to create the following kubernetes instances:
 Deployment: Defined to have 3 replicas by defautl and uses the container with image, extracted from Dockerhub, on port 5000
 NodePort: For external access to the application, mapping the port that will be forwarded in the cluster (5000) to the port on which the service will be accessible externaly (5000) 

![image](https://github.com/AtanasAtanasov2001/Funeral_Agency/assets/73695057/a3078330-946e-4afe-8823-c446f25e4a69)



# Starting with Docker

The following commands need to be executed in order of the app to be run from within a container:

Requirements:

Docker installed (If on windows: Docker Desktop)
This reporitory cloned and having the path ending with '/Funeral_Agency'

# Step 1: Building the Docker Image
docker build -t image-name .
  # Additional information
      After creating the Docker image you can push it to DockerHub (Open source docker registry)

# Step 2: Running the Container
docker run -p 5000:5000 image-name

# Starting the application through Minikube (Local Kubernetes environment)

Minikube is a local kubernetes cluster with one master Node, allowing simple deployments.

Requirements:

Installed Docker
Installed Minikube
Installed kubectl
Docker Image in registry (DockerHub) -> The previous step:

# Step 1: Start Minikube:
minikube start

# Step 2: Apply the yaml files, allocated in the k8s_manifests folder
Note: the change the container image in the Deployment.yaml file to your image (However it may be named)
kubectl apply -f k8s_manifests/deployment.yaml  
kubectl apply -f k8s_manifests/nodePort.yaml

# Step 3: Verify that everything is up and running:
Note: There should be three pods running in the node. If for some reason you are in other namespace execute:

Get the pods:
kubectl get pods --all-namespaces

The status of the pods named funeral-agency-deployment< Unique identifier > (since we have three pods)

Get the Node Port:
kubectl get services funeral-agency-node-port    (Or the name of your NodePort)

# Step 4 expose the app that is running in your cluster and open it in your default web browser

minikube service funeral-agency-node-port    (Or the name of your NodePort)
