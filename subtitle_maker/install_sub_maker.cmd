call "%~dp0activate_env"
python -m pip install --upgrade pip
pip install openai
python "%~dp0configuration.py"
start "" "%~dp0config.json"