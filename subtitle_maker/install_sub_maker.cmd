call "%~dp0activate_env"
python -m pip install --upgrade pip
pip install openai
python configuration.py
start "" "config.json"