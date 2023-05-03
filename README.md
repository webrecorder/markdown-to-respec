# respec-action

[![Build Status](https://github.com/edsu/respec-action/workflows/tests/badge.svg)](https://github.com/edsu/respec-action/actions/workflows/main.yml)

*respec-action* is a [Github Action] for automatically publishing Markdown files as [ReSpec] HTML. The idea is that it is easier to edit and manage specifications in Markdown, but easier to read specifications in your browser using HTML. By using respec-action you can have every commit to your Markdown trigger a rebuild of your specifications.

For the action to push to your gh-pages branch you will need to grant write permission in Settings / Actions / General / Read and write permissions.

```yaml
name: Test Action
on:
  - push
jobs:
  respec:
    runs-on: ubuntu-latest
    name: Builds the ReSpec HTML
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Run respec_action
        uses: ./
```

[ReSpec]: https://respec.org/docs/
[Github Action]: https://docs.github.com/en/actions
