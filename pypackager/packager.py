import os
import subprocess
import shutil

from .base import BasePackager
from .render import FileRenderer
from .exceptions import DestinationExists


class PackageCreator(BasePackager):
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')

    def __init__(self, **kwargs):
        super(PackageCreator, self).__init__(**kwargs)
        self.renderer = FileRenderer(self.settings)
        if 'template' in self.settings:
            self.template_dir = self.settings['template']['dir']

    def copy_skeleton(self, destination, context):
        if os.path.exists(destination):
            raise DestinationExists('%s already exists.' % destination)

        for root, dirnames, filenames in os.walk(self.template_dir):
            for filename in filenames:
                template = os.path.join(root, filename)
                relpath = os.path.relpath(template, self.template_dir)
                output = os.path.join(destination, relpath)
                dirname = os.path.dirname(output)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                self.render(template, output, context)

        os.rename(os.path.join(destination, '__package_name__'), os.path.join(destination, self.settings['package_name']))

    def render(self, template, destination, context=None):
        if context is None:
            context = {}
        content = self.renderer.render(template, context)
        print('Saving %s' % destination)
        with open(destination, 'w') as fh:
            fh.write(content)

    def create(self, destination):
        scripts = self.settings.get('script', None)
        if scripts and 'prerender' in scripts:
            self.execute_script(scripts['prerender'], self.settings['package_name'], destination)

        self.copy_skeleton(destination, context=self.settings)
        self.create_license(destination)

        if scripts and 'postrender' in scripts:
            self.execute_script(scripts['postrender'], self.settings['package_name'], destination)

    def execute_script(self, script, *args):
        _args = (os.path.expanduser(script),) + args
        subprocess.call(' '.join(_args), shell=True, executable="/bin/bash")

    def create_license(self, destination):
        args = ['lice', self.settings['license']['type'], '-p', destination]
        organization = self.settings['license'].get('organization', None)
        if organization:
            args += ['-o', organization]
        with open(os.path.join(destination, 'LICENSE'), 'w') as fh:
            subprocess.call(args, stdout=fh)
