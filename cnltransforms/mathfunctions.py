"""
Code for matching and replacing functions in FTML math nodes.
"""
from cnltransforms.gfxml import X, XT


def get_function_args(
        root: X
) -> list[X]:
    r: dict[int, X] = {}
    for child in root.children:
        assert isinstance(child, X), type(child)
        if 'data-ftml-arg' in child.attrs:
            arg = int(child.attrs['data-ftml-arg'])
            if arg in r:
                raise ValueError(f'Argument {arg} is already assigned')
            r[arg] = child

    return [r[i] for i in sorted(r.keys())]


def apply(
        function: X,
        args: list[X],
) -> X:
    new_node = X(
        'mrow',
        attrs={
            'data-ftml-head': 'http://mathhub.info?a=sTeX/meta-inf&m=Metatheory&s=apply',
            'data-ftml-term': 'OMA',
        },
        children=[
            X('mrow', [function], {'data-ftml-arg': '1', 'data-ftml-argmode': 'i'}),
            X('mo', [XT('(')]),
        ]
    )

    for i, arg in enumerate(args):
        if i > 0:
            new_node.children.append(X('mo', [XT(',')]))
        # application arguments are counted starting from 21 for some reason...
        new_node.children.append(X('mrow', [arg], {'data-ftml-arg': str(i + 21), 'data-ftml-argmode': 'a'}))

    new_node.children.append(X('mo', [XT(')')]))

    return new_node


