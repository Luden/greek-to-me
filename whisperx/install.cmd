call "%~dp0activate_env"
python -m pip install --upgrade pip
pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu121
pip install git+https://github.com/m-bain/whisperx.git