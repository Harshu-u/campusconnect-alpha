@echo off
REM run_https_dev.bat — Generate mkcert certs (if mkcert installed) and run manage.py runserver_plus
REM Requires: mkcert, django-extensions, pyOpenSSL (installed in venv)

REM Ensure script runs from project root (where manage.py lives)
cd /d %~dp0

REM Activate virtualenv (adjust if your venv path differs)
echo Activating virtualenv...
if exist "%~dp0venv\Scripts\activate.bat" (
	call "%~dp0venv\Scripts\activate.bat"
) else (
	echo WARNING: virtualenv activate script not found at venv\Scripts\activate.bat
	echo Please activate your venv manually before running this script.
)

REM Check for mkcert
where mkcert >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo mkcert was not found on your PATH.
	echo Install mkcert: https://mkcert.dev/ (or use Chocolatey: choco install mkcert)
	pause
	exit /b 1
)

echo Generating certificate and key files (devcert.pem / devkey.pem)...
mkcert -key-file devkey.pem -cert-file devcert.pem 127.0.0.1 localhost ::1
if %ERRORLEVEL% NEQ 0 (
	echo mkcert failed. Check output above.
	pause
	exit /b 1
)

echo Combining key+cert into devcombined.pem (required by runserver_plus)...
REM Combine key then cert into single PEM file
type devkey.pem devcert.pem > devcombined.pem
if %ERRORLEVEL% NEQ 0 (
	echo Failed to create devcombined.pem
	pause
	exit /b 1
)

echo Starting Django runserver_plus on https://127.0.0.1:8000 ...
python manage.py runserver_plus 127.0.0.1:8000 --cert-file devcombined.pem

echo Server stopped. You can remove devcert.pem/devkey.pem/devcombined.pem if desired.
pause
