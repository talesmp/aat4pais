import os
import xml.etree.ElementTree as ET

def parse_bpmn(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

namespaces = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"}

def get_outgoing_flows(element):
    element = root.find(element)  # Convert the string element to an Element object
    if element is not None:
        return [outgoing.text for outgoing in element.findall(".//bpmn:outgoing", namespaces)]
    else:
        return []

def get_next_nodes(current_node, paths, visited):
    outgoing_flows = get_outgoing_flows(current_node)
    next_nodes = []

    for flow_id in outgoing_flows:
        target_ref = root.find(f".//*[@id='{flow_id}']").get("targetRef")
        if target_ref not in visited:
            next_nodes.append(target_ref)

    return next_nodes

def traverse(current_node, path, visited, paths):
    visited.add(current_node)
    path.append(current_node)

    if current_node.tag == "{BPMN_NAMESPACE}endEvent":
        paths.append(list(path))
    else:
        next_nodes = get_next_nodes(current_node, paths, visited)
        for next_node in next_nodes:
            traverse(next_node, path, visited, paths)

    path.pop()
    visited.remove(current_node)

folder_path = os.getcwd().replace('\\', '/')  # Replace with the actual folder path
folder_path = folder_path + "/BPMNandJSONs/GraphMapping/"
file_name = "test1.bpmn"  # Replace with the actual BPMN file name

file_path = os.path.join(folder_path, file_name)
root = parse_bpmn(file_path)

start_node_id = "RequestForm"
start_node = root.find(f".//*[@id='{start_node_id}']")

paths = []
traverse(start_node, [], set(), paths)
print(paths)