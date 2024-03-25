*** Settings ***
Library    FakerLibrary    #locale=pt_BR
Library    RPA.Browser.Selenium
Library    String
Library    RPA.Desktop

*** Variables ***
${url_home}    http://localhost:8080/
${url_my_tasks}    ${url_home}my-candidate-tasks
${locator-task-book-a-hotel-hotelBookingNumber}    task-book-a-hotel-hotelBookingNumber
${locator-task-book-a-hotel-hotelName}    task-book-a-hotel-hotelName
${locator-task-buy-flight-tickets-airlineCompanyName}    task-buy-flight-tickets-airlineCompanyName
${locator-task-buy-flight-tickets-airlineTicketNumber}    task-buy-flight-tickets-airlineTicketNumber
${locator-task-rent-a-car-carBookingNumber}    task-rent-a-car-carBookingNumber
${locator-task-rent-a-car-carCompanyName}    task-rent-a-car-carCompanyName
${locator-travel-plan-start-form-endDate}    travel-plan-start-form-endDate
${locator-travel-plan-start-form-name}    travel-plan-start-form-name
${locator-travel-plan-start-form-startDate}    travel-plan-start-form-startDate

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

The user is in StartEvent_1
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Go To    http://localhost:8080/process-definition/TravelPlanProcessAND/init 

The user fills StartEvent_1
    [Arguments]  
    [Documentation]  
    Wait Until Page Contains    Create or edit a 
    Input Text When Element Is Visible    travel-plan-start-form-name    ${faker-name} 
    Input Text When Element Is Visible    travel-plan-start-form-startDate    ${faker-startDate} 
    Input Text When Element Is Visible    travel-plan-start-form-endDate    ${faker-endDate} 

The user submits StartEvent_1
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Capture Page Screenshot  
    Click Button    save-entity 

The user is in TaskCar
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Click Element If Visible    xpath:/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[12]/div[1]/button[1]  
    Wait Until Page Contains    TaskCar

The user fills TaskCar
    [Arguments]  
    [Documentation]  
    Wait Until Page Contains    TaskCar 
    Input Text When Element Is Visible    task-rent-a-car-carCompanyName    ${faker-carCompanyName} 
    Input Text When Element Is Visible    task-rent-a-car-carBookingNumber    ${faker-carBookingNumber} 

The user submits TaskCar
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Capture Page Screenshot  
    Click Button    //button[@type='submit'][contains(.,'Complete')] 

The user is in TaskFlight
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Click Element If Visible    xpath:/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[12]/div[1]/button[1]  
    Wait Until Page Contains    TaskFlight

The user fills TaskFlight
    [Arguments]  
    [Documentation]  
    Wait Until Page Contains    TaskFlight 
    Input Text When Element Is Visible    task-buy-flight-tickets-airlineCompanyName    ${faker-airlineCompanyName} 
    Input Text When Element Is Visible    task-buy-flight-tickets-airlineTicketNumber    ${faker-airlineTicketNumber} 

The user submits TaskFlight
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Capture Page Screenshot  
    Click Button    //button[@type='submit'][contains(.,'Complete')] 

The user is in TaskHotel
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Click Element If Visible    xpath:/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[12]/div[1]/button[1]  
    Wait Until Page Contains    TaskHotel

The user fills TaskHotel
    [Arguments]  
    [Documentation]  
    Wait Until Page Contains    TaskHotel 
    Input Text When Element Is Visible    task-book-a-hotel-hotelName    ${faker-hotelName} 
    Input Text When Element Is Visible    task-book-a-hotel-hotelBookingNumber    ${faker-hotelBookingNumber} 

The user submits TaskHotel
    [Arguments]  
    [Documentation]  
    Sleep    500ms  
    Capture Page Screenshot  
    Click Button    //button[@type='submit'][contains(.,'Complete')] 

