@ECHO OFF
SETLOCAL
TITLE USUSLS Simulator Environment Setup

REM setup python environment related variables
SET    ENV_NAME=trial_env
SET    SIM_ROOT=%cd%\..\

REM add virtualenv package if not already added
ECHO Adding virtualenv package...

pip install virtualenv && (
   ECHO.
   ECHO virtualenv installed correctly
   ECHO.
) || (
   ECHO.
   ECHO virtualenv installation failed. Ensure you have pip installed
   ECHO.
)

REM setup python environment related variables
SET    ENV_NAME=trial_env
SET    SIM_ROOT=%cd%\..\

IF EXIST %ENV_NAME% (
ECHO virtual environment found!
) ELSE (
ECHO virtual environment not found
ECHO creating new virtualenv with name %ENV_NAME%

python -m venv %ENV_NAME%
)

ECHO activating virtualenv...
%ENV_NAME%\Scripts\activate

