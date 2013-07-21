try:
    import pystache
except ImportError:
    pass
else:
    class Pystache(object):
        def __init__(self, template_file):
            with open(template_file) as fh:
                self.template = fh.read()
            super(Pystache, self).__init__()

        def render(self, context):
            return pystache.render(self.template, context)


try:
    from jinja2 import Template
except ImportError:
    pass
else:
    class Jinja2(object):
        def __init__(self, template_file):
            with open(template_file) as fh:
                self.template = Template(fh.read())
            super(Jinja2, self).__init__()

        def render(self, context):
            return self.template.render(**context)
