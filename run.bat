@echo off
set PORT=5000
set HOSTNAME_BASE=Ranjani-Vathsan-Shradah

:: Get local IP address dynamically
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4 Address"') do (
    set IP=%%a
    goto :found_ip
)
:found_ip
set IP=%IP: =%

echo ========================================================
echo   Dasa Bhukti Calculator Launcher
echo   Sri Ramajayam. Sri mathe ramanujaya namaha:
echo ========================================================
echo.
echo Current Network Links (Try in order):
echo 1. Local: http://127.0.0.1:%PORT%
echo 2. mDNS:  http://%HOSTNAME_BASE%.local:%PORT%/desabhuthi
echo 3. IP:    http://%IP%:%PORT%/desabhuthi (Most Reliable)
echo.
echo NOTE: If mobile access fails:
echo - Ensure mobile and PC are on the same Wi-Fi.
echo - Run this command as ADMIN: 
echo   netsh advfirewall firewall add rule name="Flask_LAN_Access" dir=in action=allow protocol=TCP localport=5000
echo.
echo MENU:
echo 1. Start Server Normally
echo 2. Start Server in Background
echo 3. Stop Background Server
echo.
set /p choice="Enter choice (1, 2, or 3): "

if "%choice%"=="1" (
    echo Opening browser...
    start http://127.0.0.1:%PORT%/desabhuthi_calculator.html
    echo Starting Server...
    python app.py
) else if "%choice%"=="2" (
    echo Starting Server in Background...
    wscript.exe run_hidden.vbs
    echo Server is running.
    echo Opening browser...
    start http://%IP%:%PORT%/desabhuthi_calculator.html
    pause
) else if "%choice%"=="3" (
    call stop_server.bat
) else (
    echo Invalid choice.
    pause
)
