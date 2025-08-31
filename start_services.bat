@echo off
echo Starting NIFTY Prediction Services...
echo.

echo Starting Backend (Flask API)...
start "Backend" cmd /k "cd niftypred && python.exe app/app.py"

echo Waiting for backend to start...
timeout /t 10 /nobreak > nul

echo Starting Frontend (React App)...
start "Frontend" cmd /k "cd nifty-prediction-app && npm start"

echo.
echo Services are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to open the application in your browser...
pause > nul

start http://localhost:3000

echo.
echo Services are running! Press any key to exit this window...
pause > nul
