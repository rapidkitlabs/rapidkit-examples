@echo off
setlocal

set "SCRIPT_DIR=%~dp0"

if exist "%SCRIPT_DIR%\.venv\Scripts\rapidkit.exe" (
  "%SCRIPT_DIR%\.venv\Scripts\rapidkit.exe" %*
  exit /b %ERRORLEVEL%
)

:rapidkit_npm_wrapper_fallback
for /f "delims=" %%R in ('where rapidkit.cmd 2^>nul') do (
  if /I not "%%~fR"=="%SCRIPT_DIR%rapidkit.cmd" if /I not "%%~fR"=="%SCRIPT_DIR%.workspai\rapidkit.cmd" if /I not "%%~fR"=="%SCRIPT_DIR%.rapidkit\rapidkit.cmd" (
    set "RAPIDKIT_LOCAL_LAUNCHER_BYPASS=1"
    "%%~fR" %*
    exit /b %ERRORLEVEL%
  )
)

:rapidkit_core_fallback
for %%R in ("%USERPROFILE%\.local\bin\rapidkit.exe" "%APPDATA%\Python\Scripts\rapidkit.exe" "%LOCALAPPDATA%\Programs\Python\Scripts\rapidkit.exe") do (
  if exist "%%~R" (
    "%%~R" %*
    exit /b %ERRORLEVEL%
  )
)

echo RapidKit launcher could not find a local Python CLI. 1>&2
echo - Python engine installation was intentionally skipped for this workspace. 1>&2
echo - For npm-owned workspace commands, run: npx workspai ^<command^> 1>&2
echo - To install the local Python engine later, create a RapidKit Core module-enabled project, then run: npx workspai workspace run init 1>&2
echo Tip: for npm-owned workspace commands, run npx --yes --package workspai workspai %* from a shell where npm is on PATH. 1>&2
exit /b 1
