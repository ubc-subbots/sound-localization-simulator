@ECHO OFF
SETLOCAL
TITLE USUSLS Simulator Environment Setup

REM find current location and python location
SET    SIM_DIR=%cd%
WHERE python > temp.txt
SET /p PYTHON_LOCATION= < temp.txt
DEL temp.txt

call :folder_path_from_file_path PYTHON_DIR %PYTHON_LOCATION%

ECHO =================================================
ECHO Adding Simulator Modules to Python Interpreter
ECHO =================================================
ECHO.

ECHO Current directory %SIM_DIR%
ECHO Python located at %PYTHON_DIR%
ECHO.

ECHO Going into %PYTHON_DIR%Lib\site-packages...
cd %PYTHON_DIR%Lib\site-packages

ECHO Creating path reference file for Python interpreter...
ECHO %SIM_DIR%\src > sounds_localization_simulator.pth
ECHO.

ECHO Running Import Test...
ECHO.
cd %SIM_DIR%\test
call import_test.py && (
   ECHO.
   ECHO Simulator module imports working correctly
   ECHO.
) || (
   ECHO.
   ECHO Simulator moduel imports not working RIP...
   ECHO.
)

ECHO =================================================
ECHO.

ECHO Simulator environment setup complete! :)

PAUSE
ENDLOCAL
EXIT

:folder_path_from_file_path <resultVar> <pathVar>
(
    set "%~1=%~dp2"
    exit /b
)