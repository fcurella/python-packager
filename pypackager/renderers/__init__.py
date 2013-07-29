try:
    import pystache
except ImportError:
    pass
else:
    class Pystache(object):
        def render(self, content, context):
            return pystache.render(content, context)


try:
    from jinja2 import Template
except ImportError:
    pass
else:
    class Jinja2(object):
        def render(self, content, context):
            template = Template(content)
            return template.render(**context)
