#!/bin/bash

green='\033[0;32m'
red='\033[0;31m'
nc='\033[0m'

# Set the name of the virtual environment
if [ -z "$1" ]; then 
    echo "A name for the virtual environment is needed. Aborting..."
    exit 1
fi
venv_name="$1"

# Check if the virtual environment already exists
if [ -d "$venv_name" ]; then
    echo "Virtual environment '$venv_name' already exists. Aborting."
    exit 1
fi

# Update the system
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3

for dependency in pip3 virtualenv; do
    if ! which "${dependency}" > /dev/null ; then
        echo "sudo apt update && sudo apt install $dependency"
        echo -e "${red}ERROR${nc}: missing system dependency: ${dependency}"
        echo "       please install the following required dependencies first:"
        echo "       * pip3"
        echo "       * virtualenv"
        read -p "Do you want to install it now? (y/n): " choice

        case "$choice" in
            [Yy]*)
                sudo apt update && sudo apt install "$dependency"
                echo -e "  ${dependency}: ${green}Installed${nc}"
                ;;
            *)
                echo "Exiting.."
                exit 3
                ;;
        esac
    else
        echo -e "  ${dependency}: ${green}OK${nc}"
    fi
done

# Create the virtual environment
python3 -m venv "$venv_name"

# Activate the virtual environment
source "$venv_name/bin/activate"

# Install packages from requirements.txt
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "No requirements.txt file found. Skipping package installation."
fi

# Install Docker, kubectl, and Minikube in the virtual environment
pip install docker

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
mv kubectl $venv_name/bin/

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube-linux-amd64
mv minikube-linux-amd64 $venv_name/bin/minikube

# deactivate

echo "Virtual environment '$venv_name' created and activated. You can deactivate it using 'deactivate'."
