import concurrent.futures
import sys

from configuration import Config, load_or_create_config
from gpt_translate import request_chat_completion, request_translation_parallel
from progress_counter import ProgressCounter
from subtitles import Subtitle, remove_tags

progress_counter = ProgressCounter('Transforming tags')


def translate_srt_in_place(input_file, output_file, config: Config):
    print(f'Translating {input_file} from {config.language_from} to {config.language_to} with context "{config.context}"')
    srt = Subtitle(input_file)
    distinct_lines = srt.get_distinct_lines_without_tags()
    translated_distinct_lines = request_translation_parallel(distinct_lines, config)
    for subtitle_line in srt.lines:
        line_index = distinct_lines.index(subtitle_line.text_without_tags)
        subtitle_line.translated_text_without_tags = translated_distinct_lines[line_index]
    print('Moving tags to translated text')
    if config.move_tags:
        progress_counter.reset(len(srt.lines))
        with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_tokens) as executor:
            executor.map(try_move_tags_in_subtitle_line_from_parallel_executor, srt.lines)
    srt.format_augmented_text()
    srt.save_srt_file(output_file, True)


def try_move_tags_in_subtitle_line_from_parallel_executor(subtitle_line):
    progress_counter.increment_and_report()
    if subtitle_line.translated_text_without_tags and subtitle_line.text_has_tags:
        subtitle_line.translated_text_with_tags = try_move_tags_to_translated_text(subtitle_line.text, subtitle_line.translated_text_without_tags)
    else:
        subtitle_line.translated_text_with_tags = subtitle_line.translated_text_without_tags


def try_move_tags_to_translated_text(original_line, translated_line, config: Config):
    user_content = config.move_tags_user_content.format(original_line=original_line, translated_line=translated_line)
    max_attempts_to_fix_tags = 5
    for attempt in range(max_attempts_to_fix_tags):
        translated_line_with_tags = request_chat_completion(config.move_tags_chat_role, user_content, config)
        translated_line_with_tags = cleanup_chats_bullshit(translated_line_with_tags)
        if check_tags_response_looks_legit(translated_line_with_tags, translated_line, attempt):
            return translated_line_with_tags
        print(f'Failed to move tags {attempt + 1}/{max_attempts_to_fix_tags}\nOriginal text: {original_line}\nTranslated text: {translated_line}\nResult: {translated_line_with_tags}\n\n')
    return translated_line


def cleanup_chats_bullshit(translated_line):
    return translated_line.replace('Translated text:', '').strip()


def check_tags_response_looks_legit(translated_line_with_tags, translated_line, attempt):
    tags_count = translated_line_with_tags.count('<u>')
    if tags_count > 1:
        return False
    if attempt == 0 and tags_count == 0:
        return False
    translated_line_without_tags = remove_tags(translated_line_with_tags)
    return translated_line_without_tags == translated_line


def main():
    if len(sys.argv) < 4:
        print('Usage: python translate_srt.py input.srt language_from language_to "context"')
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




