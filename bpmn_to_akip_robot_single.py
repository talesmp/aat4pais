#region Config and Auxiliary Functions

# Import Libraries
import os
import xml.etree.ElementTree as ET
import json
import glob   # `find_files_with_extension` function
import re     # `camel_to_dash` function

  #region [Generic] Finding Files with Extension

# [General] Finding Files with Extension
def find_files_with_extension(directory, extension):
    return glob.glob(f"{directory}/*.{extension}")

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

  #region [AKIP] Filter interactable fields from JSON

def filter_interactable_fields_from_json(json_dict, startEventId):
    filtered_dict = {}
    filtered_fields = []
    # filtered_relationships = []
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

  #region [Generic] Transform Camel Case String to Dash String

def camel_to_dash(string):
    # insert a dash before all capital letters
    string = re.sub('([A-Z])', r'-\1', string)
    # convert to lowercase and remove leading dash (if any)
    string = string.lower().lstrip('-')
    return string

  #endregion

#endregion

#region [Main] Process Folder Function
def process_folder_function(process_folder_name, current_directory):

  assessment_process_models_path = current_directory+'/AssessmentProcessModels/'
  process_folder_path = assessment_process_models_path+process_folder_name+'/'
  bpmn_path = find_files_with_extension(process_folder_path, 'bpmn')[0].replace('\\', '/')

  executed_kw_json_path = process_folder_path+'executedKeywords-'+process_folder_name+'.json'


  #region BPMN Manipulation

  """ 
  Find all elements of interest in BPMN
  Find all elements that are: Start Event; User Task; End Event; Exclusive and Inclusive Gateways
  Next steps: Service Tasks?
  """

  # Load the XML file
  tree = ET.parse(bpmn_path)

  # Get the root element
  root = tree.getroot()

  # Create a dictionary for the namespaces
  ns = {'bpmn': root.tag.split('}')[0][1:], 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

  # Define the tags of the BPMN Elements to search for
  tags = ['startEvent', 'userTask', 'exclusiveGateway', 'inclusiveGateway', 'endEvent']

  interactableBpmnElementsDict = []
  interactableBpmnElementIdsList = []
  # bpmnGateways = []
  filteredUserTasks = []
  filteredBpmnElementIds = []

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
          if tag in ['startEvent', 'userTask'] and elem.get('id') not in interactableBpmnElementIdsList:
            interactableBpmnElementsDict.append(tempDict)
            interactableBpmnElementIdsList.append(elem.get('id'))
          # [deprecated] Get a Dictionary with all Exclusive and Inclusive Gateways, to find its related conditions later on
          # if tag in ['exclusiveGateway','inclusiveGateway'] and elem.get('id') not in bpmnGateways:
          #   bpmnGateways.append(tempDict)
          # Get a list of Start Event, User Tasks and End Events, which may be unnecessary, after all
          if tag in ['startEvent', 'userTask', 'endEvent'] and elem.get('id') not in filteredBpmnElementIds:
            filteredBpmnElementIds.append(elem.get('id'))
          # Get a list of User Tasks
          if tag=='userTask' and elem.get('id') not in filteredUserTasks:
            filteredUserTasks.append(elem.get('id'))

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

  jsonFilesContentDictList = []
  jsonFilesList = find_files_with_extension(process_folder_path, 'json')
  for jsonFile in jsonFilesList:
    with open(os.path.join(process_folder_path, jsonFile)) as f:
      tempJsonFilesContentDict = json.load(f)  # Fix: Assign the loaded JSON to a variable
      if 'entityType' in tempJsonFilesContentDict and tempJsonFilesContentDict['entityType'] in ['start-form', 'user-task-form']:
        jsonFilesContentDictList.append(filter_interactable_fields_from_json(tempJsonFilesContentDict, startEventId))

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

  # Sorting by the type of field to ease the understanding in the Robot file
  unique_interactable_fields = sorted(unique_interactable_fields, key=lambda x: x[1])

  #endregion

  #region Robot Framework Files Generation

  # Manipulating the Robot Framework files
    # Faker Library documentation: https://marketsquare.github.io/robotframework-faker/

  robotTestFileName = processIdFromBpmn+'_test.robot'
  robotResourcesFileName = processIdFromBpmn+'_resources.robot'
  with open(process_folder_path+robotTestFileName, 'w') as test, open(process_folder_path+robotResourcesFileName, 'w') as resources:
    # Adding a comment line to document the Prompt Command necessary for the execution of the Test Cases
    test.write('# Prompt Command to Execute a Specific Test Case: \n')
    test.write('# robot -i TC_Random '+robotTestFileName+'\n')
    # Settings section
    test.write('*** Settings ***\n')
    test.write('Library    FakerLibrary    #locale=pt_BR \n')
    test.write('Library    OperatingSystem \n')
    test.write('Library    Collections \n')
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
    test.write('@{TaskNames}    '+'  '.join(filteredUserTasks)+'\n\n')
    resources.write('*** Variables ***\n')
    resources.write('${url_home}    http://localhost:8080/\n')
    resources.write('${url_my_tasks}    ${url_home}my-candidate-tasks\n')
    # All AgileKip form field locators
    for fl in fieldLocators:
      resources.write('${locator-'+fl[0]+'}    '+fl[1]+'\n')
    resources.write('\n')

    # Test Cases section
    test.write('*** Test Cases ***\n')
    ### 10 times batch execution of Blind  ###
    ### Implementation of executed keywords json
    test.write('TC_BlindBatch\n')
    test.write('    ${kw_executed}=    Create List\n')
    test.write('    kwFakerDataSetup\n')
    test.write('    kwLogin\n')
    test.write('    FOR    ${i}    IN RANGE    10\n')
    test.write('        ${inner_list}=    Create List\n')
    test.write('        kwFakerDataSetup\n')
    test.write('        kw'+startEventId+'\n')
    test.write('        Append To List    ${inner_list}    Start of Execution #${i}\n')
    test.write('        Append to List    ${inner_list}    '+startEventId+'\n')
    test.write('        WHILE    $processRunning == True\n')
    test.write('            kwFindFirstAvailableTask\n')
    for i, userTask in enumerate(filteredUserTasks):
      if i == 0:
        test.write('            IF    $found_task == "'+userTask+'"\n')
      else:
        test.write('            ELSE IF    $found_task == "'+userTask+'"\n')
      test.write('                kwFakerDataSetup\n')
      test.write('                kw'+userTask+'\n')
      test.write('                Append To List    ${inner_list}    '+userTask+'\n')
    test.write('            ELSE IF    $found_task == "No task available."\n')
    test.write('                ${processRunning}=    Set Variable    ${False}\n')
    test.write('                Set Test Variable    ${processRunning}\n')
    test.write('                BREAK\n')
    test.write('            END\n')
    test.write('        END\n')
    test.write('        Append To List    ${inner_list}    End of Execution #${i} \n')
    test.write('        Append To List    ${kw_executed}    ${inner_list} \n')
    test.write('    END\n')
    test.write('    ${json_string}=    Evaluate    json.dumps(${kw_executed}, indent=4) \n')
    test.write('    Create File    '+executed_kw_json_path+'    ${json_string} \n')
    test.write('    ${data}=    Evaluate    json.loads(open("'+executed_kw_json_path+'").read()) \n')
    test.write("    ${execution_paths}=    Evaluate    [' => '.join(execution[1:-1]) for execution in $data] \n")
    test.write('    ${execution_counts}=    Evaluate    dict(collections.Counter($execution_paths))    modules=collections \n')
    test.write('    ${output}=  Evaluate  "{} times\\\\n".format(len($data)) + '+"'\\\\n'.join(["+'"{} executions: {}".format(count, path) for path, count in $execution_counts.items()]) \n')
    test.write('    Create File    '+process_folder_path+'executionsCounter-'+process_folder_name+'.txt    ${output} \n')
    test.write('\n')
    ### Blind  ###
    test.write('TC_Blind\n')
    test.write('    kwFakerDataSetup\n')
    test.write('    kwLogin\n')
    test.write('    kw'+startEventId+'\n')
    test.write('    WHILE    $processRunning == True\n')
    test.write('        kwFindFirstAvailableTask\n')
    for i, userTask in enumerate(filteredUserTasks):
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
    ### Linear ###
    test.write('TC_Linear \n')
    test.write('    [Documentation]  Arrange the following Keywords below according to the desired test path:\n')
    test.write('    kwFakerDataSetup\n')
    test.write('    kwLogin\n')
    test.write('    kw'+'\n    kw'.join(interactableBpmnElementIdsList)+'\n')
    test.write('\n')

    # Keywords section
    test.write('*** Keywords ***\n')
    resources.write('*** Keywords ***\n')

    ### Implementing the search for available tasks ###
    test.write('kwFindFirstAvailableTask\n')
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
    test.write('        IF    $found_task == "No task available."\n')
    test.write('            ${processRunning}=    Set Variable    ${False}\n')
    test.write('            Set Test Variable    ${processRunning}\n')
    test.write('            ${found_task}=    Set Variable    ${task_definition_key_from_text}\n')
    test.write('            Set Test Variable    ${found_task}\n')
    test.write('            Fatal Error    Unexpected task found! \n')
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
    resources.write('    Sleep    500ms\n')
    resources.write('    Go To    ${url_my_tasks}\n')
    resources.write('    Wait Until Element Is Visible    task-instance-heading\n')
    resources.write('\n')

    """ Issue 7 Implement Arguments strategies for each interactable field

      kwRequestForm
      [Arguments]    ${argTest_description}=${faker-description}    ${argTest_date}=${faker-date}
      [Documentation]  
      The user is in RequestForm
      The user fills RequestForm    ${argTest-description}    ${argTest-date}
      The user submits RequestForm

    The user fills RequestForm
      [Arguments]    ${argRes_description}=${faker-description}    ${argRes_date}=${faker-date}
      [Documentation]  
      Wait Until Page Contains    Create or edit a 
      Input Text When Element Is Visible    friendly-shoulder-start-form-description    ${argRes_description}
      Input Text When Element Is Visible    friendly-shoulder-start-form-date    ${argRes_description}
    """
    
    for ibed in interactableBpmnElementsDict:
      test.write('kw'+ibed['bpmnElementId']+'\n')
      test.write('    [Arguments]  \n')
      test.write('    [Documentation]  \n')
      test.write('    The user is in '+ibed['bpmnElementId']+'\n')
      resources.write('The user is in '+ibed['bpmnElementId']+'\n')
      resources.write('    [Arguments]  \n')
      resources.write('    [Documentation]  \n')
      resources.write('    Sleep    500ms  \n')
      if ibed['bpmnElementType'] == 'startEvent': 
        resources.write('    Go To    http://localhost:8080/process-definition/'+processIdFromBpmn+'/init \n')  # Has to be the ID from the BPMN => OK!
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
          resources.write('    Click Element When Visible    '+defFieldLocator+' \n')
          resources.write("    ${list_options}=    Get WebElements    //select[@id='"+defFieldLocator+"']/option \n")
          resources.write('    ${options_length}=    Get Length    ${list_options} \n')
          resources.write('    ${random_index}=    Random Int    1    ${options_length - 1} \n')
          resources.write('    Select From List By Index    '+defFieldLocator+'    ${random_index} \n')
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

  #endregion

#endregion

#region Manual selection of the process folder
# 18 Friendly Shoulder
# process_folder_name = 'friendlyShoulder-exclusive-all-types-no-scalation-no-logging'
# process_folder_name = 'friendlyShoulder-exclusive-all-types-no-scalation-with-logging'
# process_folder_name = 'friendlyShoulder-exclusive-all-types-with-scalation-no-logging'
# process_folder_name = 'friendlyShoulder-exclusive-all-types-with-scalation-with-logging'
# process_folder_name = 'friendlyShoulder-inclusive-all-types-no-scalation-no-logging'
# process_folder_name = 'friendlyShoulder-inclusive-all-types-no-scalation-with-logging'
# process_folder_name = 'friendlyShoulder-inclusive-all-types-with-scalation-no-logging'
# process_folder_name = 'friendlyShoulder-inclusive-all-types-with-scalation-with-logging'
# process_folder_name = 'friendlyShoulder-only-complaint-no-scalation-no-logging'
# process_folder_name = 'friendlyShoulder-only-complaint-no-scalation-with-logging'
# process_folder_name = 'friendlyShoulder-only-complaint-with-scalation-no-logging'
# process_folder_name = 'friendlyShoulder-only-complaint-with-scalation-with-logging'
# process_folder_name = 'friendlyShoulder-only-suggestion-compliment-no-scalation-no-logging'
# process_folder_name = 'friendlyShoulder-only-suggestion-compliment-no-scalation-with-logging'
# process_folder_name = 'friendlyShoulder-parallel-all-types-no-scalation-no-logging'
# process_folder_name = 'friendlyShoulder-parallel-all-types-no-scalation-with-logging'
# process_folder_name = 'friendlyShoulder-parallel-all-types-with-scalation-no-logging'
# process_folder_name = 'friendlyShoulder-parallel-all-types-with-scalation-with-logging'
# 12 Travel Plan
# process_folder_name = 'travelPlan-AND'
# process_folder_name = 'travelPlan-EMSG'
# process_folder_name = 'travelPlan-ENTITIES'
process_folder_name = 'travelPlan-ENTITIES2'
# process_folder_name = 'travelPlan-ENTITIES3'
# process_folder_name = 'travelPlan-LOOP'
# process_folder_name = 'travelPlan-OR'
# process_folder_name = 'travelPlan-SIMPLE'
# process_folder_name = 'travelPlan-SRV'
# process_folder_name = 'travelPlan-TIMER'
# process_folder_name = 'travelPlan-VAL'
# process_folder_name = 'travelPlan-XOR'

current_directory = os.getcwd().replace('\\', '/')
process_folder_function(process_folder_name, current_directory)

#endregion


