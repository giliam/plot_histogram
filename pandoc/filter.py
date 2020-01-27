"""
Pandoc filter to convert all headers to paragraphs with two levels plus text.
"""
from pandocfilters import toJSONFilter, Header, Str, Para

def change_head_title(key, value, format, meta):
    if key == 'Header':
        value[0] += 2
        return Header(*value)

if __name__ == "__main__":
    toJSONFilter(change_head_title)
