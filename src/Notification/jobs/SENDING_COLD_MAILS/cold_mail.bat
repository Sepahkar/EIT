@echo off
setlocal

:: Set paths
set VENV_PATH=D:\DJANGO313\Notification\venv
set PROJECT_PATH=D:\DJANGO313\Notification
set LOG_FILE=D:\LOGS\Notification\jobs\SENDING_COLD_MAILS\logs\logs.txt

:: Activate the virtual environment
call "%VENV_PATH%\Scripts\activate.bat"

:: Change to project directory
cd /d "%PROJECT_PATH%"

:: Run Django management command and log output
echo [%DATE% %TIME%] Running command >> "%LOG_FILE%"
python manage.py retry_cold_emails >> "%LOG_FILE%" 2>&1

:: Deactivate virtual environment
deactivate

:: End script
endlocal
