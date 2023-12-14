*** Settings ***
Library    RPA.Browser.Selenium
Library    FakerLibrary    #locale=pt_BR
Library    String
Library    RPA.Desktop

*** Variables ***
${locator-customer-feedback-start-form-babblingCharacterization.type}    customer-feedback-start-form-babblingCharacterization
${locator-customer-feedback-start-form-date}    customer-feedback-start-form-date
${locator-customer-feedback-start-form-description}    customer-feedback-start-form-description                 
${locator-task-acknowledge-log}    task-acknowledge-log
${locator-task-acknowledge-response}    task-acknowledge-response
${locator-task-analyse-complaint-gravity}    task-analyse-complaint-gravity
${locator-task-analyse-complaint-log}    task-analyse-complaint-log
${locator-task-analyse-complaint-response}    task-analyse-complaint-response
${locator-task-review-escalation-log}    task-review-escalation-log
${locator-task-review-escalation-response}    task-review-escalation-response   


*** Keywords ***
The user logs in
    [Arguments]  
    [Documentation] 
    Open Available Browser    maximized=true
    Go To    http://localhost:8080/
    Click Element When Visible       account-menu__BV_toggle_
    Click Element When Visible       login
    Wait Until Element Is Visible    login-page___BV_modal_header_
    Input Text When Element Is Visible    username    admin
    Input Text When Element Is Visible    password    admin
    Click Element When Visible    //span[contains(.,'Remember me')]
    Click Button When Visible    //button[@data-cy='submit'][contains(.,'Sign in')] 
    Sleep    500ms

The user is in MyTasks
    Sleep    100ms
    Go To    http://localhost:8080/my-candidate-tasks
    Wait Until Element Is Visible    task-instance-heading

The user is in RequestForm
  Sleep    500ms
  Go To    http://localhost:8080/process-definition/CustomerFeedbackProcess/init

The user fills RequestForm 
  Wait Until Page Contains    Customer Feedback
  Input Text When Element Is Visible    ${locator-customer-feedback-start-form-description}    ${faker-description}
  Input Text When Element Is Visible    ${locator-customer-feedback-start-form-date}    ${faker-date} 
  Click Element When Visible    ${locator-customer-feedback-start-form-babblingCharacterization.type}
  IF    '${faker-babblingCharacterization.type}' == 'complaint'
    Click Element When Visible    //option[@value='[object Object]'][contains(.,'complaint')]
  ELSE IF    '${faker-babblingCharacterization.type}' == 'suggestion'
    Click Element When Visible    //option[@value='[object Object]'][contains(.,'suggestion')]
  ELSE IF    '${faker-babblingCharacterization.type}' == 'compliment'
    Click Element When Visible    //option[@value='[object Object]'][contains(.,'compliment')]
  END

The user submits RequestForm
    Capture Page Screenshot
    Sleep    500ms
    Click Button    save-entity

The user is in TaskAnalyseComplaint
    Sleep    500ms
    Click Element If Visible    xpath:/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[12]/div[1]/button[1]
    Wait Until Page Contains    TaskAnalyseComplaint

The user fills TaskAnalyseComplaint
    [Arguments]  
    Wait Until Page Contains    TaskAnalyseComplaint
    Input Text When Element Is Visible    task-analyse-complaint-gravity    ${faker-gravity}                                          #<<< melhorar a forma de pegar essas opções
    IF    ${faker-log} is True
        Wait Until Element Is Visible    task-analyse-complaint-log
        Select Checkbox    task-analyse-complaint-log
    ELSE IF    ${faker-log} is False
        Wait Until Element Is Visible    task-analyse-complaint-log
        Unselect Checkbox    task-analyse-complaint-log
    END
    Input Text When Element Is Visible        task-analyse-complaint-response    ${faker-response}
    
The user submits TaskAnalyseComplaint
    Capture Page Screenshot
    Sleep    500ms
    Click Button    //button[@type='submit'][contains(.,'Complete')]

The user is in TaskReviewEscalation
    Sleep    500ms
    Click Element If Visible    xpath:/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[12]/div[1]/button[1]
    Wait Until Page Contains    TaskReviewEscalation

The user fills TaskReviewEscalation
    [Arguments]  
    Wait Until Page Contains    TaskReviewEscalation
    IF    ${faker-log} is True
        Wait Until Element Is Visible    task-review-escalation-log
        Select Checkbox    task-review-escalation-log
    ELSE IF    ${faker-log} is False
        Wait Until Element Is Visible    task-review-escalation-log
        Unselect Checkbox    task-review-escalation-log
    END
    Input Text When Element Is Visible    task-review-escalation-response    ${faker-response}

The user submits TaskReviewEscalation
    Capture Page Screenshot
    Sleep    500ms
    Click Button    //button[@type='submit'][contains(.,'Complete')]

The user is in TaskAcknowledge
    Sleep    500ms
    Click Element If Visible    xpath:/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[12]/div[1]/button[1]
    Wait Until Page Contains    TaskAcknowledge

The user fills TaskAcknowledge
    [Arguments]  
    Wait Until Page Contains    TaskAcknowledge
    IF    ${faker-log} is True
        Wait Until Element Is Visible    task-acknowledge-log
        Select Checkbox    task-acknowledge-log
    ELSE IF    ${faker-log} is False
        Wait Until Element Is Visible    task-acknowledge-log
        Unselect Checkbox    task-acknowledge-log
    END
    Input Text When Element Is Visible    task-acknowledge-response    ${faker-response}
    
The user submits TaskAcknowledge
    Capture Page Screenshot
    Sleep    500ms
    Click Button    //button[@type='submit'][contains(.,'Complete')]
