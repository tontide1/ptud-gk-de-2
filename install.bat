@echo off
echo Installing Task Management System...
echo.

REM Create and activate conda environment
call conda create -n gk_ptud python=3.10.11 -y
call conda activate gk_ptud

REM Install requirements
pip install -r requirements.txt

REM Run the application
start cmd /k python app.py

REM Wait for the database to initialize (10 seconds)
timeout /t 10 /nobreak

REM Create admin account
python create_admin.py

echo.
echo Installation completed!
echo You can access the application at: http://localhost:5000
echo Default admin credentials: admin / admin123
echo.
pause