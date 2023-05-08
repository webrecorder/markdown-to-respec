# markdown-to-respec

[![Build Status](https://github.com/webrecorder/markdown-to-respec/workflows/tests/badge.svg)](https://github.com/webrecorder/markdown-to-respec/actions/workflows/main.yml)

*markdown-to-respec* is a [Github Action] for automatically publishing Markdown files as [ReSpec] HTML. The idea is that it is easier to edit and manage specifications in Markdown, but that it's easier to read specifications in your browser as HTML. By using markdown-to-respec you can have every commit to your Markdown trigger a rebuild of your HTML specifications.

As a (silly) example [this Markdown file] will generate [this ReSpec HTML].

For the action to push to your branch you will need to grant write permission in `Settings / Actions / General / Read and write permissions`. Then you will need to create a `.github/workflows/respec.yml` file in your repository which contains:

```yaml
name: Publish Specs
on:
  push:
    branches: 
      - main
jobs:
  respec:
    runs-on: ubuntu-latest
    name: Builds the ReSpec HTML
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Generate ReSpec HTML
        uses: webrecorder/markdown-to-respec@v0.4.0
```

## Action Options

The action takes several options which you can specify using the `with` clause in your markdown-to-respec step:

* `publish_branch`: the branch to push the changes to (default `gh-pages`)
* `markdown_dir`: if you want to limit the processing to a particular directory (default `.`)

For example, to publish to another branch using an alternate build of respec_js
using Markdown files in the `docs` directory you would:

```yaml
name: Publish Specs
on:
  - push:
      branches:
        - main
jobs:
  respec:
    runs-on: ubuntu-latest
    name: Builds the ReSpec HTML
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Generate ReSpec HTML
        uses: webrecorder/markdown-to-respec@v0.1.0
        with:
          publish_branch: web
          markdown_dir: docs
```

## ReSpec Configuration

ReSpec is usually [configured] with a JSON object in order to set authors, editors, various version URLs, etc. You have two options for these.

1. Include as frontmatter in your Markdown file: see [embedded] for an example.
2. Include as a JSON file along side your Markdown file: see [external] for an example.

If you would like to use an alternate ReSpec Javascript URL you can use the `respec_js` config option either in frontmatter or the external JSON configuration.

## Command Line

If you want you can install *markdown-to-respec* and run it from the command line. This can be useful in situations where you are making local changes and want to see the resulting HTML. You should be able to use your browser to open the resulting HTML files.

```
usage: markdown-to-respec [-h] [--branch BRANCH] [--publish] [--ignore IGNORE] path

positional arguments:
  path             Path to search for Markdown files

options:
  -h, --help       show this help message and exit
  --branch BRANCH  Git branch to publish to
  --publish        Commit and push new HTML files
  --ignore IGNORE  A regex of Markdown files to ignore
```

[ReSpec]: https://respec.org/docs/
[Github Action]: https://docs.github.com/en/actions
[embedded]: https://raw.githubusercontent.com/webrecorder/markdown-to-respec/main/test-data/embedded/index.md
[external]: https://github.com/webrecorder/markdown-to-respec/tree/main/test-data/external
[this Markdown file]: https://raw.githubusercontent.com/webrecorder/markdown-to-respec/main/test-data/embedded/index.md
[this ReSpec HTML]: https://webrecorder.github.io/markdown-to-respec/test-data/embedded/
[configured]: https://respec.org/docs/#configuration-options
