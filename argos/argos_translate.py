import os
import sys

os.environ['ARGOS_DEVICE_TYPE'] = 'cuda'  # should be before importing argostranslate
import argostranslate.package
import argostranslate.translate


def translate_text(text, from_name, to_name):
    install_package_with_proxy_languge(from_name, to_name)
    from_code = get_language_code(from_name)
    to_code = get_language_code(to_name)
    return argostranslate.translate.translate(text, from_code, to_code)


def translate_file(input_file, output_file, from_name, to_name):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    translated_text = translate_text(text, from_name, to_name)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(translated_text)


def install_package(from_name, to_name):
    argostranslate.package.update_package_index()
    package_to_install = get_package_by_name(from_name, to_name)
    argostranslate.package.install_from_path(package_to_install.download())


def get_package_by_name(from_name, to_name):
    available_packages = argostranslate.package.get_available_packages()
    for package in available_packages:
        if package.from_name == from_name and package.to_name == to_name:
            return package
    raise Exception(f'Package not found for {from_name} to {to_name}')


def install_package_with_proxy_languge(from_name, to_name):
    if from_name == 'English' or to_name == 'English':
        install_package(from_name, to_name)
    else:
        install_package(from_name, 'English')
        install_package('English', to_name)


def get_language_code(language_name):
    available_languages = argostranslate.translate.get_installed_languages()
    for language in available_languages:
        if language.name == language_name:
            return language.code
    raise Exception(f'Language code not found for {language_name}')


def main():
    if len(sys.argv) < 3:
        print('Usage: translate_srt.py from_language to_language input.srt output.srt \nor translate_srt.py from_language to_language "text"')
        exit(1)
    from_name = sys.argv[1]
    to_name = sys.argv[2]
    if len(sys.argv) == 5:
        input_file = sys.argv[3]
        output_file = sys.argv[4]
        translate_file(input_file, output_file, from_name, to_name)
    else:
        text = sys.argv[3]
        translated_text = translate_text(text, from_name, to_name)
        print(translated_text)


if __name__ == '__main__':
    main()

