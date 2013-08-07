try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


class Downloader(object):
    @classmethod
    def download(cls, url):
        if url.startswith('http'):
            print("Downloading '%s'" % url)
            return cls.download_http(url)

    @classmethod
    def download_http(self, url):
        return StringIO(urlopen(url).read())

