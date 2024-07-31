import json
import os

_config_file_path = 'config.json'


class Config:
    _help = 'This is a configuration file for the sub_maker. Check everything is set correctly, set your API keys and other settings. Then run sub_sub_maker.cmd'
    chat_gpt_api_key = ''
    chat_gpt_models_list = ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo']
    chat_gpt_model = 'gpt-4o-mini'
    chat_gpt_translate_context = 'Lines from SpongeBob SquarePants animated series'
    chat_gpt_translate_request_format = 'Translate from {language_from} to {language_to}. Don\'t add comments. Preserve original punctuation.'
    chat_gpt_move_tags_role = f'Place exactly a single pair of tags in the translated text around exactly the same word where they were in the original text. Add nothing except tags. Use punctuation from translated text'
    chat_gpt_move_tags_user_content = 'Original text:{original_line}\nTranslated text:{translated_line}'
    chat_gpt_max_tokens = 1000
    chat_gpt_whisper_context = 'Text recorded using OpenAI Whisper with errors.'
    language_from = 'Greek'
    language_to = 'Russian'
    max_threads = 50
    translate_with_argos = True
    translate_with_chat_gpt = False
    move_tags_with_chat_gpt = False
    transcribe_with_whisper = True
    translated_text_color = 'yellow'

    def check_valid(self):
        is_translation_enabled = self.translate_with_chat_gpt or self.translate_with_argos
        is_chat_gpt_required = self.translate_with_chat_gpt and self.move_tags_with_chat_gpt
        if is_chat_gpt_required and not self.chat_gpt_api_key:
            raise Exception('api_key for ChatGPT is missing, while translate_with_gpt or move_tags is enabled')
        if self.translate_with_chat_gpt and self.translate_with_argos:
            raise Exception('translate_with_gpt and translate_with_argos cannot be both enabled')
        if is_translation_enabled and (not self.language_from or not self.language_to):
            raise Exception('Languages are not set')
        if self.move_tags_with_chat_gpt and not self.chat_gpt_move_tags_role:
            raise Exception('Move tags chat role is not set')
        if self.move_tags_with_chat_gpt and not self.chat_gpt_move_tags_user_content:
            raise Exception('Move tags user content is not set')
        if self.translate_with_chat_gpt and not self.chat_gpt_translate_request_format:
            raise Exception('Translate request format is not set')
        if self.transcribe_with_whisper and not self.chat_gpt_whisper_context:
            raise Exception('Whisper context is not set')
        if self.translate_with_chat_gpt and not self.chat_gpt_model:
            raise Exception('Model is not set')


def save_config(config, filename):
    config_dict = {key: getattr(config, key) for key in dir(config) if not key.startswith('__') and not callable(getattr(config, key))}
    with open(filename, 'w') as file:
        json.dump(config_dict, file, indent=4)


def load_config(config_class, filename):
    with open(filename, 'r') as file:
        config_dict = json.load(file)
    config = config_class()
    for key, value in config_dict.items():
        setattr(config, key, value)
    return config


def load_or_create_config():
    if not os.path.isfile(_config_file_path):
        config = Config()
        save_config(config, _config_file_path)
        print(f'Created default config file at {_config_file_path}. Please edit it and run the script again.')
        return config
    print(f'Loading config file from {_config_file_path}')
    try:
        result = load_config(Config, _config_file_path)
        result.check_valid()
        return result
    except Exception as ex:
        print(ex)
        print(f'Failed to load config file {_config_file_path}, please fix it manually or delete it to create a new one.')
        exit(1)


if __name__ == '__main__':
    load_or_create_config()


