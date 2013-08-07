import os

from .settings import SettingsReader
from .creator import PackageCreator
from .channel import PackagerChannel


class Pypackager(object):
    def __init__(self, **kwargs):
        self.settings = SettingsReader(**kwargs)
        super(Pypackager, self).__init__()

    def run(self, action, *args):
        return getattr(self, action)(*args)

    def create(self, package_name, *args):
        destination = os.path.join(os.path.abspath('.'), package_name)
        creator = PackageCreator(settings=self.settings)
        creator.create(package_name, destination)

    def installed(self, *args):
        channel = PackagerChannel(settings=self.settings)
        channel.installed()

    def list(self, *args):
        channel = PackagerChannel(settings=self.settings)
        channel.list()

    def search(self, text, *args):
        channel = PackagerChannel(settings=self.settings)
        channel.search(text)

    def add(self, package_name, *args):
        channel = PackagerChannel(settings=self.settings)
        channel.add(package_name, *args)

    def remove(self, package_name, *args):
        channel = PackagerChannel(settings=self.settings)
        channel.remove(package_name)
