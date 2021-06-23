# K8s_in_python
Connects to a K8s cluster, Displays Pods, Containers of a Pod and events in the endpoints using Python.
## Requirements
Access to a running Kubernetes cluster.

Python3 is installed on your machine.

### Notes
The list of required packages are written in `requirements.txt`.

The code is only tested in Linux and Mac Operating Systems.

The scripts are written for bash shell.

## Prepare the Virtual Environemnt for python

Clone the directoty.
Go inside the cloned directory, open the terminal and run the following commands in the terminal:
```
cd k8s_in_python
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
The above commands create a virtual environemnt for the python code and installs the required packages from the `requirements.txt`.

## Prepare the config file for connecting to the Kubernetes cluster
Go inside the config directory and open the `config.json` file.

Replace the path inside the `config.json` file with the full path to your kubeconfig file.
Example of the content of the `config.json` file:
```
{
    "k8s_config":"/Users/mfarhadi/.kube/config"
}
```
Now everything is ready, you can run the code.

## How to run the python code

From the open terminal and within the created virtual environemnt, type the following command:
```
python main.py
```
A list of options will be displayed, you can exit the program by typing `:q`.
### To get the list of Pods:
Type in the terminal `1`
### To get the list of containers of a Pod:
Type in the terminal `2`
### To see the events in the cluster:
Type in the terminal `3`

## How to exit the code:
Type in the terminal `:q`
