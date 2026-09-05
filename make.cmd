@echo off
setlocal
set "COURSE_PY="
set "COURSE_PY_ARGS="
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" set "COURSE_PY=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if not defined COURSE_PY where py >nul 2>nul && set "COURSE_PY=py" && set "COURSE_PY_ARGS=-3"
if not defined COURSE_PY where python >nul 2>nul && set "COURSE_PY=python"
if not defined COURSE_PY (
  echo Python 3 was not found.
  exit /b 1
)
if "%~1"=="check-links" goto check_links
if "%~1"=="hours" goto hours
if "%~1"=="status" goto status
if "%~1"=="lab-05" goto lab_05
echo Usage: make.cmd ^<check-links^|hours^|status^|lab-05^>
exit /b 2

:check_links
"%COURSE_PY%" %COURSE_PY_ARGS% scripts\check_links.py
exit /b %errorlevel%

:hours
"%COURSE_PY%" %COURSE_PY_ARGS% scripts\hours.py
exit /b %errorlevel%

:status
"%COURSE_PY%" %COURSE_PY_ARGS% scripts\status.py
exit /b %errorlevel%

:lab_05
docker compose -f labs\05-openfga-crossorg\docker-compose.yml up -d
exit /b %errorlevel%
