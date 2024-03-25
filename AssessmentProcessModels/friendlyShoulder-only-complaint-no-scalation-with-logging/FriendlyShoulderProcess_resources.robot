*** Settings ***
Library    FakerLibrary    #locale=pt_BR
Library    RPA.Browser.Selenium
Library    String
Library    RPA.Desktop

*** Variables ***
${url_home}    http://localhost:8080/
${url_my_tasks}    ${url_home}my-candidate-tasks
${locator-friendly-shoulder-start-form-babblingCharacterization.type}    friendly-shoulder-start-form-babblingCharacterization
${locator-friendly-shoulder-start-form-date}    friendly-shoulder-start-form-date
${locator-friendly-shoulder-start-form-description}    friendly-shoulder-start-form-description
${locator-task-analyse-complaint-gravity}    task-analyse-complaint-gravity
${locator-task-analyse-complaint-log}    task-analyse-complaint-log
${locator-task-analyse-complaint-response}    task-analyse-complaint-response

*** Keywords ***
The user logs in
    [Arguments]  
    [Documentation]  
    Open Available Browser    maximized=true
    Go To    ${url_home}
    Click Element When Visible       account-menu__BV_toggle_
    Click Element When Visible       login
    Wait Until Element Is Visible    login-page___BV_modal_header_
    Input Text When Element Is Visible    username    admin
    Input Text When Element Is Visible    password    admin
    Click Element When Visible    //span[contains(.,'Remember me')]
    Click Button When Visible    //button[@data-cy='submit'][contains(.,'Sign in')]
    Sleep    500ms

The user is in MyTasks
    [Arguments]  
    [Documentation]  
    Sleep    500ms
    Go To    ${url_my_tasks}
    Wait Until Element Is Visible    task-instance-heading

The user is in RequestForm
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Go To    http://localhost:8080/process-definition/FriendlyShoulderProcess/init 

The user fills RequestForm
    [Arguments]  
    [Documentation]  
    Wait Until Page Contains    Create or edit a 
    Input Text When Element Is Visible    friendly-shoulder-start-form-description    ${faker-description} 
    Input Text When Element Is Visible    friendly-shoulder-start-form-date    ${faker-date} 
    Click Element When Visible    friendly-shoulder-start-form-babblingCharacterization 
    ${list_options}=    Get WebElements    //select[@id='friendly-shoulder-start-form-babblingCharacterization']/option 
    ${options_length}=    Get Length    ${list_options} 
    ${random_index}=    Random Int    1    ${options_length - 1} 
    Select From List By Index    friendly-shoulder-start-form-babblingCharacterization    ${random_index} 

The user submits RequestForm
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Capture Page Screenshot  
    Click Button    save-entity 

The user is in TaskAnalyseComplaint
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Click Element If Visible    xpath:/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[12]/div[1]/button[1]  
    Wait Until Page Contains    TaskAnalyseComplaint

The user fills TaskAnalyseComplaint
    [Arguments]  
    [Documentation]  
    Wait Until Page Contains    TaskAnalyseComplaint 
    Input Text When Element Is Visible    task-analyse-complaint-gravity    ${faker-gravity} 
    IF    ${faker-log} is True 
        Wait Until Element Is Visible    task-analyse-complaint-log 
        Select Checkbox    task-analyse-complaint-log 
    ELSE IF    ${faker-log} is False 
        Wait Until Element Is Visible    task-analyse-complaint-log 
        Unselect Checkbox    task-analyse-complaint-log 
    END 
    Input Text When Element Is Visible    task-analyse-complaint-response    ${faker-response} 

The user submits TaskAnalyseComplaint
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Capture Page Screenshot  
    Click Button    //button[@type='submit'][contains(.,'Complete')] 

