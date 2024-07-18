import os
import os.path
import sys
import tkinter as tk
from tkinter import filedialog

from configuration import load_or_create_config, Config
from translate_srt import translate_srt_in_place
from whisperx_process import make_srt_from_file


def move_srt_next_to_video(video_file_path, srt_file_path):
    video_dir = os.path.dirname(video_file_path)
    video_name_without_extension = os.path.splitext(os.path.basename(video_file_path))[0]
    subtitles_file_path = os.path.join(video_dir, f'{video_name_without_extension}.srt')
    if os.path.isfile(subtitles_file_path):
        os.remove(subtitles_file_path)
    os.rename(srt_file_path, subtitles_file_path)


def make_subtitles(video_file, config: Config):
    srt_file = make_srt_from_file(video_file, config)
    if config.translate:
        output_srt_file = srt_file.replace('.srt', f'_{config.language_to}.srt')
        translate_srt_in_place(srt_file, output_srt_file, config)
        move_srt_next_to_video(video_file, output_srt_file)
    else:
        move_srt_next_to_video(video_file, srt_file)


def main():
    video_file = ''
    if len(sys.argv) == 1:
        root = tk.Tk()
        root.withdraw()
        video_file = filedialog.askopenfilename()
    config = load_or_create_config()
    if not config.api_key:
        print('Please provide OpenAI API key in config.json')
        exit(1)
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
