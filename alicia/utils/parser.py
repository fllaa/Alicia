import re


def escape_markdown(text):
    """Helper function to escape telegram markup symbols."""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)