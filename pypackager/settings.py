try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser
import os

from .constants import LICENSES
from .loaders import (
    URLLoader, FileSystemLoader, GitLoader, HgLoader, ChannelLoader
)
from .utils import clean_dict, recursive_update

DEFAULTS = {
    'config_file': os.path.expanduser('~/.pypackager/pypackager.cfg'),
    'template': {
        'dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template'),
        'syntax': 'pystache'
    },
    'index': 'https://raw.github.com/fcurella/pypackager-channel/master/index.json',
    'template-loaders': (
        URLLoader,
        FileSystemLoader,
        ChannelLoader,
        HgLoader,
        ChannelLoader,
    ),
    'templates_dir': os.path.join(os.path.expanduser('~/.pypackager'), 'templates'),
    'template_wrap_dir': 'template',
    'support_dir': os.path.expanduser('~/.pypackager'),
}



class RecursiveDict(dict):
    def recursive_update(self, kwargs):
        self = recursive_update(self, clean_dict(kwargs))
        return self


class SettingsLoader(RecursiveDict):
    def parse(self, config_file):
        kwargs = {}
        parser = SafeConfigParser()

        if os.path.exists(config_file):
            with open(config_file) as fh:
                parser.readfp(fh)

            for section in parser.sections():
                kwargs[section] = recursive_update(kwargs.get(section, {}), dict(parser.items(section)))

        if 'license' in kwargs and 'type' in kwargs['license']:
            license_shortname = kwargs['license']['type']
            if license_shortname in LICENSES:
                kwargs['license']['classifier'] = LICENSES[license_shortname]
                kwargs['license']['name'] = LICENSES[license_shortname].split('::')[-1].strip()
            else:
                kwargs['license']['classifier'] = LICENSES['other']
                kwargs['license']['name'] = license_shortname

        return kwargs


class DefaultsLoader(SettingsLoader):
    def __init__(self):
        super(DefaultsLoader, self).__init__(**DEFAULTS)


class UserSettingLoader(SettingsLoader):
    config_file = DEFAULTS['config_file']

    def __init__(self, config_file=None):
        if config_file is not None:
            self.config_file = config_file

        kwargs = self.parse(self.config_file)

        super(UserSettingLoader, self).__init__(**kwargs)


class TemplateSettingLoader(SettingsLoader):
    templates_dir = DEFAULTS['templates_dir']

    def __init__(self, template, loaders, settings):
        kwargs = {}

        if 'templates_dir' not in settings:
            settings['templates_dir'] = self.templates_dir

        template_dir = None
        for Loader in loaders:
            loader = Loader(settings, template)
            if loader.template_exists():
                template_dir = loader.template_path()
                break

        package_cfg = os.path.join(template_dir, '.package.cfg')
        kwargs = self.parse(package_cfg)
        super(TemplateSettingLoader, self).__init__(**kwargs)


class CommandLineSettingLoader(SettingsLoader):
    pass


class SettingsReader(dict):
    support_dir = os.path.expanduser('~/.pypackager')

    def __init__(self, config_file=None, *args, **kwargs):
        _kwargs = RecursiveDict()

        defaults = DefaultsLoader()
        command_line = CommandLineSettingLoader(**kwargs)
        user = UserSettingLoader(config_file)

        if 'index' in command_line:
            index = command_line['index']
        else:
            index = defaults['index']

        template_loader_settings = {
            'index': index,
            'template_wrap_dir': DEFAULTS['template_wrap_dir'],
            'support_dir': DEFAULTS['support_dir']
        }

        if 'template' in command_line and 'dir' in command_line['template']:
            template_dir = command_line['template']['dir']
        else:
            template_dir = defaults['template']['dir']

        template = TemplateSettingLoader(template_dir, defaults['template-loaders'], template_loader_settings)

        _kwargs.recursive_update(defaults)
        _kwargs.recursive_update(template)
        _kwargs.recursive_update(user)
        _kwargs.recursive_update(command_line)

        super(SettingsReader, self).__init__(**_kwargs)
