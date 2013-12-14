from django.conf import settings

from django.template.base import (
    Library,
    Node,
    NodeList,
    TemplateSyntaxError,
    VariableDoesNotExist
)


register = Library()


class LoopNode(Node):
    def __init__(self, count, nodelist):
        self.count = count
        self.nodelist = nodelist

    def __repr__(self):
        return "<Loop Node: loop {0}>".format(self.count)

    def __iter__(self):
        for node in self.nodelist:
            yield node

    def render(self, context):
        try:
            values = range(self.count.resolve(context, True))
        except VariableDoesNotExist:
            values = []
        new_nodelist = NodeList()
        for i, item in enumerate(values):
            if settings.TEMPLATE_DEBUG:
                for node in self.nodelist:
                    try:
                        new_nodelist.append(node.render(context))
                    except Exception, e:
                        if not hasattr(e, "django_template_source"):
                            e.django_template_source = node.source
                        raise
            else:
                for node in self.nodelist:
                    new_nodelist.append(node.render(context))

        return new_nodelist.render(context)


@register.tag("loop")
def do_loop(parser, token):
    """
    {# {% loop n %}...{% endloop %} will repeat its contents n times. #}
    """
    bits = token.contents.split()

    if len(bits) != 2:
        raise TemplateSyntaxError("'loop' statements should have one argument: {0}".format(token.contents))

    nodelist = parser.parse(("endloop",))
    parser.delete_first_token()

    return LoopNode(parser.compile_filter(bits[1]), nodelist)
