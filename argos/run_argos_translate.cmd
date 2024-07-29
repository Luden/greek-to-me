call "%~dp0activate_env"
set PYTHONPATH=%~dp0
python argos_translate.py %*
pause