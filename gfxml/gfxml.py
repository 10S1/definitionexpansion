from io import StringIO
from pathlib import Path
from typing import Callable, Optional
import re
import functools
from copy import deepcopy

from lxml import etree


@functools.cache
def stanza_tokenizer():
    import stanza
    return stanza.Pipeline(lang='en', processors='tokenize')


class Node:
    def to_gf(self) -> tuple[list[tuple[str, str]], str]:
        _tags = []
        return _tags, self._to_gf(_tags)
        
    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        raise NotImplementedError()


class X(Node):
    __match_args__ = ('tag', 'children', 'attrs', 'wrapfun')

    def __init__(self, tag: str, children: list[Node], attrs: dict[str, str] = {},
                 wrapfun: Optional[str] = None):
        self.tag = tag
        self.children = children
        self.attrs = attrs
        self.wrapfun = wrapfun

    def pure_node_strings(self) -> tuple[str, str]:
        a, b = f'<{self.tag} ' + ' '.join(f'{k}="{v}"' for k, v in self.attrs.items()) + '>', f'</{self.tag}>'
        for child in self.children:
            da, db = child.pure_node_strings()
            a += da
            b = db + b
        return a, b

    def __repr__(self):
        return f'X({self.tag!r}, {self.children!r}, {self.attrs!r}, {self.wrapfun!r})'

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        tag_num = len(_tags)
        if self.wrapfun is None:
            _tags.append(self.pure_node_strings())
            return f'(tag {tag_num})'
        else:
            _tags.append((f'<{self.tag} ' + ' '.join(f'{k}="{v}"' for k, v in self.attrs.items()) + '>', f'</{self.tag}>'))
            return f'({self.wrapfun} (tag {tag_num}) {" ".join(child._to_gf(_tags) for child in self.children)})'

class XT(Node):
    __match_args__ = ('text')

    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f'XT({self.text!r})'

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        raise RuntimeError('XT nodes should only be in pure X nodes and never passed to GF')

    def pure_x_node(self) -> bool:
        return True

class G(Node):
    __match_args__ = ('node', 'children')

    def __init__(self, node: str, children: list[Node] = []):
        self.node = node
        self.children = children

    def __repr__(self):
        return f'G({self.node!r}, {self.children!r})'

    def _to_gf(self, _tags: list[tuple[str, str]]) -> str:
        return f'({self.node} {" ".join(child._to_gf(_tags) for child in self.children)})'


SHTML_NS = 'http://example.org/shtml'
MMT_NS = 'http://example.org/mmt'


def parse_shtml(path: Path) -> etree._ElementTree:
    with open(path, 'r') as f:
        # Hack: supply missing namespace declarations
        return etree.parse(
                StringIO(
                    f.read().replace(
                        '<html xmlns="http://www.w3.org/1999/xhtml">',
                        f'<html xmlns:shtml="{SHTML_NS}" xmlns:mmt="{MMT_NS}">')
                    )
                )


def get_gfxml_string(shtml: etree._ElementTree) -> tuple[list[X], str]:
    strings: list[str] = []

    nodes: list[X] = []

    def xify(node: etree._Element) -> X:
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


    def _recurse(node: etree._Element):
        tag_num = len(nodes)
        if node.tag.endswith('math'):
            # don't recurse into math nodes - place them as-is
            nodes.append(xify(node))
            strings.append(f'< {tag_num} >')
            strings.append(f'</ {tag_num} >')
            if node.tail:
                strings.append(node.tail)
            return

        # if skip_spurious_nodes and not node.text and not list(node):
        #     print(f'Skipping spurious node: {node.tag}')
        #     if node.tail:
        #         strings.append(node.tail)
        #     return

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


    nlp = stanza_tokenizer()
    doc = nlp(without_tags)
    sentences: list[str] = []
    for sent in doc.sentences:
        start = sent.words[0].start_char
        end = sent.words[-1].end_char

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

        # post-processing
        sentence = sentence.replace('>', '> ')
        sentence = sentence.replace('<', ' <')

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
                raise ValueError(f'Expected {s}, got end of string')
            if ast_str[i + j] != s[j]:
                raise ValueError(f'Expected {s}, got {ast_str[i:i+j+1]}')
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
        if tag.startswith('wrap'):
            node = deepcopy(nodes[read_tag()])
            node.wrapfun = tag
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
                    return G(tag, children)
                elif (ast_str[i].isalnum() or ast_str[i] in {'_', '\'', '/', '?', ':', '#', '.', '-'}):
                    children.append(G(read_label()))
                else:
                    raise ValueError(f'Unexpected character in AST: {ast_str[i]}')
            return G(tag, children)
    
    node = read_node()

    if i != len(ast_str):
        raise ValueError('Unmatched opening parenthesis')

    return node


def final_recovery(string: str, recovery_info: list[tuple[str, str]]) -> str:
    for i, (open_tag, close_tag) in enumerate(recovery_info):
        string = string.replace(f'< {i} >', open_tag)
        string = string.replace(f'</ {i} >', close_tag)
    return string


def main():
    import sys
    shtml = parse_shtml(Path(sys.argv[1]))
    xs, s = get_gfxml_string(shtml)
    # print(re.sub(r'\s+', ' ', s))
    print(sentence_tokenize(s))


def test():
    import sys
    # TODO: proper package structure
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Resources')))
    import gf

    shtml = parse_shtml(Path(__file__).parent / 'test.xhtml')
    xs, string = get_gfxml_string(shtml)
    sentences = sentence_tokenize(string)
    shell = gf.GFShellRaw('gf')
    output = shell.handle_command('i ' + str(Path(__file__).parent / 'TestEng.gf'))
    for s in sentences:
        print(s)
        gf_ast = shell.handle_command(f'p "{s}"')
        print(gf_ast)
        tree = build_tree(xs, gf_ast)
        print(tree)
        # rename john to mary
        match tree:
            case G(_, [X(_, [G('john') as g], _), _]):
                g.node = 'mary'
        print(tree)
        recovery_info, gf_input = tree.to_gf()
        print(gf_input)
        gf_lin = shell.handle_command(f'linearize {gf_input}')
        print(gf_lin)
        result = final_recovery(gf_lin, recovery_info)
        print(result)


# main()
test()

