# K8s_in_python
Connects to a K8s cluster, Displays Pods, Containers of a Pod and events in the endpoints using Python.
## Requirements
Access to a running Kubernetes cluster.

Python3 is installed on your machine.

### Notes
The code is tested in Linux/Mac Operating Systems.

The scripts are written for bash shell.

## Prepare the Virtual Environemnt for python

Clone the directoty.
From the cloned directory, open the terminal and run the following commands in the terminal:
```
cd k8s_in_python
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
## Prepare the config file for connecting to the Kubernetes cluster
Go into the config directory.
Edit the path inside the config.json file with the full path to your kubeconfig file.
Example for the content of the kubeconfig file:
```
{
    "k8s_config":"/Users/mfarhadi/.kube/config"
}
```

## How to run the python code
```
python main.py
```
### To get the list of Pods:
Type in the terminal 1
### To get the list of containers of a Pod:
Type in the terminal 2
### To see the events in the cluster:
Type in the terminal 3

## How to exit the code:
Type in the terminal :q
