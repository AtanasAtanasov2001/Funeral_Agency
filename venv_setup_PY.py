#!/usr/bin/env python3

import os
import sys
import subprocess

green = '\033[0;32m'
red = '\033[0;31m'
nc = '\033[0m'

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def install_dependency(dependency):
    try:
        run_command(f"which {dependency}")
        print(f"  {dependency}: {green}OK{nc}")
    except subprocess.CalledProcessError:
        print(f"sudo apt update && sudo apt install {dependency}")
        print(f"{red}ERROR{nc}: missing system dependency: {dependency}")
        print("       please install the following required dependencies first:")
        print("       * pip3")
        print("       * virtualenv")
        choice = input("Do you want to install it now? (y/n): ").lower()

        if choice == 'y':
            run_command(f"sudo apt update && sudo apt install {dependency}")
            print(f"  {dependency}: {green}Installed{nc}")
        else:
            print("Exiting...")
            sys.exit(3)

def main():
    # Set the name of the virtual environment
    if len(sys.argv) < 2:
        print("A name for the virtual environment is needed. Aborting...")
        sys.exit(1)

    venv_name = sys.argv[1]

    # Check if the virtual environment already exists
    if os.path.isdir(venv_name):
        print(f"Virtual environment '{venv_name}' already exists. Aborting.")
        sys.exit(1)

    # Update the system
    run_command("sudo apt update")
    run_command("sudo apt upgrade -y")
    run_command("sudo apt install -y python3")

    # Check and install dependencies
    for dependency in ["pip3", "virtualenv"]:
        install_dependency(dependency)

    # Create the virtual environment
    run_command(f"python3 -m venv {venv_name}")

    # Install packages from requirements.txt
    if os.path.isfile("requirements.txt"):
        run_command(f"{venv_name}/bin/pip install -r requirements.txt")
    else:
        print("No requirements.txt file found. Skipping package installation.")

    # Install Docker, kubectl, and Minikube in the virtual environment
    run_command(f"{venv_name}/bin/pip install docker")

    # Install kubectl
    run_command("curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl")
    run_command("chmod +x kubectl")
    run_command(f"mv kubectl {venv_name}/bin/")

    # Install Minikube
    run_command("curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64")
    run_command("chmod +x minikube-linux-amd64")
    run_command(f"mv minikube-linux-amd64 {venv_name}/bin/minikube")

    print(f"Virtual environment '{venv_name}' created and activated. You can deactivate it using 'deactivate'.")

if __name__ == "__main__":
    main()
