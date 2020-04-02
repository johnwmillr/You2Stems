# John W. Miller
# November 2019

import youtube_dl
import warnings
warnings.filterwarnings('ignore')
from spleeter.separator import Separator


class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting...')

def download_youtube_audio(url, filename=None, codec="wav"):
    """
    Download audio from a YouTube video.
    Adapted from: https://www.programcreek.com/python/example/98358/youtube_dl.YoutubeDL
    
    :url: (str)
    :filename: (str)
    :code: (str)
    """
    def create_filename(name, video_info):
        from string import punctuation

        root = "./{name}.%(ext)s"
        if not name:
            # Assemble the filename from the video info
            name = (video_info.get("title")
                              .translate(str.maketrans("", "", punctuation))
                              .replace(" ", "_"))
        return root.format(name=name), name

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': "",
        'noplaylist': True,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': '192'}],
        'logger': Logger(),
        'progress_hooks': [hook],
        'keepvideo': False}

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            filename, name = create_filename(filename, info_dict)
            ydl.params["outtmpl"] = filename
            ydl.download([url])
            return filename, name
    except Exception as e:
        print(f"Error while downloading: {e}")
        return None, None

def download_urls(urls, filenames, codec="wav"):
    for url, filename in zip(urls, filenames):
        download_youtube_audio(url, filename, codec)

# def split_into_stems()


# Andy Shauf: 'https://www.youtube.com/watch?v=ne0VnqTHsCk'

def main():
    print('Starting main...\n')
    videos = {"andy_shauf_thirteen_hours": "https://www.youtube.com/watch?v=ne0VnqTHsCk"}
    urls = list(videos.values())
    names = list(videos.keys())
    download_urls(urls, names)
    print('Done!')

if __name__ == '__main__':
    main()