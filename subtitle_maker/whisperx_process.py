import os
import subprocess
import sys
import re

from configuration import Config
from subtitles import Subtitle

_script_dir = os.path.dirname(os.path.abspath(__file__))
_whisperx_dir = os.path.join(_script_dir, '../whisperx')
_whisperx_location = os.path.join(_whisperx_dir, 'run_whisper.cmd')
_output_dir = os.path.join(_whisperx_dir, 'output')


def make_srt_from_file(video_file_path, config: Config):
    print(f'Creating {config.language_from} srt file for {video_file_path}')
    video_file_name = os.path.splitext(os.path.basename(video_file_path))[0]
    cmd_line = f'{_whisperx_location} --model {config.whisper_model} --language {config.language_from} "{video_file_path}"'
    process = subprocess.Popen(cmd_line, stdout=sys.stdout, stderr=sys.stderr)
    process.wait()
    srt_path = os.path.join(_output_dir, f'{video_file_name}.srt')
    if not os.path.isfile(srt_path):
        print(f'Failed to create srt file for {video_file_path}')
        exit(1)
    filter_whisperx_bs(srt_path)
    return srt_path


def filter_whisperx_bs(srt_path):
    print(f'Filtering WhisperX results for {srt_path}')
    srt = Subtitle(srt_path)
    for line in srt.lines:
        line.text = filter_bs(line.text)
    srt.save_srt_file(srt_path, False)


def filter_bs(string):
    result = string
    result = remove_sequences(result)
    result = remove_copyrights(result)
    if result != string:
        print(f'Filtered BS: {string} -> {result}')
    return result


def remove_copyrights(string):
    return string.replace('AUTHORWAVE', '')  # for some reason WhisperX adds this to the end of the text


def remove_sequences(string):
    while True:
        match = re.search(r'(.)\1\1\1\1', string)
        if not match:
            break
        string = string.replace(match.group(), match.group()[0])
    return string
