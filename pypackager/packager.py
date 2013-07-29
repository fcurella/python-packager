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

    def create(self, package_name):
        destination = os.path.join(os.path.abspath('.'), package_name)
        creator = PackageCreator(package_name=package_name, settings=self.settings)
        creator.create(destination)

    def list(self):
        channel = PackagerChannel(settings=self.settings)
        channel.list()


