import shutil
import subprocess
from pathlib import Path

from cnltransforms.document import Document
from cnltransforms.gf import GFShellRaw
from cnltransforms.gfxml import Node, X, XT, G, parse_shtml, get_gfxml_string, sentence_tokenize, build_tree


def graph_to_dot(g: Node) -> str:
    result = []

    def l(s: str) -> None:
        result.append(s)

    l('digraph G {')

    def traverse(n: Node) -> None:
        if isinstance(n, X):
            l(f'  n{id(n)} [label="<{n.tag} ' + ' '.join(f'{k}=\\"{v}\\"' for k, v in n.attrs.items()) + '>", shape=box]')
            for c in n.children:
                traverse(c)
                l(f'  n{id(n)} -> n{id(c)}')
        elif isinstance(n, XT):
            l(f'  n{id(n)} [label="{n.text}", shape=parallelogram]')
        elif isinstance(n, G):
            l(f'  n{id(n)} [label="{n.node}", shape=ellipse]')
            for c in n.children:
                traverse(c)
                l(f'  n{id(n)} -> n{id(c)}')
        else:
            raise ValueError(f'Unexpected node type: {type(n)}')

    traverse(g)

    l('}')
    return '\n'.join(result)


def make_graph_files(graph: Node, directory: Path = Path('/tmp'), name: str = 'graph') -> None:
    dot = graph_to_dot(graph)
    (directory / f'{name}.dot').write_text(dot)
    subprocess.run(['dot', '-Tsvg', f'{name}.dot', '-o', f'{name}.svg'], cwd=directory)


if __name__ == '__main__':
   #  shell = GFShellRaw(shutil.which('gf'))
   #  path = Path(__file__).parent.parent / 'cnl' / 'TopEng.gf'
   #  shell.handle_command(f'i {path.absolute().as_posix()}')
   #  path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'E000-firstPart.en.xhtml'
   #  shtml = parse_shtml(path)
   #  xs, string = get_gfxml_string(shtml)
   #  sentence = sentence_tokenize(string)[0]
   #  sentence = sentence[0].lower() + sentence[1:]
   #  print(sentence)
   #  gf_ast = shell.handle_command(f'p -cat=StmtFin "{sentence}"')
   #  print(gf_ast)
   #  tree = build_tree(xs, gf_ast)
   #  print(tree)
   path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'E000-firstPart.en.xhtml'
   path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'de-03-input.en.xhtml'
   # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'definitions' / 'positive-integer.en.xhtml'
   doc = Document(path)
   print(doc.sentences[0].trees[0])
   make_graph_files(doc.sentences[0].trees[0])
