import os
import subprocess

from .base import BasePackager
from .render import Renderer
from .exceptions import DestinationExists


class PackageCreator(BasePackager):
    blacklist = ('.package.cfg',)

    def __init__(self, package_name, **kwargs):
        super(PackageCreator, self).__init__(**kwargs)
        self.package_name = package_name
        self.template_dir = self.settings['template']['dir']
        self.renderer = Renderer(self.settings)

    def copy_skeleton(self, destination, context):
        if os.path.exists(destination):
            raise DestinationExists('%s already exists.' % destination)

        for root, dirnames, filenames in os.walk(self.template_dir):
            for filename in filenames:
                if filename in self.blacklist:
                    continue

                template = os.path.join(root, filename)
                relpath = os.path.relpath(template, self.template_dir)
                output = os.path.join(destination, relpath)
                dirname = os.path.dirname(output)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                with open(template) as fh:
                    content = fh.read()
                rendered = self.render(content, context)
                with open(destination, 'w') as fh:
                    fh.write(rendered)

        os.rename(os.path.join(destination, '__package_name__'), os.path.join(destination, self.package_name))

    def render(self, content, context=None):
        if context is None:
            context = {}
        return self.renderer.render(content, context)

    def create(self, destination):
        exit_code = self.create_license(destination, dry_run=True)
        if exit_code != 0:
            return

        scripts = self.settings.get('script', None)
        if scripts and 'prerender' in scripts:
            self.execute_script(scripts['prerender'], self.package_name, destination)

        self.copy_skeleton(destination, context=self.settings)
        self.create_license(destination)

        if scripts and 'postrender' in scripts:
            self.execute_script(scripts['postrender'], self.package_name, destination)

    def execute_script(self, script, *args):
        _args = (os.path.expanduser(script),) + args
        subprocess.call(' '.join(_args), shell=True, executable="/bin/bash")

    def create_license(self, destination, dry_run=False):
        args = ['lice', self.settings['license']['type'], '-p', destination]
        organization = self.settings['license'].get('organization', None)
        if organization:
            args += ['-o', organization]
        if dry_run:
            stdout = os.devnull
        else:
            stdout = os.path.join(destination, 'LICENSE')
        with open(stdout, 'w') as fh:
            return subprocess.call(args, stdout=fh)
