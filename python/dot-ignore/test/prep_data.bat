@ECHO OFF
IF exist test_dir  (RMDIR _test_dir /Q /S)
ROBOCOPY test_dir_save _test_dir /E

ECHO exit code: %errorlevel%
if errorlevel 8 exit /B 1

exit /B 0