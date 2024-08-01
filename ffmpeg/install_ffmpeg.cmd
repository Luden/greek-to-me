call "%~dp0activate_env"
python -m pip install --upgrade pip
pip install requests
python "%~dp0install_ffmpeg.py"