*** Settings ***
Documentation    Example Robot Framework Suite for U3 LabJack device read and write
Library          LabJackLibrary.LabJackU3
Suite Setup      Open U3 And Configure

*** Test Cases ***
Verify Digital Output 1
    ${output_value}=  Verify Digital Input    6  1
    Log               Digital Ouput 1 Value: "${output_value}"

Verify Digital Input 1
   Set Do             4  1

Verify Analog Output
   Set Dac            0  2.0

*** Keywords ***
Delay Toggle Led
    Toggle Led
    Sleep  2

Open U3 And Configure
    Documentation    Open only LabJack device found and set all I/O analog, then individually set digitals
    Open Device
    Config Io        fio_analog=0b11111111   # set all to analog before trying config digital
    Config Digital   4  6

Open U3 And Configure Alternate
    Documentation    Open only LabJack device found and set all I/O to correct state in one call
    Open Device
    Config Io        fio_analog=0b10101111   # set bit pattern to define 4 and 6 as digital, but less readable
