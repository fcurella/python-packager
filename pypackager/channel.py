from datetime import datetime
import json
import os
import shutil
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from .base import BasePackager
from .extractor import PackageExtractor


class PackagerChannel(BasePackager):
    _data = None
    _timestamp = None

    def __init__(self, settings):
        super(PackagerChannel, self).__init__(settings)
        self.support_dir = self.settings['support_dir']
        self.channel_url = settings['index']

    @property
    def data(self):
        if self._data is None:
            self._data = self.fetch()
            self._timestamp = datetime.utcnow()
        return self._data

    def fetch(self):
        response = urlopen(self.channel_url)
        return json.loads(response.read())

    @property
    def template_list(self):
        return self.data.keys()

    def template_info(self, template_name, template_info):
        return "%s v%s %s" % (template_name, template_info['version'], template_info['author'])

    def list(self):
        for name, info in self.data.items():
            print(self.template_info(name, info))

    def template_data(self, template_name):
        return self.data[template_name]

    def template_url(self, template_name):
        return self.template_data(template_name)['url']

    def template_version(self, template_name):
        return self.template_data(template_name)['version']

    def template_author(self, template_name):
        return self.template_data(template_name)['author']

    def download(self, template_name):
        url = self.template_url(template_name)
        download_dir = os.path.join(self.support_dir, template_name)
        os.makedirs(download_dir)
        if url.startswith('http'):
            print("Downloading '%s' from %s into %s" % (template_name, url, download_dir))
            self.download_http(template_name, url, download_dir)

    def download_http(self, template_name, url, download_dir):
        response = StringIO(urlopen(url).read())
        extractor = PackageExtractor(settings=self.settings, url=url, response=response, template_name=template_name)
        extractor.extract(download_dir)

    def remove(self, template_name):
        template_dir = os.path.join(self.support_dir, template_name)
        if os.path.exists(template_dir):
            shutil.rmtree(template_dir)
        else:
            print("Template '%s' is not installed." % template_name)
