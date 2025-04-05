"""
Library for documenting the transformation process as HTML.
Not thread-safe at all.
"""
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from cnltransforms.document import linearize_tree
from cnltransforms.gf import GFShellRaw
from cnltransforms.gfxml import Node
from cnltransforms.treevis import dot_to_svg, tree_to_dot


class S:
    """ global state """
    doc: Optional[str] = None
    suppress: bool = False
    default_shell: Optional[GFShellRaw] = None

@contextmanager
def new_doc(path: Path):
    assert S.doc is None, 'Another document is already open'
    S.doc = ''
    S.suppress = False
    S.doc += '''<html>
    <head>
        <title>Transformation Process</title>
        <style>
            details { margin-left: 1em; border: 1px solid #ccc; padding: 0.5em; }
            summary { cursor: pointer; font-weight: bold; }
            pre { white-space: pre-wrap; background-color: #f0f0f0; padding: 0.5em; }
            /* svg { transform: scale(0.5); display: block; margin: 0 auto; } */
        </style>
    </head>
    <body>'''
    try:
        yield
    finally:
        S.doc += '</body></html>'
        with open(path, 'w') as f:
            f.write(S.doc)
        S.doc = None

def set_default_shell(shell: GFShellRaw):
    S.default_shell = shell

def push_html(html: str):
    if S.suppress:
        return
    assert S.doc is not None, 'No document open'
    S.doc += html

def push_sentence_tree(tree: Node):
    assert S.default_shell is not None, 'No default shell set'
    push_html(linearize_tree(tree, S.default_shell))
    push_tree(tree)

def push_tree(tree: Node):
    with details('Tree'):
        push_html('<pre>' + repr(tree) + '</pre>')
        push_html('<div>')
        push_html(dot_to_svg(tree_to_dot(tree, no_attrs=True)))
        push_html('</div>')

@contextmanager
def details(summary: str):
    push_html(f'<details><summary>{summary}</summary>')
    try:
        yield
    finally:
        push_html('</details>')

@contextmanager
def suppress_docu():
    previous_value = S.suppress
    S.suppress = True
    try:
        yield
    finally:
        S.suppress = previous_value
