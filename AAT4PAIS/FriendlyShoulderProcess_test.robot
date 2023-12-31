# Prompt Command to Execute a Specific Test Case: 
# robot -i TC_Random FriendlyShoulderProcess_test.robot
*** Settings ***
Library    FakerLibrary    #locale=pt_BR
Resource    FriendlyShoulderProcess_resources.robot
Test Setup    kwFakerDataSetup

*** Variables ***
@{TaskNames}    TaskAnalyseComplaint  TaskReviewEscalation  TaskAcknowledge

*** Test Cases ***
TC_Blind
    kwFakerDataSetup
    kwLogin
    kwRequestForm
    WHILE    $processRunning == True
        kwFindFirstAvailableTask
        IF    $found_task == "TaskAnalyseComplaint"
            kwFakerDataSetup
            kwTaskAnalyseComplaint
        ELSE IF    $found_task == "TaskReviewEscalation"
            kwFakerDataSetup
            kwTaskReviewEscalation
        ELSE IF    $found_task == "TaskAcknowledge"
            kwFakerDataSetup
            kwTaskAcknowledge
        ELSE IF    $found_task == "No task available."
            ${processRunning}=    Set Variable    ${False}
            Set Test Variable    ${processRunning}
            BREAK
        END
    END

TC_BlindBatch
    kwFakerDataSetup
    kwLogin
    FOR    ${i}    IN RANGE    10
        kwFakerDataSetup
        kwRequestForm
        WHILE    $processRunning == True
            kwFindFirstAvailableTask
            IF    $found_task == "TaskAnalyseComplaint"
                kwFakerDataSetup
                kwTaskAnalyseComplaint
            ELSE IF    $found_task == "TaskReviewEscalation"
                kwFakerDataSetup
                kwTaskReviewEscalation
            ELSE IF    $found_task == "TaskAcknowledge"
                kwFakerDataSetup
                kwTaskAcknowledge
            ELSE IF    $found_task == "No task available."
                ${processRunning}=    Set Variable    ${False}
                Set Test Variable    ${processRunning}
                BREAK
            END
        END
    END

TC_Linear 
    [Documentation]  Condition Expressions: 
...                  ${processInstance.friendlyShoulder.babblingCharacterization.type== 'complaint'}
...                  ${processInstance.friendlyShoulder.babblingCharacterization.type== 'suggestion' || processInstance.friendlyShoulder.babblingCharacterization.type== 'compliment'}
...                  ${processInstance.friendlyShoulder.gravity <= 6}
...                  ${processInstance.friendlyShoulder.gravity > 6}
...                  ${processInstance.friendlyShoulder.log == false}
...                  ${processInstance.friendlyShoulder.log == true}
...  ===> arrange the following Keywords below according to the Conditions above:
    kwFakerDataSetup
    kwLogin
    kwRequestForm
    kwTaskAnalyseComplaint
    kwTaskReviewEscalation
    kwTaskAcknowledge

TC_LinearBatch 
    [Documentation]  Execute TC_Linear for i=10 consecutive times
    FOR    ${i}    IN RANGE    10
        Sleep    200ms
        kwFakerDataSetup
        # =====> Insert here the arranged Keywords according to TC_Linear above <====
        Close Browser
    END

*** Keywords ***
kwFindFirstAvailableTask
    Sleep    200ms
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
    END
    Set Test Variable    ${found_task}

kwFakerDataSetup
    ${faker-log}    FakerLibrary.Boolean
    Set Test Variable    ${faker-log}
    ${faker-gravity}    FakerLibrary.Random Int  min=1  max=10
    Set Test Variable    ${faker-gravity}
    ${faker-date}    FakerLibrary.Date
    Set Test Variable    ${faker-date}
    ${faker-description}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-description}
    ${faker-response}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-response}
    # double-check the following collection in 'ext_word_list' =====>                     <===== 
    ${faker-babblingCharacterization.type}    FakerLibrary.Word  ext_word_list=['complaint', 'compliment', 'suggestion']
    Set Test Variable    ${faker-babblingCharacterization.type}
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

kwTaskReviewEscalation
    [Arguments]  
    [Documentation]  
    The user is in TaskReviewEscalation
    The user fills TaskReviewEscalation
    The user submits TaskReviewEscalation

kwTaskAcknowledge
    [Arguments]  
    [Documentation]  
    The user is in TaskAcknowledge
    The user fills TaskAcknowledge
    The user submits TaskAcknowledge

