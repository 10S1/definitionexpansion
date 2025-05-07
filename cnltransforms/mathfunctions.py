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
        elif 'data-ftml-invisible' in child.attrs and len(child.children) == 1 and \
                isinstance(c2 := child.children[0], X) and 'data-ftml-arg' in c2.attrs:
            arg = int(c2.attrs['data-ftml-arg'])
            child = c2
        else:
            continue
        if arg in r:
            raise ValueError(f'Argument {arg} is already assigned')
        r[arg] = child

    return [r[i] for i in sorted(r.keys())]


def get_function_arg_vals(root: X) -> list[X]:
    result: list[X] = []
    for arg in get_function_args(root):
        assert len(arg.children) == 1, arg.children
        value = arg.children[0]
        assert isinstance(value, X), value
        result.append(value)
    return result


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


