import html
import re


def escape_markdown(text):
    """Helper function to escape telegram markup symbols."""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def mention_html(user_id, name):
    return '<a href="tg://user?id={}">{}</a>'.format(
        user_id,
        html.escape(name),
    )