import abc
import dataclasses
from pathlib import Path
from typing import Optional

from cnltransforms.document import Document, get_shell, linearize_tree
from cnltransforms.gfxml import Node
from cnltransforms.trafos import trafo_definition_expansion


class Trafo(abc.ABC):
    @abc.abstractmethod
    def apply(self, tree: Node) -> Optional[list[Node]]:
        pass


@dataclasses.dataclass
class DefiExpansion(Trafo):
    reference_doc: Document
    term_uri: str

    def apply(self, tree: Node) -> Optional[list[Node]]:
        return trafo_definition_expansion(tree, self.reference_doc, self.term_uri)


def run(example: str):
    if example == 'defexp1':
        input_doc = Document(Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'de-03-input.en.xhtml')
        ref_doc = Document(Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'definitions' / 'positive-integer.en.xhtml')
        term_uri = 'https://stexmmt.mathhub.info/:sTeX?a=smglom/arithmetics&p=mod&m=intarith&s=positive'
        trafo = DefiExpansion(ref_doc, term_uri)
        with open('/tmp/result.html', 'w') as f:
            f.write('<html><body>')
            for sentence in input_doc.sentences:
                f.write('<h1>Sentence</h1>')
                f.write(linearize_tree(sentence.trees[0], input_doc.shell))
                for tree in sentence.trees:
                    f.write('<h2>Tree:</h2>')
                    f.write('<pre>' + repr(tree) + '</pre>')
                    f.write('<h2>Transformed:</h2>')
                    transformed = trafo.apply(tree)
                    if transformed:
                        for t in transformed:
                            f.write('<pre>' + repr(t) + '</pre>')
                            f.write(linearize_tree(t, input_doc.shell))
            f.write('</body></html>')


if __name__ == '__main__':
    import sys
    # run(sys.argv[1])
    run('defexp1')
