# greek-to-me
An application to generate bilingual subtitles for any video files (not just Greek), using transcriptions provided by WhisperX and translations courtesy of ChatGPT or Argos.

## Why?
Because I wanted to learn Greek by watching SpongeBob with subtitles and seeing the translation of the subtitles simultaneously. I found a video with audio, but I couldn't find one with subtitles.

![](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2VidW1zeHJmZWVxOWI1N2dkNmZ5ZjlveHBmNDFqZ2o5ZWUwbjk4YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/T3bg0UQ010ZoUCLNIy/giphy.gif)

## Features
- WhisperX opens video files with ffmpeg and then runs on your GPU to transcribe video files and create .srt files.
- WhisperX adds tags to the .srt files so the currently pronounced word is highlighted.
- Argos or ChatGPT translates the .srt files into your native language.
- ChatGPT moves the tags from the original language to the translated language.
- A Python script combines everything into one large .srt file, with the original text line above the translated text line.

## Requirements
- [Python](https://www.python.org) 3.9 or any [latest release](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe). Don’t forget to add it to PATH.
- ~12gb of free space on a disk drive
- A decent GPU
- Windows PC to run `cmd` files. Since 95% of this application is on Python, it should not be a problem for you to port it to your OS.  
  
Everything else should be installed automatically with `install.cmd`
- [FFmpeg](https://www.ffmpeg.org/)
- [WhisperX](https://github.com/m-bain/whisperX)
  - Requires a GPU with 10GB+ of memory to run the best model. Surely, everyone has one of those these days, right?
  - By default, the model is selected according to your GPU memory amount.
- [Argos](https://github.com/argosopentech/argos-translate)
  - Also requires a good GPU.
  - Not needed if you choose ChatGPT for translation.
- [OpenAI](https://platform.openai.com) API key for various ChatGPT requests: translation, tags reposition, other text transformations
  - Not needed if you choose Argos for translation and don’t want to move tags.

## Installation

### Happy flow
1. Clone this repo.
2. Install [Python](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe) and add it to PATH
3. Run `install.cmd` and wait about 10 minutes. It will install everything and then will open config.json for your pleasure

It will never work, who am I trying to fool?

### Sad flow
More like "sad, ugly, tedious, brain-melting flow". Sigh. Go grab some beer, tea, or another sedative — you'll need it.

1. Clone this repo
2. Install [Python](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe) and add it to PATH
3. Install [FFmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip) and add `bin` folder to PATH
4. You need WhisperX to transcribe videos. You have two options for installation:
  - Go to the `whisperx` folder and run `install_whisperx.cmd`, then follow the instructions.
  - Alternatively, go to the `whisperx` folder and install WhisperX manually within its own Python virtual environment. Follow the instructions on the [WhisperX github](https://github.com/m-bain/whisperX)
  - Don’t forget that you also need a CUDA-powered PyTorch installation, or else WhisperX will run unbearably slow:
```
pip install torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 --index-url https://download.pytorch.org/whl/cu121
```
5. You need Argos to translate subtitles. You have two options for installation:
  - Go to the `argos` folder and run `install_argos.cmd`, then follow the instructions.
  - Alternatively, go to the `argos` folder and install Argos manually within its own Python virtual environment. Follow the instructions on the [Argos github](https://github.com/argosopentech/argos-translate)
6. You need an OpenAI API key for various ChatGPT requests:
  - Go to [OpenAI](https://platform.openai.com) and create an account.
  - Visit the [Billing page](https://platform.openai.com/settings/organization/billing/overview) and manage your tariff to ensure you have enough tokens to actually use the ChatGPT API. (This isn’t an advertisement; I’d be happier with a free offline version of ChatGPT, but alas, there isn’t one.)
  - Go to [Api keys](https://platform.openai.com/api-keys) and add a new key. Write it down somewhere safe.
7. Go to the `subtitle_maker` folder and run `run_sub_maker.cmd`:
  - A configuration file `config.json` should appear.
  - Put your API key in that file at `chat_gpt_api_key`
  - Adjust other settings if you like.

## Settings
Before using the application, you need to adjust the settings:
- Open `config.json` in any text editor.
- Change `language_from` and `language_to`.
- Set `chat_gpt_api_key` to the one you aquired from OpenAI.
- Adjust `chat_gpt_model` according to your budget.
- Adjust `whisper_model`. By default, the model is selected according to your GPU memory amount.
- Enable `move_tags_with_chat_gpt` if desired.
- Enable `translate_with_chat_gpt` if desired.
- Enable `translate_with_argos` if desired.
- Adjust `chat_gpt_translate_context` based on the videos you want to translate. The more precise the context, the better the translation, the more tokens you will pay.
- Adjust `chat_gpt_max_requests_per_minute` to your OpenAI's tier, which is by default set to 450 sligthly below tier-1 limit of 500RPM for 4o-mini
- Change `translated_text_color` to your favourite color!
- Change other parameters if you’re feeling lucky.

## Usage
The application is designed for casual use — just click on the icon, and everything should work (assuming you survived the installation process; good luck with that).
- If you run `run_sub_maker.cmd` without arguments, it will prompt you for a file and then process it according to the provided settings.
- If you pass a full file path to `run_sub_maker.cmd`, it will bypass the UI prompt and process the file directly.

## Issues
Daily token and request limits are not handled. The application will stop working properly if you deplete your ChatGPT token limit.

- Transcription with whisperx is BAD, but it’s the best free offline solution available right now.
- Translation with Argos is HORRIBLE, but it’s all you can get for free and still better than Google Translate, in my opinion.
- Translation with ChatGPT 3.5 and 4o-mini is BAD, but it's ~10x cheaper than other models.
- Translation with ChatGPT 4o is STILL BAD, but it's better than everything else out there.
- Tags transformation is BARELY WORKING and makes A LOT of requests, depleting your daily limits, but you can try adjusting the context, and maybe it will improve a little.

Overall, it’s more of a toy than a tool, but it’s sufficient to watch SpongeBob — otherwise, it would be all Greek to me =)
