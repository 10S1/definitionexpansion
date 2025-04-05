import shutil
import subprocess
from pathlib import Path

from cnltransforms.document import Document
from cnltransforms.gf import GFShellRaw
from cnltransforms.gfxml import Node, X, XT, G, parse_shtml, get_gfxml_string, sentence_tokenize, build_tree


def tree_to_dot(g: Node, no_attrs: bool = False) -> str:
    result = []

    def l(s: str) -> None:
        result.append(s)

    l('digraph G {')

    def traverse(n: Node) -> None:
        extra = ''
        if hasattr(n, ':color'):
            extra = f', fillcolor="{getattr(n, ":color")}", style=filled'
        if isinstance(n, X):
            if n.tag.startswith('?'):
                l(f'  n{id(n)} [label="<{n.tag}>", shape=diamond, fillcolor="lightgreen", style=filled]')
            elif no_attrs:
                l(f'  n{id(n)} [label="<{n.tag + (' ...' if n.attrs else '')}>", shape=box{extra}]')
            else:
                l(f'  n{id(n)} [label="<{n.tag} ' + ' '.join(f'{k}=\\"{v}\\"' for k, v in n.attrs.items()) + f'>", shape=box{extra}')
            for c in n.children:
                traverse(c)
                l(f'  n{id(n)} -> n{id(c)}')
        elif isinstance(n, XT):
            l(f'  n{id(n)} [label="{n.text}", shape=parallelogram{extra}]')
        elif isinstance(n, G):
            l(f'  n{id(n)} [label="{n.node}", shape=ellipse{extra}]')
            for c in n.children:
                traverse(c)
                l(f'  n{id(n)} -> n{id(c)}')
        else:
            raise ValueError(f'Unexpected node type: {type(n)}')

    traverse(g)

    l('}')
    return '\n'.join(result)

def dot_to_svg(dot: str) -> str:
    return subprocess.run(['dot', '-Tsvg'], input=dot, text=True, capture_output=True).stdout

# def make_graph_files(graph: Node, directory: Path = Path('/tmp'), name: str = 'graph') -> None:
#     dot = graph_to_dot(graph)
#     (directory / f'{name}.dot').write_text(dot)
#     subprocess.run(['dot', '-Tsvg', f'{name}.dot', '-o', f'{name}.svg'], cwd=directory)


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
   # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'E000-firstPart.en.xhtml'
   # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'de-03-input.en.xhtml'
   # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'definitions' / 'positive-integer.en.xhtml'
   # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'de-02-input.en.xhtml'
   path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'definitions' / 'consistent-set-of-propositions.en.xhtml'
   doc = Document(path)
   print('\n---\n'.join(repr(t) for t in doc.sentences[0].trees))
   with open('/tmp/treevis-example.svg', 'w') as f:
       f.write(dot_to_svg(tree_to_dot(doc.sentences[0].trees[0])))
   # make_graph_files(doc.sentences[0].trees[0])
