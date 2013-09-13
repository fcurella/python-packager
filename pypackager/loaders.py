import os
import shutil
import subprocess

from .base import BasePackager
from .channel import PackagerChannel
from .extractor import PackageExtractor


class GenericTemplateLoader(BasePackager):
    def __init__(self, settings, template, *args, **kwargs):
        self.template = template
        super(GenericTemplateLoader, self).__init__(settings, *args, **kwargs)

    def template_exists(self):
        raise NotImplementedError

    def template_path(self):
        raise NotImplementedError

    def cleanup(self):
        pass


class FetchLoader(GenericTemplateLoader):
    def get_extract_dir(self, template_name):
        return os.path.join(self.settings['support_dir'], 'CACHE', template_name)

    def get_template_name(self, template):
        return template.rsplit('/', 1)[-1].rsplit('.', 1)[0]


class URLLoader(FetchLoader):
    def template_exists(self):
        return self.template.startswith('http')

    def template_path(self):
        template_name = self.get_template_name(self.template)
        destination = self.get_extract_dir(template_name)
        self.extractor = PackageExtractor(self.settings, url=self.template, template_name=template_name)
        self.extractor.extract(destination)
        return destination

    def cleanup(self):
        self.extractor.cleanup()


class VCSLoader(FetchLoader):
    scheme = None
    command = None

    def template_exists(self):
        return self.template.startswith(self.scheme + '+')

    def template_path(self):
        template_name = self.get_template_name(self.template)
        destination = self.get_extract_dir(template_name)
        subprocess.check_call([self.command, 'clone', self.template], cwd=destination)
        return destination

    def cleanup(self):
        shutil.rmtree(self.template)


class GitLoader(VCSLoader):
    scheme = 'git'
    command = 'git'


class HgLoader(VCSLoader):
    scheme = 'hg'
    command = 'hg'


class FileSystemLoader(GenericTemplateLoader):
    def template_exists(self):
        return os.path.exists(self.template)

    def template_path(self):
        return self.template


class ChannelLoader(GenericTemplateLoader):
    def __init__(self, settings, *args, **kwargs):
        super(ChannelLoader, self).__init__(settings, *args, **kwargs)
        self.channel = PackagerChannel(settings)

    def template_exists(self):
        return self.template in self.channel.template_list

    def template_path(self):
        return self.channel.template_path(self.template)
