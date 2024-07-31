import os
import subprocess
import sys

from configuration import Config
from subtitles import Subtitle

_script_dir = os.path.dirname(os.path.abspath(__file__))
_argos_dir = os.path.join(_script_dir, '../argos')
_argos_location = os.path.join(_argos_dir, 'run_argos_translate.cmd')
_output_dir = os.path.join(_script_dir, 'output')


def translate_srt(srt: Subtitle, config: Config):
    distinct_lines = srt.get_distinct_lines_without_tags()
    translated_distinct_lines = translate_lines(distinct_lines, config)
    for subtitle_line in srt.lines:
        line_index = distinct_lines.index(subtitle_line.text_without_tags)
        subtitle_line.translated_text_without_tags = translated_distinct_lines[line_index]


def translate_lines(distinct_lines, config: Config):
    print(f'Argos translating srt from {config.language_from} to {config.language_to}')
    if not os.path.exists(_output_dir):
        os.makedirs(_output_dir)
    from_file_path = os.path.join(_output_dir, 'subtitle_original_lines.txt')
    with open(from_file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(distinct_lines))
    to_file_path = os.path.join(_output_dir, 'subtitle_translated_lines.txt')
    cmd_line = f'{_argos_location} {config.language_from} {config.language_to} "{from_file_path}" "{to_file_path}"'
    process = subprocess.Popen(cmd_line, stdout=sys.stdout, stderr=sys.stderr)
    process.wait()
    if not os.path.isfile(to_file_path):
        print(f'Failed to create srt file for {from_file_path}')
        exit(1)
    with open(to_file_path, 'r', encoding='utf-8') as file:
        translated_lines = file.readlines()
    print(f'Argos finished translating')
    return translated_lines

