import concurrent.futures
import sys
from itertools import repeat

from configuration import Config, load_or_create_config
from gpt_translate import request_chat_completion, request_translation_parallel
from request_counter import ProgressCounter
from subtitles import Subtitle, remove_tags

progress_counter = ProgressCounter('Transforming tags')


def translate_srt_in_place(input_file, output_file, config: Config):
    srt = Subtitle(input_file)
    translate_srt(srt, config)
    move_tags(srt, config)
    srt.format_augmented_text(config.translated_text_color)
    srt.save_srt_file(output_file, True)


def translate_srt(srt: Subtitle, config: Config):
    print(f'GPT translating srt from {config.language_from} to {config.language_to} with context "{config.chat_gpt_translate_context}"')
    distinct_lines = srt.get_distinct_lines_without_tags()
    translated_distinct_lines = request_translation_parallel(distinct_lines, config)
    for subtitle_line in srt.lines:
        line_index = distinct_lines.index(subtitle_line.text_without_tags)
        subtitle_line.translated_text_without_tags = translated_distinct_lines[line_index]
    print('GPT finished translating')


def move_tags(srt: Subtitle, config: Config):
    print('GPT moving tags to translated text')
    progress_counter.reset(len(srt.lines), config.chat_gpt_max_requests_per_minute)
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_threads) as executor:
        executor.map(try_move_tags_in_subtitle_line_from_parallel_executor, srt.lines, repeat(config))
    print('GPT finished moving tags')


def try_move_tags_in_subtitle_line_from_parallel_executor(subtitle_line, config: Config):
    progress_counter.wait_for_limit()
    if subtitle_line.translated_text_without_tags and subtitle_line.text_has_tags:
        subtitle_line.translated_text_with_tags = try_move_tags_to_translated_text(subtitle_line.text, subtitle_line.translated_text_without_tags, config)
    else:
        subtitle_line.translated_text_with_tags = subtitle_line.translated_text_without_tags


def try_move_tags_to_translated_text(original_line, translated_line, config: Config):
    user_content = config.chat_gpt_move_tags_user_content.format(original_line=original_line, translated_line=translated_line)
    max_attempts_to_fix_tags = 5
    for attempt in range(max_attempts_to_fix_tags):
        translated_line_with_tags = request_chat_completion(config.chat_gpt_move_tags_role, user_content, config)
        translated_line_with_tags = cleanup_chats_bullshit(translated_line, translated_line_with_tags)
        if check_tags_response_looks_legit(translated_line_with_tags, translated_line, attempt):
            return translated_line_with_tags
        print(f'Failed to move tags {attempt + 1}/{max_attempts_to_fix_tags}\nOriginal text: {original_line}\nTranslated text: {translated_line}\nResult: {translated_line_with_tags}\n\n')
    return translated_line


def cleanup_chats_bullshit(translated_line, translated_line_with_tags):
    translated_line_with_tags = translated_line_with_tags.strip('\n')
    translated_multiline = translated_line_with_tags.strip('\n').split('\n')
    if len(translated_multiline) > 1:
        translated_line_with_tags = translated_multiline[-1]
    translated_line_with_tags = translated_line_with_tags.replace('Translated text:', '').strip()
    for char in ['!', '?', '.', ',']:
        while translated_line_with_tags.endswith(char) and not translated_line.endswith(char):
            translated_line_with_tags = translated_line_with_tags[:-1]
    return translated_line_with_tags


def check_tags_response_looks_legit(translated_line_with_tags, translated_line, attempt):
    tags_count = translated_line_with_tags.count('<u>')
    if tags_count > 2:
        return False
    if attempt == 0 and tags_count == 0:
        return False
    translated_line_without_tags = remove_tags(translated_line_with_tags)
    return remove_punctuation(translated_line_without_tags) == remove_punctuation(translated_line)


def remove_punctuation(text):
    for char in ['!', '?', '.', ',', ';', ':', ':', '-']:
        text = text.replace(char, '')


def main():
    if len(sys.argv) < 4:
        print('Usage: python gpt_translate_srt.py input.srt language_from language_to "context"')
        sys.exit(1)
    config = load_or_create_config()
    input_file = sys.argv[1]
    config.language_from = sys.argv[2]
    config.language_to = sys.argv[3]
    config.context = sys.argv[4] if len(sys.argv) > 4 else ''
    output_file = input_file.replace('.srt', f'_{config.language_to}.srt')
    translate_srt_in_place(input_file, output_file, config)


if __name__ == '__main__':
    main()




