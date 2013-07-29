from datetime import datetime

from .base import BasePackager
from .constants import RENDERERS
from .utils import instantiate_classpath


class Renderer(BasePackager):
    def __init__(self, settings):
        super(Renderer, self).__init__(settings)
        syntax_adapter = RENDERERS[self.settings['template']['syntax']]
        self.template_engine = instantiate_classpath(syntax_adapter)

    def render(self, content, context):
        return self.template_engine.render(content, self.get_context_data(**context))

    def get_context_data(self, **kwargs):
        kwargs.update({
            'year': datetime.now().year
        })
        return kwargs
