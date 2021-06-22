# -----------------------------------------------------------
# Connects to a K8s cluster, Displays Pods, Containers of a Pod
# and events endpoints using Python.
# Requires the full path to the k8s kube config file in the config.json file.
# 2021 Mozhdeh Farhadi
# email mfarhadi@irisa.fr
# -----------------------------------------------------------
import os
import json
import sys
import re
from kubernetes import client, config, watch
import constant


def get_pods_list_with_ip():
    """ Displays the list of pods with their IP address
        No parametes is needed.
    """
    # Get the handle to the relevant API
    v1 = client.CoreV1Api()
    print("Listing all the pods with their IPs:")
    # Call the method to get the list of all the pods
    pods_list = v1.list_pod_for_all_namespaces(watch=False)
    print("IP, Namespace, Pod's Name")
    # Print all the Pods
    for i in pods_list.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


def pod_exists(pod_name, name_space):
    """ Checks if the pods with the specified name and namespace exists and
        returns a boolean value accordingly.
        param 1: the pod name.
        param 2: the pod namespace.
    """
    pods_list = v1.list_pod_for_all_namespaces(watch=False)
    for i in pods_list.items:
        if i.metadata.name == pod_name and i.metadata.namespace == name_space:
            return True
    return False


def get_pods_containers(pod_name, name_space):
    """ Displays the list of containers for the pods specified with its name
        param 1: the pod name.
        param 2: the pod namespace.
    """
    # Check if the pod exists
    if pod_exists(pod_name, name_space):
        # Call the API to get the details of the Pod
        api_response = v1.read_namespaced_pod(name=pod_name, namespace=name_space)
        # Find the container Id in the Pod's details
        containerid = str(api_response.status.container_statuses[0].container_id)
        print("Container Id")
        print(containerid)
    else:
        print("The pod does not exist. Check the 'Pod Name' or the 'Pod Namespace'")


def get_events():
    """ Displays the list of latest events in the cluster's endpoints
        No parameters is needed.
    """
    # Define a regular expression which matches the IP addresses format.
    ip_pattern = re.compile("'ip': '\d+.\d+.\d+.\d+'")
    print('Event', 'Pod Name', 'Pod Namespace', 'Pod IP', 'Container ID', 'Node Name', 'Node IP')
    # Watch for the latest events in the cluster endpoints in all the namespaces
    stream = watch.Watch().stream(v1.list_endpoints_for_all_namespaces, timeout_seconds=5)
    # Loop in each event inside the stream of events
    for event in stream:
        # If the event had a content as subset, we go further.
        if event['object'].subsets:
            # Assign the event in a string
            event_str = str(event['object'].subsets)
            # If the event is not none, we go further and extract details about the event
            if event_str != 'None':
                # Get the type of event
                event_type = str(event['type'])
                # Use the IP address regular expression to find occurrances of the IP address in the string
                pattern_iterator = ip_pattern.finditer(event_str)
                # Loop on the found IP addresses
                for match in pattern_iterator:
                    # Get the Pod IP address
                    pod_ip = event_str[match.start() + constant.LEN_IP:match.end() - 1]

                    # Move forward in the event string to exactly after the end of the IP address
                    sub_str = event_str[match.end():]
                    # Define a regular expression to match the name convention in the event string"
                    find_indx = re.search("'node_name': '\w+[-]*[\d*[-]*]*", sub_str)
                    # If a name is found, process the string with details
                    if find_indx:
                        # Put the node name in the node_name variable
                        node_name = sub_str[find_indx.start(0) + constant.LEN_NODE_NAME:find_indx.end(0)]
                        # Get the substring which starts exactly after the end of node name
                        sub_str = sub_str[find_indx.end(0):]
                        # Find another name in the string
                        find_indx = re.search("'name': '.+'", sub_str)
                        # If the pod name is not empty
                        if find_indx:
                            pod_name = sub_str[find_indx.start(0) + constant.LEN_NAME:find_indx.end(0) - 1]
                            # Get the substring which starts exactly after the end of pod name
                            sub_str = sub_str[find_indx.end(0):]
                            # Find the namespece name
                            find_indx = re.search("'namespace': '.+'", sub_str)
                            # If the namespece name is not empty
                            if find_indx:
                                pod_namespace = sub_str[
                                                find_indx.start(0) + constant.LEN_NAMESPACE:find_indx.end(0) - 1]
                                # To get the container Id of the Pod, so we get handler to the relevant class
                                api_response = v1.read_namespaced_pod(name=pod_name, namespace=pod_namespace)
                                # Get the name of container Id(s) of the Pod
                                container_id = str(api_response.status.container_statuses[0].container_id)
                                # Get the IP address of the node where the container is running (on json it is
                                # written as host_ip)
                                node_ip = str(api_response.status.host_ip)
                                # Display all the details we find about the event in one line
                                print(event_type, pod_name, pod_namespace, pod_ip, container_id, node_name, node_ip)
            # There is no event
            else:
                print('Everything is calm... No event is found!')


def get_user_input():
    """ Get the user choice from the input
        No parameter is needed.
    """
    # Get user's choice as input
    user_input = input("Your choice? (Type ':q' to exit)")
    # If...else statement on the user's input
    if user_input == "1":
        # The list of all the pods in the cluster will be displayed
        get_pods_list_with_ip()
    elif user_input == "2":
        # The list of all the containers belonging to one pod will be displayed
        # Ask the user the name of the pod
        pod_name = input("Which Pod?")
        # Ask the user the name of the pod's namespace
        name_space = input("In which namespace?")
        # Call the method to display the containers of the pod in a specific namespace
        get_pods_containers(pod_name, name_space)
    elif user_input == "3":
        # The list of the latest events in the cluster's endpoints will be displayed
        get_events()
    elif user_input == ":q":
        # Exit the code
        sys.exit()
    else:
        print("Not a valid choice")


""" Here the main method starts
    It shows some options for the users to choose between 
    and display some information about the cluster to her

    To connect to the Kubernetes cluster, the path to the K8s' config file is needed.
    Check the "k8s_config" entry in the config.json.
"""
# Open the config.json file to read its content
with open("config/config.json") as json_config_file:
    data = json.load(json_config_file)

# Make sure if the specified k8s_config file exists
assert os.path.exists(data["k8s_config"]), "Could not find the K8s config file at " + data["k8s_config"]

# Load the Kubernetes configuration file in the config class of python
config.load_kube_config(data["k8s_config"])

v1 = client.CoreV1Api()

# Show the user what she can do
print("Press 1: to get the list of Pods.\n" +
      "Press 2: to get the list of containers of a Pod.\n" +
      "Press 3: to see the events in the cluster.\n" +
      "Press q: to exit.")

# Ask the user what she wants to do
while True:
    get_user_input()
