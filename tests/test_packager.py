import os
from unittest import TestCase

from pypackager.settings import SettingsReader
from pypackager.base import BasePackager


class OptionsTests(TestCase):
    def test_read_configfile(self):
        config_path = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'pypackagerrc')
        settings = SettingsReader(config_file=config_path)

        self.assertEqual(settings['author']['name'], 'John Smith')

        settings = SettingsReader(config_file=config_path, author={'name': 'John Brown'})
        self.assertEqual(settings['author']['name'], 'John Brown')
        self.assertFalse('email' in settings['author'])

        package = BasePackager(settings=settings)
        self.assertEqual(package.settings['author']['name'], 'John Brown')
