# Prompt Command to Execute a Specific Test Case: 
# robot -i TC_Random -v testCaseVar:TC06 customer_feedback_blind_test.robot
*** Settings ***
Library    FakerLibrary    #locale=pt_BR
Library    OperatingSystem
Library    Collections
Resource    customer_feedback_blind_resources.robot
Test Setup    kwFakerDataSetup

*** Variables ***
@{TaskNames}        TaskAnalyseComplaint    TaskReviewEscalation    TaskAcknowledge

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
  ${kw_executed}=  Create List
  kwFakerDataSetup
  kwLogin
  FOR    ${i}    IN RANGE    30
    ${inner_list}=  Create List
    kwFakerDataSetup
    kwRequestForm
    Append To List  ${inner_list}  Start of Execution #${i}
    Append to List  ${inner_list}  kwRequestForm
    WHILE    $processRunning == True
      kwFindFirstAvailableTask
      IF    $found_task == "TaskAnalyseComplaint"
        kwFakerDataSetup
        kwTaskAnalyseComplaint
        Append To List  ${inner_list}  kwTaskAnalyseComplaint
      ELSE IF    $found_task == "TaskReviewEscalation"
        kwFakerDataSetup
        kwTaskReviewEscalation
        Append To List  ${inner_list}  kwTaskReviewEscalation
      ELSE IF    $found_task == "TaskAcknowledge"
        kwFakerDataSetup
        kwTaskAcknowledge
        Append To List  ${inner_list}  kwTaskAcknowledge
      ELSE IF    $found_task == "No task available."
        ${processRunning}=    Set Variable    ${False}
        Set Test Variable    ${processRunning}
        BREAK
      END    
    END  
    Append To List  ${inner_list}  End of Execution #${i}
    Append To List    ${kw_executed}    ${inner_list}
  END
  ${json_string}=  Evaluate  json.dumps(${kw_executed}, indent=4)
  Create File  executedKeywords.json  ${json_string}

TC_Linear
    kwFakerDataSetup
    kwLogin
    kwRequestForm
    IF    '${faker-babblingCharacterization}' == 'complaint'
        kwMyTasks
        kwTaskAnalyseComplaint
        IF    ${faker-gravity} > 6
            kwMyTasks
            kwTaskReviewEscalation
        END
    ELSE IF    '${faker-babblingCharacterization}' in ['suggestion', 'compliment']
        kwMyTasks
        kwTaskAcknowledge
    END

TC_LinearBatch
    kwLogin
    FOR    ${i}    IN RANGE    10
        Sleep    200ms
        kwFakerDataSetup
        kwRequestForm
        IF    '${faker-babblingCharacterization}' == 'complaint'
            kwMyTasks
            kwTaskAnalyseComplaint
            IF    ${faker-gravity} > 6
                kwMyTasks
                kwTaskReviewEscalation
            END
        ELSE IF    '${faker-babblingCharacterization}' in ['suggestion', 'compliment']
            kwMyTasks
            kwTaskAcknowledge
        END
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
  ${faker-babblingCharacterization.type}  FakerLibrary.Word  ext_word_list=['suggestion','compliment','complaint']
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
