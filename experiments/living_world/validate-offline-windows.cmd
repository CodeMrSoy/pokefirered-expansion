@echo off
setlocal
set "report=%TEMP%\LivingQuantumWorld-validation-%RANDOM%-%RANDOM%.log"
echo Running offline validation. The model check may take a minute.
call :validate > "%report%" 2>&1
set "result=%errorlevel%"
echo(
if exist "%report%" (
    type "%report%"
    echo(
    echo Report saved to "%report%"
) else (
    echo Could not write the validation report to "%report%".
)
echo Validation exit code: %result%
echo(
pause
exit /b %result%

:validate
pushd "%~dp0"
if errorlevel 1 exit /b 1
echo === Sandbox check ===
python\python.exe -B play.py --sandbox-test
set "status=%errorlevel%"
echo Sandbox check exit code: %status%
if not "%status%"=="0" (
    echo Model check skipped because the sandbox check failed.
    popd
    exit /b %status%
)
echo(
echo === Local model check ===
python\python.exe -B play.py --model-test
set "status=%errorlevel%"
echo Local model check exit code: %status%
popd
exit /b %status%
