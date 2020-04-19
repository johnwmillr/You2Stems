"""
YouStem
John W. Miller
2020
"""

import os
import warnings

import youtube_dl
from spleeter.separator import Separator


warnings.filterwarnings('ignore')


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
            

class Downloader(object):

    def __init__(self, codec=None, verbose=True):
        self.codec = codec if codec else "mp3"
        self.verbose = verbose

    def create_filename(self, name, video_info):
        """
        :name: (str)
        :video_info: (str)
        """
        from string import punctuation
        
           
        # Assemble the filename from the video info
        if not name:
            name = (
                video_info.get("title")
                          .translate(str.maketrans("", "", punctuation))
                          .replace(" ", "_"))
        else:
            name = os.path.basename(name)

        # Save the file to the output directory
        root = "output/{name}.%(ext)s"
        return root.format(name=name), name

    def download_youtube_audio(self, url, filename=None, codec=None):
        """
        Download audio from a YouTube video.
        Adapted from: https://www.programcreek.com/python/example/98358/youtube_dl.YoutubeDL
        
        :url: (str)
        :filename: (str)
        :code: (str)
        """
        codec = codec if codec else self.codec

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
                filename, name = self.create_filename(filename, info_dict)
                ydl.params["outtmpl"] = filename
                ydl.download([url])

                # Assemble the output file name
                # TODO: Don't assume the desired codec was downloaded
                final_file_name = f'output/{name}.{codec}'
                return final_file_name
        except Exception as e:
            raise Exception(f"Error while downloading: {e}")

    def download_urls(self, urls, filenames, codec='mp3'):
        """
        :urls: (list)
        :filenames: (list)
        :codec: (str)
        """
        codec = codec if codec else self.codec
        msg = "`urls` and `filenames` must be the same length."
        assert len(urls) == len(filenames), msg
        
        # Download the audio for each URL
        filenames = []
        for url, filename in zip(urls, filenames):
            filenames.append(self.download_youtube_audio(url, filename))
        return filenames


class Splitter(object):

    def __init__(self, codec=None):
        self.codec = codec if codec else "mp3"

    def split_into_stems(self, filename, num_stems=2):
        """
        Split an audio track into its track stems.
        :filename: (str)
        :num_stems: (int) Number of stems to split track into.
            Options are 2, 4, or 5.
        """
        msg = "num_stems must be 2, 4, or 5."
        assert num_stems in [2, 4, 5], msg

        # Create the separator object
        separator = Separator(f"spleeter:{num_stems}stems")

        # Separate the audio track
        fileout = os.path.join(os.path.dirname(filename), 'stems')
        separator.separate_to_file(filename,
                                   fileout,
                                   codec=self.codec,
                                   filename_format='{filename}/{instrument}.{codec}')


class SongToStems(object):
    """
    Downloads YouTube audio and splits the resulting file into stems.
    """

    def __init__(self, codec=None, num_stems=2, verbose=True):
        """
        :codec: (str) Usually either 'wav' or 'mp3'
        :num_stems: (int) Number of stems to split track into.
            Options are 2, 4, or 5.
        :verbose: (bool) Toggle verbose output.
        """
        self.codec = codec if codec else "mp3"
        self.num_stems = num_stems
        self.verbose = verbose

        # Create the Downloader and Splitter instances
        self.downloader = Downloader(codec=self.codec, verbose=self.verbose)
        self.splitter = Splitter(codec=self.codec)

    def download_and_split(self, url, filename=None):
        """
        Downloads audio from YouTube, splits track into stems.
        :url: (str) YouTube video URL
        :filename: (str) Name of output file
        """
        # Download the audio
        print(url)
        youtube_audio_file = self.downloader.download_youtube_audio(
            url=url,
            filename=filename)
    
        # Split into stems
        self.splitter.split_into_stems(
            filename=youtube_audio_file,
            num_stems=self.num_stems)
