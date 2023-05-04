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
* `markdown_dir`: if you want to limit the processing to a particular directory (default `.`)

For example, to publish to another branch using an alternate build of respec_js
using Markdown files in the `docs` directory you would:

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
          markdown_dir: docs
```

## ReSpec Configuration

ReSpec is usually configured with a JSON object in order to set authors, editors, various version URLs, etc. You have two options for these.

1. Include as frontmatter in your Markdown file: see [embedded] for an example.
2. Include as a JSON file along side your Markdown file: see [external] for an example.

If you would like to use an alternate ReSpec Javascript URL you can use the `respec_js` config option either in frontmatter or the external JSON configuration.

[ReSpec]: https://respec.org/docs/
[Github Action]: https://docs.github.com/en/actions
[external]: https://raw.githubusercontent.com/edsu/respec-action/main/test-data/embedded/index.md
[embedded]: https://github.com/edsu/respec-action/tree/main/test-data/external
