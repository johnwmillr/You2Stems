# John W. Miller
# January 2020


''' Unit testing for YouTube mp3 downloader. '''

__email__ = 'john.w.millr@gmail.com'
__author__ = 'John W. Miller'
__license__ = 'MIT License'


import os
from os.path import splitext, basename, exists, join

import pytest
from tube2stems.tube2stems import Downloader


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

TEST_CONFIGURATIONS = [
    ('https://www.youtube.com/watch?v=BaW_jenozKc', 'youtube-dl_test_video', 'wav'),
    ('https://www.youtube.com/watch?v=BaW_jenozKc', 'youtube-dl_test_video', 'mp3')
]


@pytest.mark.parametrize('url, filename, codec', TEST_CONFIGURATIONS)
def test_download_youtube_audio(url, filename, codec):
    ''' Test downloading audio from a YouTube video '''

    downloader = Downloader(codec=codec)
    filename = join("tests", filename)
    
    result = downloader.download_youtube_audio(url=url, filename=filename)
    fn = f'{filename}.{codec}'
    assert exists(fn)
    os.remove(fn)