#!/usr/bin/env python3

import os
import re
import git
import sys
import json
import logging
import pathlib
import argparse
import frontmatter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default=".", help="Path to search for Markdown files")
    parser.add_argument("--branch", help="Git branch to publish to")
    parser.add_argument("--publish", action="store_true", help="Commit and push new HTML files")
    parser.add_argument("--ignore", help="A regex of Markdown files to ignore")
    args = parser.parse_args()
    run(args.path, branch=args.branch, publish=args.publish, ignore=args.ignore)

def run(path, branch="gh-pages", publish=False, ignore=None):
    """Generate ReSpec HTML from Markdown files in supplied path.
    """
    html_files = []
    for markdown_file in markdown_files(path):
        if ignore and re.match(ignore, str(markdown_file)):
            continue
        try:
            html_file = convert(markdown_file)
            html_files.append(html_file)
        except Exception as e:
            sys.exit(f"Unable to convert {markdown_file}: {e}")
        print(f"converted {markdown_file} to {html_file}")

    if publish:
        git_push(branch, html_files)

def markdown_files(path):
    """Iterator for Markdown files in a given path.
    """
    for root, _, files in os.walk(path):
        for filename in files:
            path = pathlib.Path(root) / filename
            if path.suffix in ['.md', '.markdown']:
                yield path

def convert(markdown_file):
    """Convert a markdown_file to ReSpec HTML.
    """
    html_file = get_html_file(markdown_file)
    html_file.open('w').write(respec(markdown_file))
    return html_file

def get_html_file(markdown_file):
    """Determine HTML file path based on the Markdown path.
    """
    html_file = markdown_file.stem + '.html'
    if html_file == 'README.html':
        html_file = 'index.html'
    return markdown_file.parent / html_file

def respec(markdown_file):
    """Generate HTML for a Markdown file (or file object).
    """
    doc = parse_markdown(markdown_file)
    return head(doc.metadata) + doc.content + foot()

def head(respec_config):
    """
    Generate the head section of the ReSpec HTML including the ReSpec
    configuration.
    """
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
    """Return the footer for the ReSpec HTML.
    """
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
    if 'respec_js' not in doc.metadata:
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
    """Extract the title from the Markdown using the first header.
    """
    if 'title' not in doc.metadata and (m := re.search(r'# (.+?)$', doc.content, re.MULTILINE)):
        doc.metadata['title'] = m.group(1).strip()
        doc.content = doc.content.replace(m.group(0), '', 1)
    else:
        logging.warn("Unable to find title in Markdown or in frontmatter")
        doc.metadata['title'] = ''

def extract_section(doc, header, name):
    """
    Extract a given section from the Markdown. The header should be the text
    of the header to be extracted, and the name is the config name to use to
    refer to the extracted section.
    """
    pattern = re.compile(r'^#+ ' + header + r'$((?:\W|\w)+?)^#', re.MULTILINE)
    if name not in doc.metadata and (m := re.search(pattern, doc.content)):
        text = m.group(1).strip()
        doc.metadata[name] = text
        doc.content = doc.content.replace(m.group(0), '#', 1)
    else:
        doc.metadata[name] = ''

def load_external_config(markdown_file):
    """Look for an external JSON config for the given Markdown file.
    """
    json_file = markdown_file.stem + '.json'
    json_file = markdown_file.parent / json_file
    if json_file.is_file():
        return json.load(json_file.open('r'))
    else:
        raise Exception(f"Unable to find external ReSpec config at {json_file}")

def git_push(branch_name, html_files):
    """Publish by pushing a git branch.
    """
    repo = git.Repo(".")

    # if we are publishing to a different branch we need to switch to it
    if branch_name != repo.active_branch.name:
        branch_names = [branch.name for branch in repo.branches]
        if branch_name not in branch_names:
            branch = repo.create_head(branch_name)
        else:
            branch = repo.branches[branch_names.index(branch_name)]
        branch.checkout()

    # set user to commit as (needs to be defined)
    config = repo.config_writer()
    config.add_section('user')
    config.set('user', 'email', 'markdown-to-respec@example.com')
    config.set('user', 'name', 'markdown-to-respec')

    # commit the new HTML files
    repo.index.add(html_files)
    repo.index.commit('Latest ReSpec HTML')

    # push to the origin (assumed to be the first remote)
    repo.git.push('origin', branch_name, force=True)

if __name__ == "__main__":
    main()

