"""
A hacky implementation to process XML/HTML documents with GF.

It requires clean-up and documentation.
It works already and is somewhat complicated, so this is not a priority.
"""

from __future__ import annotations

import abc
from io import StringIO
from pathlib import Path
from typing import Callable, Optional
import re
import functools
from copy import deepcopy

import nltk.tokenize
from lxml import etree


@functools.cache
def stanza_tokenizer():
    import stanza
    return stanza.Pipeline(lang='en', processors='tokenize')


class Node(abc.ABC):
    children: list[Node]

    def to_gf(self) -> tuple[list[tuple[str, str]], str]:
        _tags = []
        return _tags, self._to_gf(_tags)
        
    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        raise NotImplementedError()

    def equals(self, other: Node) -> bool:
        raise NotImplementedError()


class X(Node):
    __match_args__ = ('tag', 'children', 'attrs', 'wrapfun')

    def __init__(self, tag: str, children: list[Node], attrs: dict[str, str] = {},
                 wrapfun: Optional[str] = None):
        self.tag = tag
        self.children = children
        self.attrs = attrs
        self.wrapfun = wrapfun

    def equals(self, other: Node) -> bool:
        if not isinstance(other, X):
            return False
        return (
                self.tag == other.tag and len(self.children) == len(other.children) and
                all(a.equals(b) for a, b in zip(self.children, other.children)) and
                self.attrs == other.attrs and self.wrapfun == other.wrapfun
        )

    def pure_node_strings(self) -> tuple[str, str]:
        a, b = f'<{self.tag} ' + ' '.join(f'{k}="{v}"' for k, v in self.attrs.items()) + '>', f'</{self.tag}>'
        for child in self.children:
            da, db = child.pure_node_strings()
            a += da + db
            # was:
            #   a += da
            #   b = db + b
        return a, b

    def __repr__(self):
        return f'X({self.tag!r}, {self.children!r}, {self.attrs!r}, {self.wrapfun!r})'

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        tag_num = len(_tags)
        if self.tag == 'math':
            _tags.append(self.pure_node_strings())
            return f'(wrap_math (tag {tag_num}) epsilon)'
        else:
            # if self.wrapfun is None:
            #     raise RuntimeError('wrapfun must be set')
            _tags.append((f'<{self.tag} ' + ' '.join(f'{k}="{v}"' for k, v in self.attrs.items()) + '>', f'</{self.tag}>'))
            return f'({self.wrapfun} (tag {tag_num}) {" ".join(child._to_gf(_tags) for child in self.children)})'


class XT(Node):
    __match_args__ = ('text',)

    def __init__(self, text: str):
        self.text = text
        self.children = []

    def __repr__(self):
        return f'XT({self.text!r})'

    def equals(self, other: Node) -> bool:
        return isinstance(other, XT) and self.text == other.text

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        raise RuntimeError('XT nodes should only be in pure X nodes and never passed to GF')

    def pure_x_node(self) -> bool:
        return True

    def pure_node_strings(self) -> tuple[str, str]:
        return self.text, ''   # TODO: escaping (except if it's the content of an mtext tag that was created using our hacks for recursive linearization)


class G(Node):
    __match_args__ = ('node', 'children')

    def __init__(self, node: str, children: list[Node] = []):
        self.node = node
        self.children = children

    def equals(self, other: Node) -> bool:
        if not isinstance(other, G):
            return False
        return (
                self.node == other.node and len(self.children) == len(other.children) and
                all(a.equals(b) for a, b in zip(self.children, other.children))
        )

    def __repr__(self):
        return f'G({self.node!r}, {self.children!r})'

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        return f'({self.node} {" ".join(child._to_gf(_tags) for child in self.children)})'


SHTML_NS = 'http://example.org/shtml'
MMT_NS = 'http://example.org/mmt'


def parse_shtml(path: Path) -> etree._ElementTree:
    with open(path, 'r', encoding="utf-8") as f:
        # Hack: supply missing namespace declarations
        return etree.parse(
                StringIO(
                    f.read().replace(
                        '<html xmlns="http://www.w3.org/1999/xhtml">',
                        f'<html xmlns:shtml="{SHTML_NS}" xmlns:mmt="{MMT_NS}">')
                    )
                )


def xify(node: etree._Element | str) -> X:
    if isinstance(node, str):
        node = etree.parse(StringIO(node)).getroot()
    x = X(
        tag=node.tag,
        children=[],
        attrs=node.attrib
    )
    if node.text and node.text.strip():
        x.children.append(XT(node.text))
    for child in node:
        x.children.append(xify(child))
        if child.tail and child.tail.strip():
            x.children.append(XT(child.tail))
    return x



def get_gfxml_string(shtml: etree._ElementTree) -> tuple[list[X], str]:
    strings: list[str] = []

    nodes: list[X] = []

    def _recurse(node: etree._Element):
        if isinstance(node, etree._Comment):
            return
        if node.attrib.get('data-ftml-invisible', '') == 'true':
            if node.tail:
                strings.append(node.tail)
            return
        tag_num = len(nodes)
        if node.tag.endswith('math'):
            # don't recurse into math nodes - place them as-is
            nodes.append(xify(node))
            strings.append(f'<m {tag_num} >')
            strings.append(f'</m {tag_num} >')
            if node.tail:
                strings.append(node.tail)
            return

        nodes.append(X(
            tag=node.tag,
            children=[],
            attrs=node.attrib
        ))
        strings.append(f'< {tag_num} >')
        if node.text:
            strings.append(node.text)
        for child in node:
            _recurse(child)

        strings.append(f'</ {tag_num} >')
        if node.tail:
            strings.append(node.tail)

    _recurse(shtml.getroot())

    return nodes, ''.join(strings)

def sentence_tokenize(text: str) -> list[str]:
    # simplify whitespace
    text = re.sub(r'\s+', ' ', text)

    # replace math tags <m i > </m i > with Xi
    text = re.sub(r'<m (?P<i>[0-9]+) ></m [0-9]+ >', r'X\g<i>', text)

    # we will remove all tags, but remember them to reinsert them later
    tags = [[]]   # tags[i] is the list of tags that are should be reinserted at position i
    # open_tags = [[]]   # open_tags[i] is the list of tags that are open at position i
    # close_tags = [[]]
    without_tags = ''

    i = 0
    while i < len(text):
        if text[i] == '<':
            j = i
            while text[j] != '>':
                j += 1
            tags[-1].append(text[i:j+1])
            i = j
        else:
            tags.append([])
            without_tags += text[i]
            assert len(tags) == len(without_tags) + 1
        i += 1

    #print(text)

    sentences: list[str] = []
#     nlp = stanza_tokenizer()
#     doc = nlp(without_tags)
#     for sent in doc.sentences:
#         start = sent.words[0].start_char
#         end = sent.words[-1].end_char
    for start, end in nltk.tokenize.PunktSentenceTokenizer().span_tokenize(without_tags):
        sentence = ''
        for i in range(start, end):
            for tag in tags[i]:
                sentence += tag
            sentence += without_tags[i]

        # remove unmatched tags at the beginning and end of the sentence

        open_tags = [int(match.group('i')) for match in re.finditer(r'< (?P<i>\d+) >', sentence)]
        close_tags = [int(match.group('i')) for match in re.finditer(r'</ (?P<i>\d+) >', sentence)]

        for tag in open_tags:
            if tag not in close_tags and sentence.endswith(f'</ {tag} >'):
                sentence = sentence[:-len(f'</ {tag} >')]
        for tag in close_tags:
            if tag not in open_tags and sentence.startswith(f'< {tag} >'):
                sentence = sentence[len(f'< {tag} >'):]

        # add missing tags at the beginning and end (e.g. "This </ 3 > is a sentence" -> "< 3 > This </ 3 > is a sentence")
        open_tags = [int(match.group('i')) for match in re.finditer(r'< (?P<i>\d+) >', sentence)]
        close_tags = [int(match.group('i')) for match in re.finditer(r'</ (?P<i>\d+) >', sentence)]

        for tag in close_tags:
            if tag not in open_tags:
                sentence = f'< {tag} >' + sentence
        for tag in reversed(open_tags):
            if tag not in close_tags:
                sentence = sentence + f'</ {tag} >'

        # strip away outer tags
        # e.g. < 0 > < 1 > </ 1 > Words </ 0 > -> Words
        while True:
            m = (
                re.match(r'^\s*(< (?P<i>[0-9]+) >)(?P<sentence>.*?)(</ (?P=i) >\s*)$', sentence)
                or re.match(r'^\s*(< (?P<i>[0-9]+) >)\s*(</ (?P=i) >)\s*(?P<sentence>.*?)$', sentence)
                or re.match(r'^(?P<sentence>.*?)\s*(< (?P<i>[0-9]+) >)\s*(</ (?P=i) >)\s*$', sentence)
            )
            if m:
                sentence = m.group('sentence')
            else:
                break


        # post-processing
        sentence = sentence.replace('>', '> ')
        sentence = sentence.replace('<', ' <')

        sentence = re.sub(r'\bX(?P<i>[0-9]+)\b', r'<m \g<i> > </m \g<i> >', sentence)

        sentences.append(sentence)

    return sentences


def build_tree(nodes: list[X], ast_str: str) -> Node:

    i = 0

    def read_label() -> str:
        nonlocal i
        label = ''
        while i < len(ast_str) and (ast_str[i].isalnum() or ast_str[i] in {'_', '\'', '/', '?', ':', '#', '.', '-'}):
            label += ast_str[i]
            i += 1
        return label

    def expect_str(s: str):
        nonlocal i
        for j in range(len(s)):
            if i + j >= len(ast_str):
                raise ValueError(f'Expected {s!r}, got end of string')
            if ast_str[i + j] != s[j]:
                raise ValueError(f'Expected {s!r}, got {ast_str[i:i+j+1]!r}')
        i += len(s)
    
    def read_tag() -> int:
        nonlocal i
        expect_str(' (tag ')
        number = int(read_label())
        expect_str(') ')
        return number

    
    def read_node() -> Node:
        nonlocal i
        tag = read_label()
        if tag.lower().startswith('wrap'):
            node = deepcopy(nodes[read_tag()])
            node.wrapfun = tag
            if tag == 'wrap_math':
                read_node()
            else:
                node.children = [read_node()]
            return node
        else:
            children = []
            while i < len(ast_str):
                if ast_str[i] == ' ':
                    i += 1
                elif ast_str[i] == '(':
                    i += 1
                    new_node = read_node()
                    children.append(new_node)
                elif ast_str[i] == ')':
                    i += 1
                    break
                elif (ast_str[i].isalnum() or ast_str[i] in {'_', '\'', '/', '?', ':', '#', '.', '-'}):
                    children.append(G(read_label()))
                else:
                    raise ValueError(f'Unexpected character in AST: {ast_str[i]!r}')

            if not tag:
                assert len(children) == 1
                return children[0]
            return G(tag, children)
    
    node = read_node()

    if i != len(ast_str):
        raise ValueError('Unmatched opening parenthesis')

    return node


def final_recovery(string: str, recovery_info: list[tuple[str, str]]) -> str:
    for i, (open_tag, close_tag) in enumerate(recovery_info):
        if open_tag.startswith('<math'):
            string = string.replace(f'<m {i} >', open_tag)
            string = string.replace(f'</m {i} >', close_tag)
        else:
            string = string.replace(f'< {i} >', open_tag)
            string = string.replace(f'</ {i} >', close_tag)
    return string


def tree_eq(a: Node, b: Node) -> bool:
    match (a, b):
        case (X(t1, c1, _, f1), X(t2, c2, _, f2)):
            return t1 == t2 and f1 == f2 and len(c1) == len(c2) and all(tree_eq(aa, bb) for aa, bb in zip(c1, c2))
        case (G(f1, c1), G(f2, c2)):
            return f1 == f2 and len(c1) == len(c2) and all(tree_eq(aa, bb) for aa, bb in zip(c1, c2))
        case (XT(t1), XT(t2)):
            return t1 == t2
        case (str(_), str(_)):
            return a == b
        case _:
            return False


def tree_subst(t: Node, a: Node, b: Node) -> Node:
    """ replaces all occurrences of a in t with b (ignoring attributes) """
    if tree_eq(t, a):
        return deepcopy(b)
    t = deepcopy(t)
    if isinstance(t, G) or isinstance(t, X):
        for i in range(len(t.children)):
            t.children[i] = tree_subst(t.children[i], a, b)
    return t


def get_outerNodes(t: Node, subtree: Node) -> list[Node]:
    outer_nodes = []
    if isinstance(t, G) or isinstance(t, X):
        if subtree in t.children:
            outer_nodes.append(t)
        else:
            for child in t.children:
                outer_nodes.extend(get_outerNodes(child, subtree))
    return outer_nodes


def get_firstOuterNode(t: Node, subtree: Node) -> Node:
    outer_nodes = get_outerNodes(t, subtree)
    return outer_nodes[0] if outer_nodes else None


def tree_contains_node(t: Node, n: Node) -> bool:
    if tree_eq(t, n):
        return True
    if isinstance(t, G) or isinstance(t, X):
        for child in t.children:
            if tree_contains_node(child, n):
                return True
    return False


def parse_mtext_contents(parse_fn: Callable[[str], list[str]], tree: Node) -> list[Node]:
    make_copy = lambda : deepcopy(tree)
    todo_list = [tree]
    final_result = []

    class FoundNodeException(Exception):
        def __init__(self, node: Node):
            self.node = node

    def _recurse(n: Node):
        if isinstance(n, G):
            for child in n.children:
                _recurse(child)
        elif isinstance(n, X):
            if n.tag == 'mtext':
                if not hasattr(n, '::already_processed'):
                    raise FoundNodeException(n)
            for child in n.children:
                _recurse(child)
        else:
            assert isinstance(n, XT), f'Unexpected node type: {n}'


    while todo_list:
        root = todo_list.pop()
        try:
            _recurse(root)
            final_result.append(root)   # nothing left to do
        except FoundNodeException as e:
            setattr(e.node, '::already_processed', True)
            # create string, analogously to get_gfxml_string
            strings: list[str] = []
            nodes: list[X] = []

            def _recurse2(node: X):
                tag_num = len(nodes)
                nodes.append(node)

                if node.tag.endswith('math'):
                    strings.append(f'<m {tag_num} >')
                    strings.append(f'</m {tag_num} >')
                    return

                strings.append(f'< {tag_num} >')
                for child in node.children:
                    if isinstance(child, XT):
                        strings.append(child.text)
                    else:
                        _recurse2(child)
                strings.append(f'</ {tag_num} >')

            for child in e.node.children:
                if isinstance(child, XT):
                    strings.append(child.text)
                else:
                    assert isinstance(child, X)
                    _recurse2(deepcopy(child))

            # integrate the parsed contents
            string = re.sub(r'\s+', ' ', ' '.join(strings)).strip()
            for gf_ast in parse_fn(string):
                tree = build_tree(nodes, gf_ast)
                e.node.children = [tree]
                todo_list.append(deepcopy(root))

    return final_result


def linearize_mtree_contents(linearize_fn: Callable[[str], str], tree: Node):
    if isinstance(tree, X) and tree.tag == 'mtext' and hasattr(tree, '::already_processed'):
        assert len(tree.children) == 1
        recovery_info, gf_input = tree.children[0].to_gf()
        gf_lin = linearize_fn(gf_input)
        result = final_recovery(gf_lin, recovery_info)
        tree.children = [XT(result)]  # TODO: XT content should not be escaped!
    elif isinstance(tree, G) or isinstance(tree, X):
        for i in range(len(tree.children)):
            linearize_mtree_contents(linearize_fn, tree.children[i])




def test():
    import sys
    # TODO: proper package structure
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Resources')))
    import cnltransforms.gf as gf

    shtml = parse_shtml(Path(__file__).parent / 'test.xhtml')
    xs, string = get_gfxml_string(shtml)
    print('XS', xs)
    sentences = sentence_tokenize(string)
    shell = gf.GFShellRaw('gf')
    output = shell.handle_command('i ' + str(Path(__file__).parent / 'TestEng.gf'))
    for s in sentences:
        print('------------------------')
        print(s)
        gf_ast = shell.handle_command(f'p "{s[:-1]}"')
        print(gf_ast)
        tree = build_tree(xs, gf_ast)
        print(tree)
        tree = parse_mtext_contents(lambda s: shell.handle_command(f'parse "{s}"').splitlines(), tree)[0]
        print(tree)
        # rename john to mary
        match tree:
            case G(_, [X(_, [G('john') as g], _), _]):
                g.node = 'mary'
        print(tree)
        linearize_mtree_contents(lambda s: shell.handle_command(f'linearize {s}'), tree)
        print(tree)
        recovery_info, gf_input = tree.to_gf()
        print('RECOVERY', recovery_info)
        print(gf_input)
        gf_lin = shell.handle_command(f'linearize {gf_input}')
        print(gf_lin)
        result = final_recovery(gf_lin, recovery_info)
        print(result)


if __name__ == '__main__':
    # main()
    test()

