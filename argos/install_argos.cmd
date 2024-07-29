call "%~dp0activate_env"
python -m pip install --upgrade pip
pip install argostranslate
pip install --force-reinstall -v "numpy==1.26.4"
pip install --force-reinstall -v "torch==2.2.1" --index-url https://download.pytorch.org/whl/cu121