"""
simplifications are functions Node -> bool
the trees are modified in place
the return value indicates if a modification was made

sometimes, multiple simplifications can modify the same part of the tree,
so order is important
"""
from copy import deepcopy
from typing import Optional, Callable

from cnltransforms.gfxml import Node, G, X
from cnltransforms.mathfunctions import get_function_arg_vals
from cnltransforms.treeutils import parent_dict


def simplify_comprehension_plain(tree: Node) -> bool:
    """ odd-numbered element of {v | v is a vertex of G} -> odd-numbered vertex of G """

    def simplify_if_match(matchroot: Node) -> bool:
        nonlocal tree

        match matchroot:
            case G('kind_with_arg', [G('prekind_to_kind', [core]), G('lex_argmark_of'), G('math_term', [X('math') as formula])]):
                pass
            case _:
                return False


        print('""""""""""""""""""""""""""""""""""""""')

        # step 1: check if the formula is a set comprehension of the right form
        if len(formula.children) != 1:
            return False
        compr = formula.children[0]
        if not isinstance(compr, X) or compr.attrs.get('data-ftml-head') != 'https://mathhub.info?a=smglom/sets&p=mod&m=set&s=set comprehension':
            return False
        comprargs = get_function_arg_vals(compr)
        assert len(comprargs) == 3
        print('B')
        if not comprargs[0].equals(comprargs[1]):
            return False
        print('C')
        match comprargs[2]:
            case X('mtext', [G('term_is_term_stmt', [G('math_term', [X('math', [subj])]), G('quantified_nkind', [
                G('existential_quantification'), G('name_kind', [G('prekind_to_kind', [obj]), G('no_ident')])])])]):
                print('C2')
                if not subj.equals(comprargs[0]):
                    return False
            case _:
                return False

        print('D')
        # step 2: check if the core refers to elementhood
        while isinstance(core, G) and core.node == {'property_prekind'}:
            core = core.children[0]
        if not isinstance(core, X) and core.attrs.get('data-ftml-head') != 'https://mathhub.info?a=smglom/sets&amp;p=mod&amp;m=set&amp;s=element':
            return False

        # Success!!! We can simplify
        print('E')
        parents = parent_dict(tree)
        print('F')
        print(core)
        print(obj)
        parents.replace_node_in_parent(core, obj)
        print('G')
        parents.replace_node_in_parent(matchroot, matchroot.children[0])

        return True

    def _recurse(node: Node) -> bool:
        if simplify_if_match(node):
            return True
        for child in node.children:
            if _recurse(child):
                return True
        return False

    if _recurse(tree):
        return True
    return False


SIMPLIFIER_T = Callable[[Node], bool]

# should be attempted in order, and (on success) be restarted from the beginning
SIMPLIFIERS: list[SIMPLIFIER_T] = [
    simplify_comprehension_plain,
]


def basic_simplify(tree: Node) -> Node:
    """ "greedily" applies all simplifications """
    tree = deepcopy(tree)

    while True:
        changed = False
        for simplifier in SIMPLIFIERS:
            if simplifier(tree):
                changed = True
                break
        if not changed:
            break

    return tree
