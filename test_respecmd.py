import io
import os
import pytest
import shutil
import pathlib
import respecmd

@pytest.fixture
def setup_data():
    if os.path.isdir('test'):
        shutil.rmtree('test')
    shutil.copytree('test-data', 'test')

def test_run(setup_data):
    assert pathlib.Path('test/subdir/index.md').is_file()

    respecmd.main('test')

    html_file = pathlib.Path('test/subdir/index.html')
    assert html_file.is_file()

    html = html_file.open().read()
    assert '<title>Test Specification</title>' in html
    assert '<section id="abstract">' in html
    assert '<section id="sotd">' in html
    assert '<section id="conformance">' in html

def test_parse():
    markdown = \
"""
# This is a title

## Status of this Document

A custom document status.

## Abstract

This is the abstract.

It can have multiple lines.

## Conformance

This is some conformance text.

## Overview

This is the overview

"""
    doc = respecmd.parse_markdown(io.StringIO(markdown))

    assert 'title' in doc.metadata
    assert doc.metadata['title'] == 'This is a title'
    assert '# This is a title' not in doc.content

    assert 'abstract' in doc.metadata
    assert doc.metadata['abstract'] == 'This is the abstract.\n\nIt can have multiple lines.'
    assert '## Abstract' not in doc.content

    assert 'sotd' in doc.metadata
    assert doc.metadata['conformance'] == 'This is some conformance text.'
    assert '## Conformance' not in doc.content

    assert doc.metadata['sotd'] == 'A custom document status.'
    assert doc.metadata['sotd'] == 'A custom document status.'
    assert '## Status of this Document' not in doc.content

def test_missing():
    markdown = \
"""
# This is a title

Everything else is missing!
"""

    doc = respecmd.parse_markdown(io.StringIO(markdown))
    assert 'abstract' in doc.metadata
    assert 'sotd' in doc.metadata
    assert 'conformance' in doc.metadata


class MockDoc:
    def __init__(self, content, metadata={}):
        self.content = content
        self.metadata = metadata
