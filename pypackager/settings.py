from ConfigParser import SafeConfigParser
import os

from .constants import LICENSES
from .utils import clean_dict


class SettingsReader(dict):
    config_file = os.path.expanduser('~/.pypackager/pypackager.cfg')

    def __init__(self, config_file=None, *args, **kwargs):
        if config_file:
            self.config_file = config_file
        parser = SafeConfigParser()

        if os.path.exists(self.config_file):
            with open(self.config_file) as fh:
                parser.readfp(fh)

            _kwargs = {}
            for section in parser.sections():
                _kwargs[section] = dict(parser.items(section))

        _kwargs.update(clean_dict(kwargs))
        if 'license' in _kwargs:
            license_shortname = _kwargs['license']['type']
            if license_shortname in LICENSES:
                _kwargs['license']['classifier'] = LICENSES[license_shortname]
                _kwargs['license']['name'] = LICENSES[license_shortname].split('::')[-1].strip()
            else:
                _kwargs['license']['name'] = license_shortname
        super(SettingsReader, self).__init__(**_kwargs)
