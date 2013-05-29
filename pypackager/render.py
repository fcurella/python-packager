from datetime import datetime
import pystache

from .base import BasePackager


class FileRenderer(BasePackager):
    def render(self, template_file, context):
        with open(template_file) as fh:
            template = fh.read()
        return pystache.render(template, self.get_context_data(**context))

    def get_context_data(self, **kwargs):
        kwargs.update({
            'year': datetime.now().year
        })
        return kwargs
