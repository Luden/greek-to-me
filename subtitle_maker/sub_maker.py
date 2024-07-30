import os
import os.path
import sys
import tkinter as tk
import gpt_translate_srt
import argos_process
from tkinter import filedialog

from configuration import load_or_create_config, Config
from subtitles import Subtitle
from whisperx_process import make_srt_from_file


def make_subtitles(video_file, config: Config):
    srt_file = make_srt_from_file(video_file, config)
    srt = Subtitle(srt_file)
    if config.translate_with_gpt:
        gpt_translate_srt.translate_srt(srt, config)
    if config.translate_with_argos:
        argos_process.translate_srt(srt, config)
    if config.move_tags:
        gpt_translate_srt.move_tags(srt, config)
    srt.format_augmented_text()
    output_file = make_unique_srt_file_name(video_file)
    srt.save_srt_file(output_file, True)


def make_unique_srt_file_name(video_file):
    video_dir = os.path.dirname(video_file)
    video_name_without_extension = os.path.splitext(os.path.basename(video_file))[0]
    srt_name = os.path.join(video_dir, f'{video_name_without_extension}.srt')
    index = 1
    while os.path.isfile(srt_name):
        srt_name = os.path.join(video_dir, f'{video_name_without_extension}_{index}.srt')
        index += 1
    return srt_name


def main():
    config = load_or_create_config()
    video_file = ''
    if len(sys.argv) == 1:
        root = tk.Tk()
        root.withdraw()
        video_file = filedialog.askopenfilename()
    if len(sys.argv) == 2:
        video_file = sys.argv[1]
    if not video_file:
        print('No video file provided')
        exit(1)
    if not os.path.isfile(video_file):
        print(f'File not found: {video_file}')
        exit(1)
    make_subtitles(video_file, config)


if __name__ == '__main__':
    main()
