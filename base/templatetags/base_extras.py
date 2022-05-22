import markdown
from django import template

register = template.Library()


@register.filter
def convert_markdown(text):
    return markdown.markdown(text, extensions=["markdown.extensions.fenced_code"])
