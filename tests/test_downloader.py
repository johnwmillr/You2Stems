# John W. Miller
# January 2020


''' Unit testing for YouTube mp3 downloader. '''

__email__ = 'john.w.millr@gmail.com'
__author__ = 'John W. Miller'
__license__ = 'MIT License'


import pytest
from tube2stems.tube2stems import download_urls


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


TEST_OUTPUT_FILENAME = './tests/downloaded_audio'
TEST_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredquality': '192',
    }],
    'logger': Logger(),
    'progress_hooks': [hook],
    'keepvideo': False
}


TEST_CONFIGURATIONS = [
    ('https://www.youtube.com/watch?v=BaW_jenozKc', 'mp3'),
    ('https://www.youtube.com/watch?v=BaW_jenozKc', 'wav')
]


@pytest.mark.parametrize('url, extension', TEST_CONFIGURATIONS)
def test_download_video(url, extension):
    ''' Test downloading audio from a YouTube video '''
    TEST_OPTIONS['postprocessors'][0]['preferredcodec'] = extension
    TEST_OPTIONS['outtmpl'] = './tmp/FOO_%(title)s-%(id)s.%(ext)s'
    print(TEST_OPTIONS)

    result = download_urls([url])
    assert result == True
