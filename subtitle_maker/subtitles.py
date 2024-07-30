from itertools import groupby


def wrap_in_color(text, color='yellow'):
    return f'<font color="{color}">{text}</font>'


def remove_tags(text):
    return text.replace('<u>', '').replace('</u>', '').replace('  ', ' ').strip()


class SubtitleLine:
    text = ''
    augmented_text = ''
    text_has_tags = False
    text_without_tags = ''
    translated_text_without_tags = ''
    translated_text_with_tags = ''
    end = ''
    start = ''
    index = 0

    def __init__(self, index, start, end, text):
        self.index = index
        self.start = start
        self.end = end
        self.text = text
        self.augmented_text = text
        self.text_has_tags = '<u>' in text
        self.text_without_tags = remove_tags(text)
        self.translated_text_without_tags = ''
        self.translated_text_with_tags = ''

    def format_augmented_text(self, color):
        second_line = self.translated_text_with_tags
        if self.text and not second_line:
            second_line = self.translated_text_without_tags
        second_line = wrap_in_color(second_line.strip('\n'), color)
        self.augmented_text = f'{self.text}\n{second_line}'


class Subtitle:
    lines = [SubtitleLine]

    def __init__(self, file_path):
        self.parse_srt_file(file_path)

    def get_distinct_lines_without_tags(self):
        text_lines = []
        for subtitle_line in self.lines:
            text_lines.append(subtitle_line.text_without_tags)
        distinct_lines = [k for k, g in groupby(text_lines)]
        return distinct_lines

    def format_augmented_text(self, color):
        for subtitle_line in self.lines:
            subtitle_line.format_augmented_text(color)

    def parse_srt_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            srt_text = file.read()
        file_lines = srt_text.split('\n')
        self.lines = []
        index = 0
        start = ''
        end = ''
        for line in file_lines:
            if not line:
                continue
            if line.isdigit():
                index = int(line)
            elif '-->' in line:
                start, end = line.split('-->')
                start = start.strip()
                end = end.strip()
            else:
                text = line.strip()
                subtitle = SubtitleLine(index, start, end, text)
                self.lines.append(subtitle)

    def save_srt_file(self, file_path, with_augmented_text):
        srt_text = ''
        for subtitle_line in self.lines:
            srt_text += str(subtitle_line.index) + '\n'
            srt_text += subtitle_line.start + ' --> ' + subtitle_line.end + '\n'
            srt_text_line = subtitle_line.augmented_text if with_augmented_text else subtitle_line.text
            srt_text += srt_text_line + '\n\n'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(srt_text)


