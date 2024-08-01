call "%~dp0activate_env"
set PYTHONPATH=%~dp0
set PATH=%~dp0..\ffmpeg;%PATH%
whisperx --highlight_words True --model large-v2 --output_format srt --output_dir "%~dp0output" %*