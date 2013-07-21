from ConfigParser import SafeConfigParser
import os

from .constants import LICENSES
from .utils import clean_dict, recursive_update

DEFAULTS = {
    'template': {
        'dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template'),
        'syntax': 'pystache'
    }
}


class SettingsReader(dict):
    config_file = os.path.expanduser('~/.pypackager/pypackager.cfg')

    def __init__(self, config_file=None, *args, **kwargs):
        if config_file:
            self.config_file = config_file
        parser = SafeConfigParser()

        _kwargs = {}

        if 'template' in _kwargs and 'dir' in _kwargs['template']:
            package_cfg = os.path.join(_kwargs['template']['dir'], '.package.cfg')
            if os.path.exists(package_cfg):
                with open(package_cfg) as fh:
                    parser.readfp(fh)
                for section in parser.sections():
                    _kwargs[section] = recursive_update(_kwargs.get(section, {}), dict(parser.items(section)))

        if 'license' in _kwargs and 'type' in _kwargs['license']:
            license_shortname = _kwargs['license']['type']
            if license_shortname in LICENSES:
                _kwargs['license']['classifier'] = LICENSES[license_shortname]
                _kwargs['license']['name'] = LICENSES[license_shortname].split('::')[-1].strip()
            else:
                _kwargs['license']['classifier'] = LICENSES['other']
                _kwargs['license']['name'] = license_shortname

        if os.path.exists(self.config_file):
            with open(self.config_file) as fh:
                parser.readfp(fh)

            for section in parser.sections():
                _kwargs[section] = recursive_update(_kwargs.get(section, {}), dict(parser.items(section)))

        _kwargs.update(clean_dict(kwargs))

        super(SettingsReader, self).__init__(**_kwargs)
