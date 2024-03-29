# Prompt Command to Execute a Specific Test Case: 
# robot -i TC_Random TravelPlanProcessMKR_test.robot
*** Settings ***
Library    FakerLibrary    #locale=pt_BR
Resource    TravelPlanProcessMKR_resources.robot
Test Setup    kwFakerDataSetup

*** Variables ***
@{TaskNames}    TaskCar  TaskFlight  TaskHotel

*** Test Cases ***
TC_Blind
    kwFakerDataSetup
    kwLogin
    kwEvent_1mlm38e
    WHILE    $processRunning == True
        kwFindFirstAvailableTask
        IF    $found_task == "TaskCar"
            kwFakerDataSetup
            kwTaskCar
        ELSE IF    $found_task == "TaskFlight"
            kwFakerDataSetup
            kwTaskFlight
        ELSE IF    $found_task == "TaskHotel"
            kwFakerDataSetup
            kwTaskHotel
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
        kwEvent_1mlm38e
        WHILE    $processRunning == True
            kwFindFirstAvailableTask
            IF    $found_task == "TaskCar"
                kwFakerDataSetup
                kwTaskCar
            ELSE IF    $found_task == "TaskFlight"
                kwFakerDataSetup
                kwTaskFlight
            ELSE IF    $found_task == "TaskHotel"
                kwFakerDataSetup
                kwTaskHotel
            ELSE IF    $found_task == "No task available."
                ${processRunning}=    Set Variable    ${False}
                Set Test Variable    ${processRunning}
                BREAK
            END
        END
    END

TC_Linear 
    [Documentation]  Arrange the following Keywords below according to the desired test path:
    kwFakerDataSetup
    kwLogin
    kwStartEvent_1
    kwEvent_1mlm38e
    kwTaskCar
    kwTaskFlight
    kwTaskHotel

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
    ${faker-endDate}    FakerLibrary.Date
    Set Test Variable    ${faker-endDate}
    ${faker-startDate}    FakerLibrary.Date
    Set Test Variable    ${faker-startDate}
    ${faker-carBookingNumber}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-carBookingNumber}
    ${faker-hotelName}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-hotelName}
    ${faker-hotelBookingNumber}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-hotelBookingNumber}
    ${faker-name}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-name}
    ${faker-carCompanyName}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-carCompanyName}
    ${faker-airlineTicketNumber}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-airlineTicketNumber}
    ${faker-airlineCompanyName}    FakerLibrary.Sentence  nb_words=8
    Set Test Variable    ${faker-airlineCompanyName}
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

kwStartEvent_1
    [Arguments]  
    [Documentation]  
    The user is in StartEvent_1
    The user fills StartEvent_1
