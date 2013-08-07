from datetime import datetime
import json
import os
import shutil
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
        self.templates_dir = settings['templates_dir']
        self.channel_url = settings['index']
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)

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
    def installed_list(self):
        templates = [d for d in os.listdir(self.templates_dir) if os.path.isdir(os.path.join(self.templates_dir, d))]
        templates.sort()
        return templates

    def installed(self):
        for name in self.installed_list:
            print(name)
        print("%d templates installed." % len(self.installed_list))

    @property
    def template_list(self):
        return self.data.keys()

    def template_info(self, template_name, template_info):
        return "%s v%s %s" % (template_name, template_info['version'], template_info['author'])

    def list(self):
        for name, info in self.data.items():
            print(self.template_info(name, info))

    def search(self, text):
        for name, info in self.data.items():
            if text in name:
                print(self.template_info(name, info))

    def template_path(self, template_name):
        return os.path.join(self.templates_dir, template_name, self.settings['template_wrap_dir'])

    def template_data(self, template_name):
        if template_name not in self.data:
            raise RuntimeError("Template '%s' not found." % template_name)
        return self.data[template_name]

    def template_url(self, template_name):
        return self.template_data(template_name)['url']

    def template_version(self, template_name):
        return self.template_data(template_name)['version']

    def template_author(self, template_name):
        return self.template_data(template_name)['author']

    def download(self, template_name, url=None):
        if url is None:
            url = self.template_url(template_name)
        destination = os.path.join(self.templates_dir, template_name)
        extractor = PackageExtractor(url=url, template_name=template_name)
        extractor.extract(destination)

    def remove(self, template_name):
        template_dir = os.path.join(self.templates_dir, template_name)
        if os.path.exists(template_dir):
            shutil.rmtree(template_dir)
        else:
            print("Template '%s' is not installed." % template_name)
