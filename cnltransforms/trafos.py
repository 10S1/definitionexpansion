"""
    Functionality for transformations.
"""

import dataclasses
from copy import deepcopy
from typing import Optional, Callable, Literal

from cnltransforms.document import Document
from cnltransforms.gfxml import Node, X, G
from cnltransforms.treeutils import parent_dict, find_nodes, get_node_type


@dataclasses.dataclass
class Definiens:
    term_uri: str
    argmarkers: list[G]
    term_type_: Literal['property', 'kind']

    # given the arguments (including the "main" argument),
    # returns the accordingly instantiated definiens
    equivalent_stmt: Callable[[list[Node]], Node]


# def arg_extract(node: Node) -> Node | Literal['anonymous']:
#     match node:
#         case X('math', [child]):
#             # TODO: Cases like x∈A
#             return child
#         # TODO: named kinds
#         case _:
#             raise Exception(f'Failed to extract argument from {node}')


def _instantiate(args: list[Node], definiens: Node) -> Callable[[list[Node]], Node]:
    print('_instantiate', args, definiens)
    def instantiate(args_: list[Node]) -> Node:
        # instantiate the definiens with the given arguments
        if len(args_) != len(args):
            raise Exception(f'Expected {len(args)} arguments, got {len(args_)}')

        definiens_ = deepcopy(definiens)
        parents = parent_dict(definiens_)

        def _recurse(node: Node):
            for (arg, arg_) in zip(args, args_):
                if node.equals(arg):
                    parents[node].parent.children[parents[node].position] = arg_
                    return
            for child in node.children:
                _recurse(child)
        _recurse(definiens_)

        return definiens_

    return instantiate


def extract_definiens(doc: Document, term_uri: str) -> Optional[list[Definiens]]:
    """
    Searches for the first definition of the term in the document and
    returns a list of PropDefs (one for each reading).
    """
    filter = lambda n: isinstance(n, X) and n.attrs.get('data-ftml-definiendum') == term_uri
    for sentence in doc.sentences:
        if not sentence.trees:
            continue

        node = next(find_nodes(sentence.trees[0], filter, search_matches=False), None)
        if node is None:
            continue

        # we found the definition
        result: list[Definiens] = []
        for reading in sentence.trees:
            node = next(find_nodes(reading, filter), None)
            if node is None:
                raise Exception('Definiendum not found in all readings')

            parents = parent_dict(reading)

            match parents[parents[node].parent].parent:
                case G('iff_stmt', [G(define_term_prop, [mainarg, _node]), definiens]) \
                    if define_term_prop.startswith('define_term_prop'):
                    assert node == _node
                    result.append(Definiens(term_uri, [], 'property', _instantiate([deepcopy(get_mainarg_from_math(mainarg))], definiens)))

                case _:
                    raise Exception('Failed to match definition type')

        return result


def get_mainarg_from_math(node: Node) -> X:
    if isinstance(node, G):
        assert node.node == 'math_term'
        return get_mainarg_from_math(node.children[0])
    assert isinstance(node, X), node
    # TODO: Cases like x∈A
    if node.tag == 'math':
        children = node.children
        if len(children) == 1:
            return get_mainarg_from_math(children[0])
    elif node.tag == 'mrow':
        return get_mainarg_from_math(node.children[0])
    return node


def get_mainarg_from_context(root: Node, for_: Node) -> Optional[tuple[Node, X]]:
    """
        ("every integer is positive", "integer") -> ("every integer X is positive", "X"),
        ("z is positive", "z") -> ("z is positive", "z"),
    """
    parents = parent_dict(root)
    assert for_ in parents

    if get_node_type(for_) == 'Property':
        match parents.get_parent(for_, skip_X=True):
            case G('property_prekind'):
                return get_mainarg_from_context(root, parents.get_parent(for_, skip_X=True))

    elif get_node_type(for_) == 'PreKind':
        return get_mainarg_from_context(
            root,
            parents.filter_parent(for_, lambda n: get_node_type(n) == 'NamedKind')
        )

    elif get_node_type(for_) == 'NamedKind':
        match for_:
            case G('name_kind', [_kind, G('no_ident')]):
                # anonymous kinds -> get from context or definientia inject new identifier
                # TODO: implement this
                match parents.get_parent(for_, skip_X=True):
                    case G('let_kind_stmt', [G('math_ident', [formula]), nk]):
                        assert nk == for_
                        return get_mainarg_from_context(root, formula)
            case G('name_kind', [_kind, ident]):
                return get_mainarg_from_context(root, ident)

    elif isinstance(for_, X):
        # TODO: this has to be expanded
        if for_.tag == 'math':
            return root, deepcopy(get_mainarg_from_math(for_))
        elif for_.tag in {'mi', 'msub', 'msup', 'msubsup'}:
            return root, deepcopy(for_)
        elif for_.tag in {'span'}:
            return get_mainarg_from_context(root, for_.children[0])

    print('P8143: Failed to find main argument for', for_)
    return None


def trafo_definition_expansion(root: Node, reference_doc: Document, term_uri: str) -> Optional[list[Node]]:
    definientia = extract_definiens(reference_doc, term_uri)
    if not definientia:
        print(f'P5413: No definition found for {term_uri} in {reference_doc.path}')
        return None

    incomplete = [deepcopy(root)]   # trees that may still have references
    already_created: set[str] = set()     # no need to generate anything twice
    finished = []

    def _find_ref(node: Node) -> Optional[Node]:
        return next(find_nodes(
            node,
            lambda n: isinstance(n, X) and n.attrs.get('data-ftml-head') == term_uri,
            search_matches=False
        ), None)

    while incomplete:
        node = incomplete.pop()
        reference = _find_ref(node)
        if not reference:
            finished.append(node)
            continue

        mainarg_result = get_mainarg_from_context(node, reference)

        if mainarg_result is None:
            print(f'P92345: Failed to find main argument for {reference}')
            return None

        root, mainarg = mainarg_result

        for definiens in definientia:
            new_root = deepcopy(root)
            reference = _find_ref(new_root)   # we're working in a copy
            parents = parent_dict(new_root)
            if definiens.term_type_ == 'property':
                p = parents.get_parent(reference, skip_X=True)
                match p:
                    case G('property_prekind', [_property, prekind]):
                        # remove the reference
                        pp = parents.get_parentinfo(p, skip_X=True)
                        if pp is None:
                            print('Failed to find parent of property_prekind')
                            return None
                        pp.parent.children[pp.position] = prekind
                        ppp = parents.filter_parent(p, lambda a: get_node_type(a) == 'NamedKind')
                        if ppp is None:
                            print('Failed to find parent of type NamedKind')
                            return None
                        pppp = parents.get_parentinfo(ppp)
                        if pppp is None:
                            print('Failed to find parent of NamedKind')
                            return None
                        pppp.parent.children[pppp.position] = G(
                            'such_that_named_kind', [ppp, definiens.equivalent_stmt([mainarg])]
                        )
                        incomplete.append(new_root)
                    case _:
                        print(f'Unsupported parent type {p}')
                        return None
            else:
                # TODO
                print(f'Unsupported term type {definiens.term_type_}')
                return None

            hashable_repr = repr(new_root)
            if hashable_repr in already_created:
                continue
            already_created.add(hashable_repr)
            incomplete.append(new_root)

    return finished
