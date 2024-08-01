import glob
import os
import requests
import zipfile
import shutil

_script_dir = os.path.dirname(os.path.abspath(__file__))
_output_dir = os.path.join(_script_dir, 'output')
url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"


def download_ffmpeg(url):
    local_filename = url.split('/')[-1]
    local_file_path = os.path.join(_output_dir, local_filename)
    print(f"Downloading {local_filename} from {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_file_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_file_path


def extract_ffmpeg(local_file_path):
    print(f"Extracting {local_file_path}")
    with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
        zip_ref.extractall(_output_dir)
    ffmpeg_path = glob.glob(os.path.join(_output_dir, 'ffmpeg*/bin/ffmpeg.exe'))[0]
    shutil.copy(ffmpeg_path, _script_dir)


def cleanup():
    if os.path.isdir(_output_dir):
        shutil.rmtree(_output_dir)


def main():
    if not os.path.exists(_output_dir):
        os.makedirs(_output_dir)
    ffmpeg_local_file_path = os.path.join(_script_dir, 'ffmpeg.exe')
    if os.path.isfile(ffmpeg_local_file_path):
        print("FFmpeg is already installed")
        return
    try:
        local_filename = download_ffmpeg(url)
        extract_ffmpeg(local_filename)
        if os.path.isfile(ffmpeg_local_file_path):
            print("FFmpeg is installed successfully")
    finally:
        cleanup()


if __name__ == "__main__":
    main()

