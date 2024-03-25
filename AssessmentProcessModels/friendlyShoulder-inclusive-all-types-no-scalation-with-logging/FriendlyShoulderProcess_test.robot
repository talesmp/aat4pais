# Prompt Command to Execute a Specific Test Case: 
# robot -i TC_Random FriendlyShoulderProcess_test.robot
*** Settings ***
Library    FakerLibrary    #locale=pt_BR 
Library    OperatingSystem 
Library    Collections 
Resource    FriendlyShoulderProcess_resources.robot
Test Setup    kwFakerDataSetup

*** Variables ***
@{TaskNames}    TaskAnalyseComplaint  TaskAcknowledge

*** Test Cases ***
TC_BlindBatch
    ${kw_executed}=    Create List
    kwFakerDataSetup
    kwLogin
    FOR    ${i}    IN RANGE    10
        ${inner_list}=    Create List
        kwFakerDataSetup
        kwRequestForm
        Append To List    ${inner_list}    Start of Execution #${i}
        Append to List    ${inner_list}    RequestForm
        WHILE    $processRunning == True
            kwFindFirstAvailableTask
            IF    $found_task == "TaskAnalyseComplaint"
                kwFakerDataSetup
                kwTaskAnalyseComplaint
                Append To List    ${inner_list}    TaskAnalyseComplaint
            ELSE IF    $found_task == "TaskAcknowledge"
                kwFakerDataSetup
                kwTaskAcknowledge
                Append To List    ${inner_list}    TaskAcknowledge
            ELSE IF    $found_task == "No task available."
                ${processRunning}=    Set Variable    ${False}
                Set Test Variable    ${processRunning}
                BREAK
            END
        END
        Append To List    ${inner_list}    End of Execution #${i} 
        Append To List    ${kw_executed}    ${inner_list} 
    END
    ${json_string}=    Evaluate    json.dumps(${kw_executed}, indent=4) 
    Create File    C:/Users/tales/LocalDocuments/Development/aat4pais/AssessmentProcessModels/friendlyShoulder-inclusive-all-types-no-scalation-with-logging/executedKeywords-friendlyShoulder-inclusive-all-types-no-scalation-with-logging.json    ${json_string} 
    ${data}=    Evaluate    json.loads(open("C:/Users/tales/LocalDocuments/Development/aat4pais/AssessmentProcessModels/friendlyShoulder-inclusive-all-types-no-scalation-with-logging/executedKeywords-friendlyShoulder-inclusive-all-types-no-scalation-with-logging.json").read()) 
    ${execution_paths}=    Evaluate    [' => '.join(execution[1:-1]) for execution in $data] 
    ${execution_counts}=    Evaluate    dict(collections.Counter($execution_paths))    modules=collections 
    ${output}=  Evaluate  "{} times\\n".format(len($data)) + '\\n'.join(["{} executions: {}".format(count, path) for path, count in $execution_counts.items()]) 
    Create File    C:/Users/tales/LocalDocuments/Development/aat4pais/AssessmentProcessModels/friendlyShoulder-inclusive-all-types-no-scalation-with-logging/executionsCounter-friendlyShoulder-inclusive-all-types-no-scalation-with-logging.txt    ${output} 

TC_Blind
    kwFakerDataSetup
    kwLogin
    kwRequestForm
    WHILE    $processRunning == True
        kwFindFirstAvailableTask
        IF    $found_task == "TaskAnalyseComplaint"
            kwFakerDataSetup
            kwTaskAnalyseComplaint
        ELSE IF    $found_task == "TaskAcknowledge"
            kwFakerDataSetup
            kwTaskAcknowledge
        ELSE IF    $found_task == "No task available."
            ${processRunning}=    Set Variable    ${False}
            Set Test Variable    ${processRunning}
            BREAK
        END
    END

TC_Linear 
    [Documentation]  Arrange the following Keywords below according to the desired test path:
    kwFakerDataSetup
    kwLogin
    kwRequestForm
    kwTaskAnalyseComplaint
    kwTaskAcknowledge

*** Keywords ***
kwFindFirstAvailableTask
    kwMyTasks
    ${found_task}=    Set Variable    No task available.
    ${exist_available_task}=    Run Keyword And Return Status    Get Text  xpath=/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[8]
    IF    $exist_available_task == True
        FOR    ${taskName}    IN ZIP    ${TaskNames}
            ${task_definition_key_from_text}=    Get Text  xpath=/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[8]
            IF    $task_definition_key_from_text == $taskName
                ${found_task}=    Set Variable    ${taskName}
                BREAK
            END
        END
        IF    $found_task == "No task available."
            ${processRunning}=    Set Variable    ${False}
            Set Test Variable    ${processRunning}
            ${found_task}=    Set Variable    ${task_definition_key_from_text}
            Set Test Variable    ${found_task}
            Fatal Error    Unexpected task found! 
        END
    END
    Set Test Variable    ${found_task}

kwFakerDataSetup
    ${faker-log}    FakerLibrary.Boolean
    Set Test Variable    ${faker-log}
    ${faker-gravity}    FakerLibrary.Random Int  min=1  max=10
    Set Test Variable    ${faker-gravity}
    ${faker-date}    FakerLibrary.Date
    Set Test Variable    ${faker-date}
    ${faker-response}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-response}
    ${faker-description}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-description}
    ${processRunning}=    Set Variable    ${True}
    Set Test Variable    ${processRunning}

kwLogin
    [Arguments]  
    [Documentation]  
    The user logs in

kwMyTasks
    [Arguments]  
    [Documentation]  
    The user is in MyTasks

kwRequestForm
    [Arguments]  
    [Documentation]  
    The user is in RequestForm
    The user fills RequestForm
    The user submits RequestForm

kwTaskAnalyseComplaint
    [Arguments]  
    [Documentation]  
    The user is in TaskAnalyseComplaint
    The user fills TaskAnalyseComplaint
    The user submits TaskAnalyseComplaint

kwTaskAcknowledge
    [Arguments]  
    [Documentation]  
    The user is in TaskAcknowledge
    The user fills TaskAcknowledge
    The user submits TaskAcknowledge

