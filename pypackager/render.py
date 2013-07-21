from datetime import datetime

from .base import BasePackager
from .constants import RENDERERS
from .utils import instantiate_classpath


class FileRenderer(BasePackager):
    def render(self, template_file, context):
        syntax_adapter = RENDERERS[self.settings['template']['syntax']]
        template = instantiate_classpath(syntax_adapter, template_file=template_file)
        return template.render(self.get_context_data(**context))

    def get_context_data(self, **kwargs):
        kwargs.update({
            'year': datetime.now().year
        })
        return kwargs
