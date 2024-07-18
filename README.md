# greek-to-me
Application to generate bilingual subtitles to any video files (not only Greek), based on transcription provided by WhisperX and translation provided by ChatGPT or Argos.

## Why?
Because I wanted to learn Greek by watching SpongeBob with subtitles and see translation of subtitles at the same time. I found video with audio, but I haven't found it with subtitles.

## Features
- WhisperX will run on your GPU to transcribe video file and create `.srt` for it.
- WhisperX will also put tags into .srt so current pronounced word will be highlighted
- Argos or ChatGPT will translate .srt into your native language
- ChatGPT will move tags from original language to translated language
- Python script of this application will put it all together into one big .srt file, with original line of text above translated line of text.

## Requirements
- [python](https://www.python.org) 3.9 or any [latest release](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe), don't forget to add it to PATH
- [ffmpeg](https://www.ffmpeg.org/) any [latest release](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip), don't forget to add it to PATH
- [WhisperX](https://github.com/m-bain/whisperX)
  - Requires GPU with 10GB+ VRAM to run it with the best model 
- [Argos](https://github.com/argosopentech/argos-translate)
  - It also requires a good GPU
  - It is not required, if you chose ChatGPT for translation
- OpenAI API key for various ChatGPT requests
  - Translation
  - Tags reposition
  - Other text transformations
  - Is not required, if you chose Argos for translation and don't want to move tags

## Installation

### Happy flow
1. Clone this repo
2. Run `install.cmd` and follow instructions

### Sad flow
1. Clone this repo
2. Install [python](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe) and add it to PATH
3. Install [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip) and add bin folder to PATH
4. You need whisperx to transcribe videos. You have 2 options of installation
  - Go to whisperx folder and run `install_whisperx.cmd`, follow insructions
  - Go to whisperx folder and install whisperx manually inside it's own python virtual environment. Follow instructions on [WhisperX github](https://github.com/m-bain/whisperX)
5. You need Argos to translate subtitles. You have 2 options of installation
  - Go to argos folder and run `install_argos.cmd`, follow insructions
  - Go to argos folder and install argos manually inside it's own python virtual environment. Follow instructions on [Argos github](https://github.com/argosopentech/argos-translate)
6. You need OpenAI API key for various ChatGPT requests.
  - go to [OpenAI](https://platform.openai.com) and create an account
  - go to [Billing page](https://platform.openai.com/settings/organization/billing/overview) and manage your tariff so you'll have enough tokens to actually use chat's api (This is not an advertisement, I'll be more happy to use free offline version of ChatGPT, but there is none)
  - go to [Api keys](https://platform.openai.com/api-keys) and add a new key. Write it down somewhere.
7. Go to gpt_translate folder and run `run_sub_maker.cmd`
  - configuration file `config.json` should appear
  - put your API key there
  - change other settings if you like

## Settings
Before using the application, you need to adjust settings
- Open `config.json` in any text editor
- Change `language_from` and `language_to`
- Change ChatGPT's `model` according to your budget
- Enable `move_tags` if you want
- Enable `translate_with_gpt` if you want
- Enable `translate_with_argos` if you want
- Adjust `context` according to what videos you want to translate. The more precide context you provide, the better translation will be.
- Change other parameters if you feel lucky. 

## Usage
Application is meant to be used casually, just click on icon and everything just works (that is IF you survived installation process, good luck with that).

If you run `run_sub_maker.cmd` without arguments, it will ask for a file and then process it according to provided settings 

If you pass full file path to `run_sub_maker.cmd`, it will not ask it in UI.

## Issues
Token limits are not handled. It will stop working appropriately if you depleat your limit of ChatGPT tokens.

Transcription is BAD, but it is the best free offline solution that exist now.

Translation with Argos is HORRIBLE, but it's all you can get for free and it is still better than google translate, imo.

Translation with ChatGPT 3.5 is BAD, but it's ~10x cheaper than other models.

Translation with ChatGPT 4o is STILL BAD, but it's better than everything out there.

Tags transformation is BARELLY WORKING, but you can try to adjust context and maybe it will work a little better

Overall, it is more a toy than a tool, but enough to watch SpongeBob, otherwise it would be all greek to me.
