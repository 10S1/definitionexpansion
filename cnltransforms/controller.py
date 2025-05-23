import abc
from pathlib import Path
from typing import Optional

from cnltransforms.document import Document, linearize_tree
from cnltransforms.extstruct import ExtStruct
from cnltransforms.filters import default_readings_filter
from cnltransforms.gfxml import Node, X
from cnltransforms.htmldocu import new_doc, push_html, push_tree, details, set_default_shell, push_sentence_tree
from cnltransforms.simplify import basic_simplify
import cnltransforms.simplify as simplify
from cnltransforms.trafos import trafo_definition_expansion, extract_definiens, trafo_pushout
from cnltransforms.treeutils import find_nodes

LOG_DIR = Path('/tmp/cnltransform-logs')
EXAMPLES_DIR = Path(__file__).parent.parent / 'sHTML' / 'Examples'
OVERHEAD_EXAMPLES = Path(__file__).parent.parent / 'sHTML' / 'Overhead' / 'All_examples'


def color_tree(tree: Node, color: str, style: Optional[str] = None):
    """Color the tree with the given color."""
    setattr(tree, ':color', color)
    if style:
        setattr(tree, ':style', style)
    for child in tree.children:
        color_tree(child, color, style)


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
        context: list[Document] = []
        if example == 'defexp1':
            input_doc = Document(EXAMPLES_DIR / 'Statements' / 'de-03-input.en.xhtml', default_readings_filter)
            set_default_shell(input_doc.shell)
            ref_doc = Document(EXAMPLES_DIR / 'definitions' / 'positive-integer.en.xhtml', default_readings_filter)
            print('\n\n'.join(repr(t) for t in ref_doc.sentences[0].trees))
            term_uri = 'https://stexmmt.mathhub.info/:sTeX?a=smglom/arithmetics&p=mod&m=intarith&s=positive'
            for sentence in input_doc.sentences:
                for tree in sentence.trees:
                    color_tree(tree, 'darkturquoise')
            for sentence in ref_doc.sentences:
                for tree in sentence.trees:
                    color_tree(tree, 'indianred', style='radial')
            trafo = DefiExpansion(ref_doc, term_uri)
        elif example == 'defexp2':
            input_doc = Document(EXAMPLES_DIR / 'Statements' / 'de-02-input.en.xhtml', default_readings_filter)
            set_default_shell(input_doc.shell)
            ref_doc = Document(EXAMPLES_DIR / 'definitions' / 'consistent-set-of-propositions.en.xhtml',
                               default_readings_filter)
            term_uri = 'https://stexmmt.mathhub.info/:sTeX?a=smglom/logic&p=mod&m=consistent&s=consistent'
            for sentence in input_doc.sentences:
                for tree in sentence.trees:
                    color_tree(tree, 'pink')
            for sentence in ref_doc.sentences:
                for tree in sentence.trees:
                    color_tree(tree, 'yellow')
            trafo = DefiExpansion(ref_doc, term_uri)
        elif example == 'pushout1':
            input_doc = Document(OVERHEAD_EXAMPLES / 'pushout' / 'quiver-walk-to-nts-derivation' / 'quiver-walk.en.xhtml',
                                 default_readings_filter)
            set_default_shell(input_doc.shell)
            context = [
                Document(OVERHEAD_EXAMPLES / 'pushout' / 'quiver-walk-to-nts-derivation' / 'nts.en.xhtml', default_readings_filter)
            ]
            ref_doc = ExtStruct(OVERHEAD_EXAMPLES / 'pushout' / 'quiver-walk-to-nts-derivation' / 'nts-derivation.en.xhtml')
            trafo = Pushout(ref_doc)

        simplify.SIMPLIFICATION_CTX = {}
        for doc in context:
            for sentence in doc.sentences:
                if sentence.trees:
                    tree = sentence.trees[0]   # any tree should work
                    for definiendum in find_nodes(tree, lambda n: isinstance(n, X) and 'data-ftml-definiendum' in n.attrs):
                        assert isinstance(definiendum, X)
                        simplify.SIMPLIFICATION_CTX.setdefault(definiendum.attrs['data-ftml-definiendum'], []).append(sentence)


        # push_html('<h1>Input</h1>')
        # # push_html(input_doc.path.read_text())
        # for sentence in input_doc.sentences:
        #     for tree in sentence.trees:
        #         push_sentence_tree(tree)
        for doc in context:
            push_html(f'<h1>Context: {doc.path}</h1>')
            push_html(doc.path.read_text())
            for sentence in doc.sentences:
                if not sentence.trees:
                    print('UNPARSED:', sentence.string)
                with details('Sentence: ' + linearize_tree(sentence.trees[0], input_doc.shell)):
                    for tree in sentence.trees:
                        push_sentence_tree(tree)

        push_html('<h1>Reference</h1>')
        push_html(ref_doc.path.read_text())


        for sentence in input_doc.sentences:
            with details('Sentence: ' + linearize_tree(sentence.trees[0], input_doc.shell)):
                options = []
                for i, tree in enumerate(sentence.trees):
                    with details(f'Reading {i}'):
                        push_tree(tree)
                        transformed = trafo.apply(tree)
                        push_html('<h2>Transformation results:</h2>')
                        if transformed:
                            for t in transformed:
                                push_html('<h3>Unsimplified</h3>')
                                push_sentence_tree(t)
                                push_html('<h3>Simplified</h3>')
                                push_sentence_tree(basic_simplify(t))
                                options.append(linearize_tree(basic_simplify(t), input_doc.shell))
                options = set(options)
                push_html('<h3>Final result:</h3>')
                if len(options) == 1:
                    push_html(f'<p>{options.pop()}</p>')
                else:
                    push_html(f'<p>Failed to find one sentence for all readings</p>')
                    push_html('<ul>')
                    for option in options:
                        push_html(f'<li>{option}</li>')
                    push_html('</ul>')


if __name__ == '__main__':
    import sys
    run(sys.argv[1])
    # run('pushout1')
