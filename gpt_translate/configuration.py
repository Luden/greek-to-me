import json

_config_file_path = 'config.json'


class Config:
    api_key = ''
    models_list = ['gpt-4o', 'gpt-3.5-turbo']
    model = 'gpt-3.5-turbo'
    context = 'Lines from SpongeBob SquarePants animated series'
    translate_request_format = 'Translate from {language_from} to {language_to}. Don\'t add comments or punctuation.'
    whisper_context = 'Text recorded using OpenAI Whisper with errors.'
    language_from = 'Greek'
    language_to = 'Russian'
    move_tags_chat_role = f'Place exactly a single pair of tags in the "translated text around exactly the same word where they were in the original text. Add nothing except tags.'
    move_tags_user_content = 'Original text:{original_line}\nTranslated text:{translated_line}'
    max_tokens = 1000
    max_threads = 100
    move_tags = False
    is_whisper = True
    translate = True


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
    try:
        result = load_config(Config, _config_file_path)
        if not result.language_from:
            raise Exception('Config file is invalid')
        return result
    except Exception:
        config = Config()
        save_config(config, _config_file_path)
        return config
