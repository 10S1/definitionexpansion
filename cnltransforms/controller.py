import abc
import dataclasses
from collections.abc import Iterable
from pathlib import Path
from typing import Optional, Iterator

from cnltransforms.document import Document, get_shell, linearize_tree
from cnltransforms.extstruct import ExtStruct
from cnltransforms.filters import definiendum_filter
from cnltransforms.gfxml import Node, X
from cnltransforms.htmldocu import new_doc, push_html, push_tree, details, set_default_shell, push_sentence_tree
from cnltransforms.trafos import trafo_definition_expansion, extract_definiens, trafo_pushout

LOG_DIR = Path('/tmp/cnltransform-logs')
EXAMPLES_DIR = Path(__file__).parent.parent / 'sHTML' / 'Examples'
OVERHEAD_EXAMPLES = Path(__file__).parent.parent / 'sHTML' / 'Overhead' / 'All_examples'

def readings_filter(input: list[Node]) -> list[Node]:
    return definiendum_filter(input)


def color_tree(tree: Node, color: str):
    """Color the tree with the given color."""
    setattr(tree, ':color', color)
    for child in tree.children:
        color_tree(child, color)


class Trafo(abc.ABC):
    @abc.abstractmethod
    def apply(self, tree: Node) -> Optional[list[Node]]:
        pass


class DefiExpansion(Trafo):
    reference_doc: Document
    term_uri: str

    def __init__(self, reference_doc: Document, term_uri: str):
        self.reference_doc = reference_doc
        self.term_uri = term_uri
        self.definientia: Optional[list[Node]] = extract_definiens(self.reference_doc, self.term_uri)
        with details('Definientia'):
            for d in self.definientia:
                push_html(f'Arguments: <pre>{d.argmarkers}</pre>')
                push_tree(d.equivalent_stmt([(X(f'?{i}', []), None) for i in range(len(d.argmarkers) + 1)]))

    def apply(self, tree: Node) -> Optional[list[Node]]:
        if not self.definientia:
            print(f'P5413: No definition found for {self.term_uri} in {self.reference_doc.path}')
            return None

        return trafo_definition_expansion(tree, self.reference_doc, self.term_uri, self.definientia)


class Pushout(Trafo):
    def __init__(self, mapping: ExtStruct):
        self.mapping = mapping

    def apply(self, tree: Node) -> Optional[list[Node]]:
        return trafo_pushout(tree, self.mapping)


def run(example: str):
    LOG_DIR.mkdir(exist_ok=True)
    with new_doc(LOG_DIR / f'{example}.html'):
        if example == 'defexp1':
            input_doc = Document(EXAMPLES_DIR / 'Statements' / 'de-03-input.en.xhtml', readings_filter)
            set_default_shell(input_doc.shell)
            ref_doc = Document(EXAMPLES_DIR / 'definitions' / 'positive-integer.en.xhtml', readings_filter)
            print('\n\n'.join(repr(t) for t in ref_doc.sentences[0].trees))
            term_uri = 'https://stexmmt.mathhub.info/:sTeX?a=smglom/arithmetics&p=mod&m=intarith&s=positive'
            trafo = DefiExpansion(ref_doc, term_uri)
        elif example == 'defexp2':
            input_doc = Document(EXAMPLES_DIR / 'Statements' / 'de-02-input.en.xhtml', readings_filter)
            set_default_shell(input_doc.shell)
            ref_doc = Document(EXAMPLES_DIR / 'definitions' / 'consistent-set-of-propositions.en.xhtml', readings_filter)
            term_uri = 'https://stexmmt.mathhub.info/:sTeX?a=smglom/logic&p=mod&m=consistent&s=consistent'
            for sentence in input_doc.sentences:
                for tree in sentence.trees:
                    color_tree(tree, 'pink')
            for sentence in ref_doc.sentences:
                for tree in sentence.trees:
                    color_tree(tree, 'yellow')
            trafo = DefiExpansion(ref_doc, term_uri)
        elif example == 'pushout1':
            input_doc = Document(OVERHEAD_EXAMPLES / 'pushout' / 'quiver-walk-to-nts-derivation' / 'quiver-walk.en.xhtml', readings_filter)
            set_default_shell(input_doc.shell)
            ref_doc = ExtStruct(OVERHEAD_EXAMPLES / 'pushout' / 'quiver-walk-to-nts-derivation' / 'nts-derivation.en.xhtml')
            trafo = Pushout(ref_doc)


        push_html('<h1>Input</h1>')
        # push_html(input_doc.path.read_text())
        for sentence in input_doc.sentences:
            for tree in sentence.trees:
                push_sentence_tree(tree)
        push_html('<h1>Reference</h1>')
        push_html(ref_doc.path.read_text())


        for sentence in input_doc.sentences:
            with details('Sentence: ' + linearize_tree(sentence.trees[0], input_doc.shell)):
                for i, tree in enumerate(sentence.trees):
                    with details(f'Reading {i}'):
                        push_tree(tree)
                        transformed = trafo.apply(tree)
                        push_html('<h2>Transformation results:</h2>')
                        if transformed:
                            for t in transformed:
                                print(t)
                                push_sentence_tree(t)

if __name__ == '__main__':
    import sys
    # run(sys.argv[1])
    run('pushout1')
