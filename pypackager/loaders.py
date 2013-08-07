import os

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


class URLLoader(GenericTemplateLoader):
    def template_exists(self):
        return self.template.startswith('http')

    def template_path(self):
        template_name = self.template.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        self.extractor = PackageExtractor(self.settings, url=self.template, template_name=template_name)
        self.extractor.extract()
        return self.extractor.extract_dir

    def cleanup(self):
        self.extractor.cleanup()


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
