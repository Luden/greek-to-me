import concurrent.futures
from openai import OpenAI

from configuration import Config
from progress_counter import ProgressCounter

progress_counter = ProgressCounter('Translating lines')


def split_text_into_chunks(text, max_tokens):
    chunks = []
    chunk = ''
    for line in text.split('\n'):
        if not chunk:
            chunk += line
        else:
            chunk += '\n' + line
        if len(chunk) > max_tokens:
            chunks.append(chunk)
            chunk = ''
    if chunk:
        chunks.append(chunk)
    return chunks


def translate_file(input_file, output_file, config: Config):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    translated_text = request_translation(text, config)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(translated_text)


def request_chat_completion(role_content, user_content, config: Config):
    try:
        client = OpenAI(api_key=config.api_key)
        response = client.chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": role_content},
                {"role": "user", "content": user_content}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f'Failed to get response for "{user_content}"')
        print(e)
        return ''


def request_chunked_chat_completion(role_content, user_content, config: Config):
    chunks = split_text_into_chunks(user_content, config.max_tokens)
    translated_chunks = []
    for chunk in chunks:
        response = request_chat_completion(role_content, chunk, config)
        translated_chunks.append(response)
    return '\n'.join(translated_chunks)


def request_chunked_chat_completion_from_parallel_executor(role_content, user_content, config: Config):
    progress_counter.increment_and_report()
    return request_chunked_chat_completion(role_content, user_content, config)


def request_translation(text, config: Config):
    role_content = format_translator_role_content(config)
    return request_chunked_chat_completion(role_content, text, config)


def request_translation_parallel(text_list, config: Config):
    role_content = format_translator_role_content(config)
    progress_counter.reset(len(text_list))
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.max_threads) as executor:
        result = list(executor.map(lambda text: request_chunked_chat_completion_from_parallel_executor(role_content, text, config), text_list))
    return result


def format_translator_role_content(config: Config):
    additional_role_context = config.context
    if additional_role_context and not additional_role_context.endswith('.'):
        additional_role_context += '.'
    if config.is_whisper:
        additional_role_context += f' {config.whisper_context}'
    context = f' Context: {additional_role_context}' if additional_role_context else ''
    translate_request = config.translate_request_format.format(language_from=config.language_from, language_to=config.language_to)
    return f'{translate_request}{context} Text:'


