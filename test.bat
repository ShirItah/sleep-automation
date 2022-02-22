@echo off
REM change to install directory
CD /d C:\Program Files (x86)\Itamar Medical\WP_Interface
@REM REM Commands example
SET source=%1
SET dest=%2
SET action=%3
@REM ECHO source: %source%, destination: %dest%, action: %action%

ECHO "" | zzzPATAnalyzeReport -s %source% -d %dest% -a %action% -p

ECHO:

IF /I %errorlevel% GEQ  1 (
    ECHO execution failed, error leve: %errorlevel%
)
IF /I %errorlevel% EQU  0 (
    ECHO DONE
)