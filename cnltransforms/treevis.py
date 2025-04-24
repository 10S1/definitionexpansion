import subprocess
from pathlib import Path

from cnltransforms.document import Document
from cnltransforms.gfxml import Node, X, XT, G, build_tree


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
                l(f'  n{id(n)} [label="<{n.tag} ' + ' '.join(f'{k}=\\"{v}\\"' for k, v in n.attrs.items()) + f'>", shape=box{extra}]')
            for c in n.children:
                traverse(c)
                l(f'  n{id(n)} -> n{id(c)}')
        elif isinstance(n, XT):
            l(f'  n{id(n)} [label="{n.text}", shape=parallelogram{extra}]')
        elif isinstance(n, G):
            if n.node.startswith('Δ'):
                l(f'  n{id(n)} [label="{n.node[1:]}", shape=triangle{extra}]')
            else:
                l(f'  n{id(n)} [label="{n.node}", shape=ellipse{extra}]')
            for c in n.children:
                traverse(c)
                l(f'  n{id(n)} -> n{id(c)}')
        else:
            raise ValueError(f'Unexpected node type: {type(n)}')

    traverse(g)

    l('}')
    return '\n'.join(result)


def tree_to_qtree(g: Node) -> str:
    result = []

    def l(s: str) -> None:
        result.append(s)

    def get_label(n: Node) -> str:
        if isinstance(n, X):
            return r'\textless' +  n.tag.replace('_', r'\_') + r'\textgreater'
        elif isinstance(n, XT):
            return n.text.replace('_', r'\_')
        elif isinstance(n, G):
            return n.node.replace('_', r'\_')
        else:
            raise ValueError(f'Unexpected node type: {type(n)}')

    def traverse(n: Node) -> None:
        if isinstance(n, X) or isinstance(n, G):
            if n.children:
                l(f'[ .{{ \\astnode{{ {get_label(n)} }} }}')
            else:
                l(f'{{ \\astnode{{ {get_label(n)} }} }}')
            for c in n.children:
                traverse(c)
            if n.children:
                l(']')
        elif isinstance(n, XT):
            l(f'{{ \\astnode{{ {get_label(n)} }} }}')
        else:
            raise ValueError(f'Unexpected node type: {type(n)}')

    l(r'\Tree')
    traverse(g)
    l(r';')
    return ' '.join(result)


def dot_to_svg(dot: str) -> str:
    return subprocess.run(['dot', '-Tsvg'], input=dot, text=True, capture_output=True).stdout

if __name__ == '__main__':
    import sys
    path = Path(sys.argv[1])
    if not path.exists():
        print(dot_to_svg(
            tree_to_dot(build_tree([], sys.argv[1]))
        ))
        # print(
        #     tree_to_qtree(build_tree([], sys.argv[1]))
        # )
    else:
    # # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'E000-firstPart.en.xhtml'
    # # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'de-03-input.en.xhtml'
    # # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'definitions' / 'positive-integer.en.xhtml'
    # # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'Statements' / 'de-02-input.en.xhtml'
    # path = Path(__file__).parent.parent / 'sHTML' / 'Examples' / 'definitions' / 'consistent-set-of-propositions.en.xhtml'
        doc = Document(path)
        with open('/tmp/treevis.html', 'w') as f:
            f.write('<html><head></head><body>')
            for sentence in doc.sentences:
                f.write(f'<h1>{sentence.string}</h1>')
                for tree in sentence.trees:
                    f.write(dot_to_svg(tree_to_dot(tree, no_attrs=True)))
            f.write('</body></html>')
        # print('\n---\n'.join(repr(t) for t in doc.sentences[0].trees))
        # with open('/tmp/treevis-example.svg', 'w') as f:
        #     f.write(dot_to_svg(tree_to_dot(doc.sentences[0].trees[0])))
