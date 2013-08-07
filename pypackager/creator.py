import os
import shutil
import subprocess

from .base import BasePackager
from .channel import PackagerChannel
from .render import Renderer
from .exceptions import DestinationExists


class PackageCreator(BasePackager):
    blacklist = ('.package.cfg',)

    def __init__(self, **kwargs):
        super(PackageCreator, self).__init__(**kwargs)
        self.template_dir = self.settings['template']['dir']
        self.renderer = Renderer(self.settings)
        self.channel = PackagerChannel(self.settings)

    def create(self, package_name, destination):
        if os.path.exists(destination):
            if self.settings['force']:
                shutil.rmtree(destination)
            else:
                raise DestinationExists('%s already exists.' % destination)

        os.makedirs(destination)
        exit_code = self.create_license(destination, dry_run=True)
        if exit_code != 0:
            return

        scripts = self.settings.get('script', None)
        if scripts and 'prerender' in scripts:
            self.execute_script(scripts['prerender'], package_name, destination)

        context = self.settings
        context['package_name'] = package_name

        for Loader in self.settings['template-loaders']:
            loader = Loader(self.settings, self.template_dir)
            if loader.template_exists():
                source = loader.template_path()
                self.copy_skeleton(source, destination, context=context)
                loader.cleanup()
                break

        self.create_license(destination)

        if scripts and 'postrender' in scripts:
            self.execute_script(scripts['postrender'], package_name, destination)

    def copy_skeleton(self, source, destination, context):
        for root, dirnames, filenames in os.walk(source):
            for filename in filenames:
                if filename in self.blacklist:
                    continue

                template = os.path.join(root, filename)
                relpath = os.path.relpath(template, source)
                _output = os.path.join(destination, relpath)
                output = self.render(_output, context)
                dirname = os.path.dirname(output)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                with open(template) as fh:
                    content = fh.read()
                rendered = self.render(content, context)
                print(output)
                with open(output, 'w') as fh:
                    fh.write(rendered)

    def render(self, content, context=None):
        if context is None:
            context = {}
        return self.renderer.render(content, context)

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
