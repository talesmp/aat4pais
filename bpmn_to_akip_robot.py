#region Config

# -*- coding: utf-8 -*-
"""
# Preparing the Environment
- Importing the libraries
- Importing the BPMN (XML)
- Importing the AgileKip entity JSONs
"""

# Import Libraries
import os
import xml.etree.ElementTree as ET
import json
import re    # `camel_to_dash` function

# Files locations
current_directory = os.getcwd().replace('\\', '/')
print(current_directory)
robot_file_path = current_directory+'/AAT4PAIS/'
executed_kw_json_path = current_directory+'/BPMNandJSONs/FriendlyShoulder/executedKeywords.json'
bpmn_path = current_directory+'/BPMNandJSONs/FriendlyShoulder/friendlyShoulder.bpmn'
json_folder_path = current_directory+'/BPMNandJSONs/FriendlyShoulder/'

# def list_folders_in_directory(directory):
#   for root, dirs, files in os.walk(directory):
#       if '.git' in dirs:
#           dirs.remove('.git')  # Skip the .git folder
#       print("Folders in", root)
#       for folder in dirs:
#           print(os.path.join(root, folder))
# # Get current working directory
# current_directory = os.getcwd()
# # List all folders in the current directory and its subdirectories
# list_folders_in_directory(current_directory)

#endregion

#region Functions

"""# Functions
- [BPMN-DTish] find_dict_and_index_by_key_name: Find the dictionary and its index from the TC name
- [BPMN] find_tag_type_by_id: Find the type of a given element by it's tag using the ID
- [BPMN/BPMN-DTish] find_condition_expression_in_flow: Find the condition in the flow between two elements with their IDs
- [BPMN] find_outgoing_condition_expressions_from_gateway
- [Generic] camel_to_dash: Transform Camel Case String to Dash String
- [AKIP] filter_interactable_fields_from_json: Filter interactable fields from JSON
- [AKIP] extract_many_to_one_collection: Extract the collection of options of a given 'many-to-one' Complex Entity
"""

#region [BPMN-DT] Find the dictionary and its index from the TC name

def find_dict_and_index_by_key_name(dict_list, name):
    for i, dictionary in enumerate(dict_list):
        if dictionary['name'] == name:
            return dictionary, i
    return None, None
# If the function is called with [0] in the end, it returns only the dictionary, and with [1] it returns the index

#endregion

#region [BPMN] Find the type of a given element by it's tag using the ID

def find_tag_type_by_id(id):
    # Find the element with the specified id attribute
    element = root.find(".//*[@id='"+id+"']")
    # Extract the tag name without the bpmn: prefix
    tag_name = element.tag.split('}')[-1]
    # Return the tag name of the element
    return tag_name

# print(find_tag_type_by_id(tc_list[find_dict_and_index_by_key_name(tc_list, 'TC06')[1]]['elementId'][2]))
# startEvent; endEvent; sequenceFlow; userTask; exclusiveGateway; serviceTask; textAnnotation

#endregion

#region [BPMN/BPMN-DTish] Find the condition in the flow between two elements with the IDs in the list of Test Cases

def find_condition_expression_in_flow(source, target):
  # Find the refs
  sourceRef = root.find(".//bpmn:sequenceFlow[@sourceRef='"+source+"']", ns)
  targetRef = root.find(".//bpmn:sequenceFlow[@targetRef='"+target+"']", ns)
  # Find the sequence flow between the gateway and the task
  sequence_flow = root.find(".//bpmn:sequenceFlow[@sourceRef='"+source+"'][@targetRef='"+target+"']", ns)
  # Extract the condition expression from the sequence flow, if it exists
  try:
    condition_expression = sequence_flow.find("bpmn:conditionExpression", ns)
    condition = condition_expression.text
  except AttributeError:
    # If condition_expression is None, return a string specifying the lack of it
    condition = "No condition present."
  # Return the condition expression text (always a string? think about returning it to `None`)
  return condition
# print(find_condition_expression_in_flow(tc_list[2][1], tc_list[2][2]))

#endregion

#region [BPMN] Find the conditions in the outgoing flows of a given Gateway

def find_outgoing_condition_expressions_from_gateway(gatewayElementId):
  gatewayOutgoingConditionsDict = {}
  gatewayOutgoingConditionsDict['gatewayId']=gatewayElementId
  # Get a list of the outgoing flows
  exclusive_gateway = root.find('.//*[@id="'+gatewayElementId+'"]')
  outgoing_flows = [outgoing.text for outgoing in exclusive_gateway.findall('bpmn:outgoing', ns)]
  outgoingConditions = []
  # Find the outgoing sequence flows
  for outgoingFlow in outgoing_flows:
    sourceRef = root.find(".//bpmn:sequenceFlow[@sourceRef='"+gatewayElementId+"']", ns)
    # Find the outgoing sequence flow from its ID and the Gateway it's coming from (sourceRef)
    sequence_flow = root.find(".//bpmn:sequenceFlow[@id='"+outgoingFlow+"'][@sourceRef='"+gatewayElementId+"']", ns)
    # Extract the condition expression from the sequence flow, if it exists
    try:
      condition_expression = sequence_flow.find("bpmn:conditionExpression", ns)
      condition = condition_expression.text
    except AttributeError:
      # If condition_expression is None, return a string specifying the lack of it
      condition = "No condition present."
    # Return the condition expression text (always a string? think about returning it to `None`)
    outgoingConditionDict = {}
    # For each Outgoing Flow, a dictionary with the Flow Id and its Condition
    outgoingConditionDict[outgoingFlow]=condition
    # A list of dictionaries, each containing the Flow Id and its Condition
    outgoingConditions.append(outgoingConditionDict)
  gatewayOutgoingConditionsDict['outgoingConditions'] = outgoingConditions

  return gatewayOutgoingConditionsDict
#endregion

#region [Generic] Transform Camel Case String to Dash String

def camel_to_dash(string):
    # insert a dash before all capital letters
    string = re.sub('([A-Z])', r'-\1', string)
    # convert to lowercase and remove leading dash (if any)
    string = string.lower().lstrip('-')
    return string

#endregion

#region [AKIP] Filter interactable fields from JSON

def filter_interactable_fields_from_json(json_dict):
    filtered_dict = {}
    filtered_fields = []
    filtered_relationships = []
    for field in json_dict["fields"]:
        if "fieldReadOnly" not in field or not field["fieldReadOnly"]:
            filtered_fields.append({"fieldName": field["fieldName"], "fieldType": field["fieldType"], "fieldLocator": camel_to_dash(json_dict["name"])+'-'+field["fieldName"]})
    for relationship in json_dict["relationships"]:
        if "fieldReadOnly" not in relationship or not relationship["fieldReadOnly"]:
          filtered_fields.append({"fieldName": relationship["otherEntityName"]+'.'+relationship["otherEntityField"], "fieldType": relationship["relationshipType"], "otherEntityField": relationship["otherEntityField"], "fieldLocator": camel_to_dash(json_dict["name"])+'-'+relationship["otherEntityName"]})
    filtered_dict["jsonName"] = json_dict["name"]
    filtered_dict["jsonEntityType"] = json_dict["entityType"]
    if json_dict["entityType"] == 'user-task-form':
      filtered_dict["bpmnElementType"] = 'userTask'
      filtered_dict["bpmnElementId"] = json_dict["taskBpmnId"]
    if json_dict["entityType"] == 'start-form':
      filtered_dict["bpmnElementType"] = 'startEvent'
      filtered_dict["bpmnElementId"] = startEventId
    filtered_dict["formFieldPrefix"] = camel_to_dash(json_dict["name"])+'-'
    if filtered_fields:
      filtered_dict["jsonInteractableFields"] = filtered_fields
    return filtered_dict

#endregion

#region [AKIP] Extract the collection of options of a given 'many-to-one' Complex Entity
def extract_many_to_one_collection(input_list, target_substring):
    pattern = rf"{re.escape(target_substring)}\s*==\s*\'(\w+)\'"
    result = [match for string in input_list for match in re.findall(pattern, string)]
    filteredResult = list(set(result))
    return filteredResult

#endregion

#endregion

#region BPMN Manipulation

"""# Find all elements of interest in BPMN

Find all elements that are: Start Event; User Task; End Event; Exclusive Gateway

Next steps: Service Tasks?
"""

# Load the XML file
tree = ET.parse(bpmn_path)

# Get the root element
root = tree.getroot()

# Create a dictionary for the namespaces
ns = {'bpmn': root.tag.split('}')[0][1:], 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

# Define the tags of the BPMN Elements to search for
tags = ['startEvent', 'userTask', 'exclusiveGateway', 'endEvent']

interactableBpmnElementsDict_notDT = []
interactableBpmnElementIdsList_notDT = []
bpmnGateways_notDT = []
filteredUserTasks_notDT = []
filteredBpmnElementIds_notDT = []

# Iterate over all elements with the specified tags
for tag in tags:
    for elem in root.findall('.//bpmn:' + tag, ns):
        # Get the id attribute of the element
        tempDict = {}
        tempDict['bpmnElementId']=elem.get('id')
        tempDict['bpmnElementType']=tag
        # Get the ID of the Start Event
        if tag == 'startEvent':
          startEventId = elem.get('id')
        # Get a List and Dictionary of the Elements which should have Human interaction, i.e. Start Event and User Tasks
        if tag in ['startEvent', 'userTask'] and elem.get('id') not in interactableBpmnElementIdsList_notDT:
          interactableBpmnElementsDict_notDT.append(tempDict)
          interactableBpmnElementIdsList_notDT.append(elem.get('id'))
        # Get a Dictionary with all Exclusive Gateways, to find its related conditions later on
        if tag in ['exclusiveGateway'] and elem.get('id') not in bpmnGateways_notDT:
          bpmnGateways_notDT.append(tempDict)
        # Get a list of Start Event, User Tasks and End Events, which may be unnecessary, after all
        if tag in ['startEvent', 'userTask', 'endEvent'] and elem.get('id') not in filteredBpmnElementIds_notDT:
          filteredBpmnElementIds_notDT.append(elem.get('id'))
        # Get a list of User Tasks
        if tag=='userTask' and elem.get('id') not in filteredUserTasks_notDT:
          filteredUserTasks_notDT.append(elem.get('id'))
        elem_id = elem.get('id')

# print(startEventId)
print("\n====================================\n")
print("interactableBpmnElementsDict_notDT  \n")
print(interactableBpmnElementsDict_notDT)
print("\n====================================\n")
print("interactableBpmnElementIdsList_notDT  \n")
print(interactableBpmnElementIdsList_notDT)
print("\n====================================\n")
print("filteredBpmnElementIds_notDT  \n")
print(filteredBpmnElementIds_notDT)
print("\n====================================\n")
print("filteredUserTasks_notDT  \n")
print(filteredUserTasks_notDT)
print("\n====================================\n")
print("bpmnGateways_notDT  \n")
print(bpmnGateways_notDT)
print("\n====================================\n")

# Get all outgoing flow gateway conditions in alphabetical order
crudeOutgoingGatewayConditions = []
for gateway in bpmnGateways_notDT:
  gatewayId = gateway['bpmnElementId']
  conditionsDict = find_outgoing_condition_expressions_from_gateway(gatewayId)
  conditions = conditionsDict['outgoingConditions']
  for condition in conditions:
    for value in condition.values():
      if value != 'No condition present.':
        crudeOutgoingGatewayConditions.append(value)
crudeOutgoingGatewayConditions.sort()

# print(crudeOutgoingGatewayConditions)

#endregion

#region AgileKip Metadata JSON Manipulation

"""# Manipulating the AgileKip Metadata JSON files"""

# Getting the IDs and Names that bind the BPMN with the AgileKip Metadata JSON files
processIdFromBpmn = root.find('bpmn:process', ns).get('id')
domainNameFromProcessId = processIdFromBpmn.replace("Process", "")
domainNameInBpmnExpressions = domainNameFromProcessId[0].lower() + domainNameFromProcessId[1:]

# Deriving the JSON files names from the BPMN Process ID
processBindingJsonName = processIdFromBpmn
domainJsonName = domainNameFromProcessId
startFormJsonName = domainJsonName+"StartForm"

print(domainNameFromProcessId)

# Extracting the Interactable Fields of each Form from the AgileKip Metadata JSON files
jsonFilesContentDictList = []
for jsonFile in os.listdir(json_folder_path):
    if jsonFile.endswith('.json') and (jsonFile == domainNameFromProcessId+"StartForm.json" or jsonFile in [userTask+".json" for userTask in filteredUserTasks_notDT]):
        with open(os.path.join(json_folder_path, jsonFile)) as f:
            jsonFilesContentDictList.append(filter_interactable_fields_from_json(json.load(f)))
print("\n====================================\n")
print("jsonFilesContentDictList  \n")
print(jsonFilesContentDictList)
print('\n=====================================\n')

fieldLocators = set()
bpmnElementIds = []
unique_interactable_fields = set()
complex_entity_interactable_fields = set()
for e in jsonFilesContentDictList:
  # Extracting a list of the BPMN Element IDs
  bpmnElementIds.append(e['bpmnElementId'])
  # Extracting a list of form field locators in which there will be interaction
  for interactable_field in e['jsonInteractableFields']:
    fieldLocators.add((e['formFieldPrefix']+interactable_field['fieldName'], interactable_field['fieldLocator']))
    #fieldLocators.append(interactable_field['fieldLocator'])
    if interactable_field['fieldType'] == 'many-to-one':
      unique_interactable_fields.add((interactable_field['fieldName'], interactable_field['fieldType']))
    else:
      unique_interactable_fields.add((interactable_field['fieldName'], interactable_field['fieldType']))

# Sorting alphabetically to ease the understanding in the Robot file
fieldLocators = sorted(fieldLocators, key=lambda x: x[0])
print('\n=====================================\n')
print("fieldLocators  \n")
print(fieldLocators)
print('\n=====================================\n')

# Sorting by the type of field to ease the understanding in the Robot file
unique_interactable_fields = sorted(unique_interactable_fields, key=lambda x: x[1])
print('\n=====================================\n')
print("unique_interactable_fields  \n")
print(unique_interactable_fields)
print('\n=====================================\n')

# Extracting the Interactable Fields from each Form
# for element in bpmnElementIds:
#   # Selecting a specific Form
#   form = next((f for f in jsonFilesContentDictList if f['bpmnElementId'] == element), None)
#   print(form)
#   # Getting the Interactable Fields from the Form
#   interactableFields = form['jsonInteractableFields']
#   print(interactableFields)
#   print('======================================\n')

#endregion

#region Robot Framework Manipulation

# Manipulating the Robot Framework files

robotTestFileName = processIdFromBpmn+'_test.robot'
robotResourcesFileName = processIdFromBpmn+'_resources.robot'
with open(robot_file_path+robotTestFileName, 'w') as test, open(robot_file_path+robotResourcesFileName, 'w') as resources:
  # Adding a comment line to document the Prompt Command necessary for the execution of the Test Cases
  test.write('# Prompt Command to Execute a Specific Test Case: \n')
  test.write('# robot -i TC_Random '+robotTestFileName+'\n')
  # Settings section
  test.write('*** Settings ***\n')
  test.write('Library    FakerLibrary    #locale=pt_BR\n')
  test.write('Resource    '+robotResourcesFileName+'\n')
  test.write('Test Setup    kwFakerDataSetup\n')
  test.write('\n')
  resources.write('*** Settings ***\n')
  resources.write('Library    FakerLibrary    #locale=pt_BR\n')
  resources.write('Library    RPA.Browser.Selenium\n')
  resources.write('Library    String\n')
  resources.write('Library    RPA.Desktop\n')
  resources.write('\n')

  # Variables section
  test.write('*** Variables ***\n')
  test.write('@{TaskNames}    '+'  '.join(filteredUserTasks_notDT)+'\n\n')
  resources.write('*** Variables ***\n')
  resources.write('${url_home}    http://localhost:8080/\n')
  resources.write('${url_my_tasks}    ${url_home}my-candidate-tasks\n')
  # All AgileKip form field locators
  for fl in fieldLocators:
    resources.write('${locator-'+fl[0]+'}    '+fl[1]+'\n')
  resources.write('\n')

  # Test Cases section
  test.write('*** Test Cases ***\n')
  ### Blind  ###
  test.write('TC_Blind\n')
  test.write('    kwFakerDataSetup\n')
  test.write('    kwLogin\n')
  test.write('    kw'+startEventId+'\n')
  test.write('    WHILE    $processRunning == True\n')
  test.write('        kwFindFirstAvailableTask\n')
  for i, userTask in enumerate(filteredUserTasks_notDT):
    if i == 0:
        test.write('        IF    $found_task == "'+userTask+'"\n')
    else:
        test.write('        ELSE IF    $found_task == "'+userTask+'"\n')
    test.write('            kwFakerDataSetup\n')
    test.write('            kw'+userTask+'\n')
  test.write('        ELSE IF    $found_task == "No task available."\n')
  test.write('            ${processRunning}=    Set Variable    ${False}\n')
  test.write('            Set Test Variable    ${processRunning}\n')
  test.write('            BREAK\n')
  test.write('        END\n')
  test.write('    END\n')
  test.write('\n')
  ### 10 times batch execution of Blind  ###
  ### Implementation of executed keywords json
  test.write('TC_BlindBatch\n')
  test.write('    kwFakerDataSetup\n')
  test.write('    kwLogin\n')
  test.write('    FOR    ${i}    IN RANGE    10\n')
  test.write('        kwFakerDataSetup\n')
  test.write('        kw'+startEventId+'\n')
  test.write('        WHILE    $processRunning == True\n')
  test.write('            kwFindFirstAvailableTask\n')
  for i, userTask in enumerate(filteredUserTasks_notDT):
    if i == 0:
      test.write('            IF    $found_task == "'+userTask+'"\n')
    else:
      test.write('            ELSE IF    $found_task == "'+userTask+'"\n')
    test.write('                kwFakerDataSetup\n')
    test.write('                kw'+userTask+'\n')
  test.write('            ELSE IF    $found_task == "No task available."\n')
  test.write('                ${processRunning}=    Set Variable    ${False}\n')
  test.write('                Set Test Variable    ${processRunning}\n')
  test.write('                BREAK\n')
  test.write('            END\n')
  test.write('        END\n')
  test.write('    END\n')
  test.write('\n')
  ### Linear ###
  test.write('TC_Linear \n')
  test.write('    [Documentation]  Condition Expressions: \n...                  '+'\n...                  '.join(crudeOutgoingGatewayConditions)+'\n...  ===> arrange the following Keywords below according to the Conditions above:\n')
  test.write('    kwFakerDataSetup\n')
  test.write('    kwLogin\n')
  test.write('    kw'+'\n    kw'.join(interactableBpmnElementIdsList_notDT)+'\n')
  test.write('\n')
  ### 10 times batch execution of Linear ###
  test.write('TC_LinearBatch \n')
  test.write('    [Documentation]  Execute TC_Linear for i=10 consecutive times\n')
  test.write('    FOR    ${i}    IN RANGE    10\n')
  test.write('        Sleep    200ms\n')
  test.write('        kwFakerDataSetup\n')
  test.write('        # =====> Insert here the arranged Keywords according to TC_Linear above <====\n')
  test.write('        Close Browser\n')
  test.write('    END\n')
  test.write('\n')

  # Keywords section
  test.write('*** Keywords ***\n')
  resources.write('*** Keywords ***\n')

  ### Implementing the search for available tasks ###
  test.write('kwFindFirstAvailableTask\n')
  test.write('    Sleep    200ms\n')
  test.write('    kwMyTasks\n')
  test.write('    ${found_task}=    Set Variable    No task available.\n')
  test.write('    ${exist_available_task}=    Run Keyword And Return Status    Get Text  xpath=/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[8]\n')
  test.write('    IF    $exist_available_task == True\n')
  test.write('        FOR    ${taskName}    IN ZIP    ${TaskNames}\n')
  test.write('            ${task_definition_key_from_text}=    Get Text  xpath=/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[8]\n')
  test.write('            IF    $task_definition_key_from_text == $taskName\n')
  test.write('                ${found_task}=    Set Variable    ${taskName}\n')
  test.write('                BREAK\n')
  test.write('            END\n')
  test.write('        END\n')
  test.write('    END\n')
  test.write('    Set Test Variable    ${found_task}\n')
  test.write('\n')

  ### Implementing the Faker for each interactable field ###
  ### An interactable field is a non-fieldReadOnly in the AgileKip entity JSON ###
  test.write('kwFakerDataSetup\n')
  for uif in unique_interactable_fields:
    if uif[1] == 'Boolean':
      test.write('    ${faker-'+uif[0]+'}    FakerLibrary.Boolean\n')
      test.write('    Set Test Variable    ${faker-'+uif[0]+'}\n')
    if uif[1] == 'LocalDate':
      test.write('    ${faker-'+uif[0]+'}    FakerLibrary.Date\n')
      test.write('    Set Test Variable    ${faker-'+uif[0]+'}\n')
    if uif[1] == 'String':
      test.write('    ${faker-'+uif[0]+'}    FakerLibrary.Sentence  nb_words=8\n')
      test.write('    Set Test Variable    ${faker-'+uif[0]+'}\n')
    if uif[1] == 'Integer':
      test.write('    ${faker-'+uif[0]+'}    FakerLibrary.Random Int  min=1  max=10\n')
      test.write('    Set Test Variable    ${faker-'+uif[0]+'}\n')
    if uif[1] == 'many-to-one':
      test.write("    # double-check the following collection in 'ext_word_list' =====>                     <===== \n")
      ### https://github.com/talesmp/aat4pais/issues/5
      inputSubstring = "processInstance."+domainNameInBpmnExpressions+"."+uif[0]
      collectionResult = extract_many_to_one_collection(crudeOutgoingGatewayConditions, inputSubstring)
      for dictionary in jsonFilesContentDictList:
        for field in dictionary.get('jsonInteractableFields', []):
          if field.get('fieldName') == uif[0]:
            field['manyToOneOptions'] = collectionResult
      test.write("    ${faker-"+uif[0]+"}    FakerLibrary.Word  ext_word_list="+str(collectionResult)+"\n")
      test.write('    Set Test Variable    ${faker-'+uif[0]+'}\n')
  test.write('    ${processRunning}=    Set Variable    ${True}\n')
  test.write('    Set Test Variable    ${processRunning}\n')
  test.write('\n')

  ### Implementing the keywords related to logging in and going to My Tasks
  ### [TEST] ###
  test.write('kwLogin\n')
  test.write('    [Arguments]  \n')
  test.write('    [Documentation]  \n')
  test.write('    The user logs in\n')
  test.write('\n')
  ### [RESOURCES] ###
  resources.write('The user logs in\n')
  resources.write('    [Arguments]  \n')
  resources.write('    [Documentation]  \n')
  resources.write('    Open Available Browser    maximized=true\n')
  resources.write('    Go To    ${url_home}\n')
  resources.write('    Click Element When Visible       account-menu__BV_toggle_\n')
  resources.write('    Click Element When Visible       login\n')
  resources.write('    Wait Until Element Is Visible    login-page___BV_modal_header_\n')
  resources.write('    Input Text When Element Is Visible    username    admin\n')
  resources.write('    Input Text When Element Is Visible    password    admin\n')
  resources.write("    Click Element When Visible    //span[contains(.,'Remember me')]\n")
  resources.write("    Click Button When Visible    //button[@data-cy='submit'][contains(.,'Sign in')]\n")
  resources.write('    Sleep    500ms\n')
  resources.write('\n')
  ### [TEST] ###
  test.write('kwMyTasks\n')
  test.write('    [Arguments]  \n')
  test.write('    [Documentation]  \n')
  test.write('    The user is in MyTasks\n')
  test.write('\n')
  ### [RESOURCES] ###
  resources.write('The user is in MyTasks\n')
  resources.write('    [Arguments]  \n')
  resources.write('    [Documentation]  \n')
  resources.write('    Sleep    100ms\n')
  resources.write('    Go To    ${url_my_tasks}\n')
  resources.write('    Wait Until Element Is Visible    task-instance-heading\n')
  resources.write('\n')

  for ibed in interactableBpmnElementsDict_notDT:
    test.write('kw'+ibed['bpmnElementId']+'\n')
    test.write('    [Arguments]  \n')
    test.write('    [Documentation]  \n')
    test.write('    The user is in '+ibed['bpmnElementId']+'\n')
    resources.write('The user is in '+ibed['bpmnElementId']+'\n')
    resources.write('    [Arguments]  \n')
    resources.write('    [Documentation]  \n')
    resources.write('    Sleep    500ms  \n')
    if ibed['bpmnElementType'] == 'startEvent': 
      resources.write('    Go To    http://localhost:8080/process-definition/'+processIdFromBpmn+'/init \n')
    elif ibed['bpmnElementType'] == 'userTask': 
      resources.write('    Click Element If Visible    xpath:/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[12]/div[1]/button[1]  \n')
      resources.write('    Wait Until Page Contains    '+ibed['bpmnElementId']+'\n')
    resources.write('\n')

    test.write('    The user fills '+ibed['bpmnElementId']+'\n')
    resources.write('The user fills '+ibed['bpmnElementId']+'\n')
    resources.write('    [Arguments]  \n')
    resources.write('    [Documentation]  \n')
    if ibed['bpmnElementType'] == 'startEvent': 
      resources.write("    Wait Until Page Contains    Create or edit a \n")
    elif ibed['bpmnElementType'] == 'userTask': 
      resources.write("    Wait Until Page Contains    "+ibed['bpmnElementId']+" \n")
    ### using ibed['bpmnElementId'], find the object in jsonFilesContentDictList that has the same 'bpmnElementId' <<<===================================
    ### for each jsonInteractableFields in the said form, implement the keyword for each fieldType, and the said Faker input
    ### params(fieldType, locator, fakerData)
    for entry in jsonFilesContentDictList:
        if entry['bpmnElementId'] == ibed['bpmnElementId']:
            foundInteractableFields = entry['jsonInteractableFields']
    for field in foundInteractableFields:
      defFieldType = field['fieldType'] 
      defFieldName = field['fieldName']
      defFieldLocator = field['fieldLocator']
      if defFieldType in ('String', 'Integer','LocalDate'):
        resources.write('    Input Text When Element Is Visible    '+defFieldLocator+'    ${faker-'+defFieldName+'} \n')
      # elif fieldType=='Integer':
      #   resources.write('     \n')
      # elif fieldType=='LocalDate':
      #   resources.write('     \n')
      elif defFieldType =='Boolean':
        resources.write('    IF    ${faker-'+defFieldName+'} is True \n')
        resources.write('        Wait Until Element Is Visible    '+defFieldLocator+' \n')
        resources.write('        Select Checkbox    '+defFieldLocator+' \n')
        resources.write('    ELSE IF    ${faker-'+defFieldName+'} is False \n')
        resources.write('        Wait Until Element Is Visible    '+defFieldLocator+' \n')
        resources.write('        Unselect Checkbox    '+defFieldLocator+' \n')
        resources.write('    END \n')
      elif defFieldType =='many-to-one':
        defManyToOneOptions = field['manyToOneOptions']
        resources.write('    Click Element When Visible    '+defFieldLocator+' \n')
        for index, item in enumerate(defManyToOneOptions):
            if index==0:
              resources.write("    IF    '${faker-"+defFieldName+"}' == '"+item+"' \n") 
              resources.write("        Click Element When Visible     //option[@value='[object Object]'][contains(.,'"+item+"')] \n") 
            elif index == len(defManyToOneOptions) - 1: 
              resources.write("    ELSE IF    '${faker-"+defFieldName+"}' == '"+item+"' \n")  
              resources.write("        Click Element When Visible     //option[@value='[object Object]'][contains(.,'"+item+"')] \n") 
              resources.write('    END \n')
            else: 
              resources.write("    ELSE IF    '${faker-"+defFieldName+"}' == '"+item+"' \n") 
              resources.write("        Click Element When Visible     //option[@value='[object Object]'][contains(.,'"+item+"')] \n") 
    resources.write('\n')

    test.write('    The user submits '+ibed['bpmnElementId']+'\n')
    ### https://github.com/talesmp/aat4pais/issues/4
    resources.write('The user submits '+ibed['bpmnElementId']+'\n')
    resources.write('    [Arguments]  \n')
    resources.write('    [Documentation]  \n')
    resources.write('    Sleep    500ms  \n')
    resources.write('    Capture Page Screenshot  \n')
    if ibed['bpmnElementType'] == 'startEvent': 
      resources.write("    Click Button    save-entity \n")
    elif ibed['bpmnElementType'] == 'userTask': 
      resources.write("    Click Button    //button[@type='submit'][contains(.,'Complete')] \n")
    resources.write('\n')
    test.write('\n')



### https://github.com/talesmp/aat4pais/issues/3

# já estará com o `ibed`` (interactableBpmnElementIdsList_notDT) situado;
"""
[
  'RequestForm', 
  'TaskAnalyseComplaint', 
  'TaskReviewEscalation', 
  'TaskAcknowledge'
]
"""
# localizar `ibed` em `jsonFilesContentDictList` pelo `bpmnElementId`,
# para cada item em `jsonInteractableFields` fazer:
## pegar `fieldName`, `fieldType`, `fieldLocator e, se for `many-to-one`, pegar `manyToOneOptions`;
# pegar os dados de `manyToOneOptions`, contar o tamanho da lista e aí montar o IF/ELSE do Robot levando em conta o tamanho dessa lista

     

#endregion

#region Unused 
#####################################################################################################

# """# Hush... (mining)"""

# from collections import Counter

# # Load the JSON data from a file
# with open(executed_kw_json_path) as f:
#     data = json.load(f)

# # Extract the content of each inner list, excluding the first and last item of each
# inner_lists = [lst[1:-1] for lst in data]

# # Count the unique combinations of inner lists
# counts = Counter(tuple(inner_list) for inner_list in inner_lists)

# # Print the unique combinations and their counts
# for combination, count in counts.most_common():
#   formatted_count = f"{count:02d}"
#   formatted_combination = " => ".join(word[2:] for word in combination)
#   print(f"{formatted_count} executions: {formatted_combination}")

# # 10 times
# # 06 executions: RequestForm => TaskAcknowledge
# # 02 executions: RequestForm => TaskAnalyseComplaint
# # 02 executions: RequestForm => TaskAnalyseComplaint => TaskReviewEscalation

# # 20 times
# # 16 executions: RequestForm => TaskAcknowledge
# # 02 executions: RequestForm => TaskAnalyseComplaint
# # 02 executions: RequestForm => TaskAnalyseComplaint => TaskReviewEscalation

# # 35 times
# # 23 executions: RequestForm => TaskAcknowledge
# # 07 executions: RequestForm => TaskAnalyseComplaint
# # 05 executions: RequestForm => TaskAnalyseComplaint => TaskReviewEscalation

# # 50 times
# # 29 executions: RequestForm => TaskAcknowledge
# # 11 executions: RequestForm => TaskAnalyseComplaint
# # 10 executions: RequestForm => TaskAnalyseComplaint => TaskReviewEscalation

################################################################################################################################################################################################################################################


# """# Hush... (prior)"""

# # Searching for the Test Cases prior to execution

# import networkx as nx

# def generate_paths(G, node, path=None):
#     if path is None:
#         path = []

#     path.append(node)

#     if len(list(G.successors(node))) == 0:
#         yield path
#     else:
#         for next_node in G.successors(node):
#             yield from generate_paths(G, next_node, path.copy())

# # Create a directed graph
# G = nx.DiGraph()

# # Add nodes (tasks, gateways, and events) to the graph
# for element in tree.findall('.//bpmn:userTask|.//bpmn:exclusiveGateway|.//bpmn:endEvent|.//bpmn:startEvent', ns):
#     element_type = element.tag.split('}')[-1]
#     element_name = element.attrib.get('name', 'Unnamed')
#     G.add_node(element.attrib['id'], name=element_name, type=element_type)

# # Add edges (sequence flows) to the graph
# for element in tree.findall('.//bpmn:sequenceFlow', ns):
#     G.add_edge(element.attrib['sourceRef'], element.attrib['targetRef'], id=element.attrib['id'])

# # Generate all unique paths
# unique_paths = list(generate_paths(G, 'RequestForm'))

# # Print the unique paths (test cases)
# for i, path in enumerate(unique_paths, start=1):
#     print(f"Test case {i}:")
#     for j, node in enumerate(path):
#         node_type = G.nodes[node].get('type', '')
#         node_name = G.nodes[node].get('name', '')
#         print(f"  {j + 1}. {node_type} {node} {node_name}".strip())
#     print()

#endregion