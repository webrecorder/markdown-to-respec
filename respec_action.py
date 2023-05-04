#!/usr/bin/env python3

import os
import re
import sys
import json
import pathlib
import frontmatter

def main(path='.'):
    for markdown_file in markdown_files(path):
        convert(markdown_file)

def markdown_files(path):
    for root, _, files in os.walk(path):
        for filename in files:
            path = pathlib.Path(root) / filename
            if path.suffix in ['.md', '.markdown']:
                yield path

def convert(markdown_file):
    html_file = get_html_file(markdown_file)
    html_file.open('w').write(respec(markdown_file))

def get_html_file(markdown_file):
    html_file = markdown_file.stem + '.html'
    if html_file == 'README.html':
        html_file = 'index.html'
    return markdown_file.parent / html_file

def respec(markdown_file):
    doc = parse_markdown(markdown_file)
    return head(doc.metadata) + doc.content + foot()

def head(respec_config):
    config_json = json.dumps(respec_config, default=str, indent=2)
    # conformance and sotd
    return f"""
<!DOCTYPE html>
<html>
  <head>
  <meta charset="utf8">
  <title>{respec_config['title']}</title>
  <script src="{respec_config['respec_js']}" class="remove" defer ></script>
  <script class="remove">
    var respecConfig = {config_json}
  </script>
  </head>
  <body>

<!-- these need to be flush left or else all the markdown gets mucked up -->
<section id="sotd"></section>
<section id="abstract">{respec_config['abstract']}</section>
<section id="conformance">{respec_config['conformance']}</section>

<!-- start of markdown text -->

"""

def foot():
    return """

<!-- end  of markdown text -->

  </body>
</html>"""

def parse_markdown(markdown_file):
    """
    Parse a Markdown file or file object and return a frontmatter.Post object
    If the Markdown contains no frontmatter it will look for a corresponding
    JSON file and load metadata from that instead.
    """
    doc = frontmatter.load(markdown_file)

    # if there is no frontmatter configuration look for JSON file
    if len(doc.metadata) == 0:
        doc.metadata = load_external_config(markdown_file)

    # the spec can live as markdown in the HTML as long as we tell respec
    doc.metadata['format'] = 'markdown'

    # the respec javascript
    doc.metadata['respec_js'] = 'https://www.w3.org/Tools/respec/respec-w3c'

    # respec requires these at least to be empty to work
    if 'logos' not in doc.metadata:
        doc.metadata['logos'] = []
    if 'authors' not in doc.metadata:
        doc.metadata['authors'] = []
    if 'title' not in doc.metadata:
        extract_title(doc)

    # These need to be <section> elements, but it's nice to have them as
    # headinged sections in the Markdown.
    extract_section(doc, 'Abstract', 'abstract')
    extract_section(doc, 'Conformance', 'conformance')
    extract_section(doc, 'Status of this Document', 'sotd')

    return doc

def extract_title(doc):
    if m := re.search(r'# (.+?)$', doc.content, re.MULTILINE):
        doc.metadata['title'] = m.group(1).strip()
        doc.content = re.sub(m.group(0), '', doc.content, count=1).strip()

def extract_section(doc, header, name):
    pattern = re.compile(r'^#+ ' + header + r'$((?:\W|\w)+?)^#', re.MULTILINE)
    if name not in doc.metadata and (m := re.search(pattern, doc.content)):
        text = m.group(1).strip()
        doc.metadata[name] = text
        doc.content = doc.content.replace(m.group(0), '#')
    else:
        doc.metadata[name] = ''

def load_external_config(markdown_file):
    # look for JSON config next to Markdown file
    json_file = markdown_file.stem + '.json'
    json_file = markdown_file.parent / json_file
    if json_file.is_file():
        return json.load(json_file.open('r'))
    else:
        raise Exception(f"Unable to find external ReSpec config at {json_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '.'
    main(path)
