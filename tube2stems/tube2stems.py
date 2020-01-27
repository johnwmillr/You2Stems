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

options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
    'progress_hooks': [hook],
    'keepvideo': False
}

def download_urls(urls, outdir='', verbose=True):
    """Download and convert YouTube URL to mp3
    :urls: (list) One or more video URLs for downloading
    :outdir: (str) (optional) Specify where to save the mp3
    Returns: None on success
    """
    options['verbose'] = verbose
    options['outtmpl'] = './tmp/FOO_%(title)s-%(id)s.%(ext)s'
    # options['outtmpl'] = 'TEST'
    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download(urls)
        return True
    except Exception as e:
        print(f'Error while downloading:\n\n{e}')
        return e
    return True

# def split_into_stems()


# Andy Shauf: 'https://www.youtube.com/watch?v=ne0VnqTHsCk'

def main():
    print('Starting main...\n')
    urls = ['https://www.youtube.com/watch?v=BaW_jenozKc']
    download_urls(urls)
    print('Done!')


if __name__ == '__main__':
    main()