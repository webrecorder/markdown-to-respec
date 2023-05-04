# respec-action

[![Build Status](https://github.com/edsu/respec-action/workflows/tests/badge.svg)](https://github.com/edsu/respec-action/actions/workflows/main.yml)

*respec-action* is a [Github Action] for automatically publishing Markdown files as [ReSpec] HTML. The idea is that it is easier to edit and manage specifications in Markdown, but easier to read specifications in your browser using HTML. By using respec-action you can have every commit to your Markdown trigger a rebuild of your HTML specifications.

For the action to push to your gh-pages branch you will need to grant write permission in `Settings / Actions / General / Read and write permissions`. Then you will need to create a `.github/workflows/respec.yml` file in your repository which contains:

```yaml
name: Publish Specs
on:
  - push
jobs:
  respec:
    runs-on: ubuntu-latest
    name: Builds the ReSpec HTML
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Generate ReSpec HTML
        uses: edsu/respec-action@v0.1.0
```

## Action Options

The action takes several options which you can specify using the `with` clause in your respec-action step:

* `publish_branch`: the branch to push the changes to (default `gh-pages`)
* `respec_js`: a URL to use for the ReSpec JavaScript (default `https://www.w3.org/Tools/respec/respec-w3c`)

For example, to publish to another branch using an alternate build of respec_js you would:

```yaml
name: Publish Specs
on:
  - push
jobs:
  respec:
    runs-on: ubuntu-latest
    name: Builds the ReSpec HTML
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Generate ReSpec HTML
        uses: edsu/respec-action@v0.1.0
        with:
          publish_branch: web
          respec_js: https://example.com/js/respec-w3c.js
```

## ReSpec Configuration

ReSpec is usually configured with a JSON object in order to set authors, editors, various version URLs, etc. You have two options for these.

1. Include as frontmatter in your Markdown file: see [embedded] for an example.
2. Include as a JSON file along side your Markdown file: see [external] for an example.

[ReSpec]: https://respec.org/docs/
[Github Action]: https://docs.github.com/en/actions
[external]: https://raw.githubusercontent.com/edsu/respec-action/main/test-data/embedded/index.md
[embedded]: https://github.com/edsu/respec-action/tree/main/test-data/external
