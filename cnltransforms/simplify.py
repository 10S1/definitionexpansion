"""
simplifications are functions Node -> bool
the trees are modified in place
the return value indicates if a modification was made

sometimes, multiple simplifications can modify the same part of the tree,
so order is important
"""
import re
from copy import deepcopy
from typing import Optional, Callable

from cnltransforms.document import Sentence
from cnltransforms.gfxml import Node, G, X, XT
from cnltransforms.htmldocu import details, push_tree, push_sentence_tree
from cnltransforms.mathfunctions import get_function_arg_vals
from cnltransforms.treeutils import parent_dict, find_nodes, get_node_type


SIMPLIFICATION_CTX: dict[str, list[Sentence]] = {

}


def simplify_comprehension_plain(tree: Node) -> bool:
    """ odd-numbered element of {v | v is a vertex of G} -> odd-numbered vertex of G """

    def simplify_if_match(matchroot: Node) -> bool:
        nonlocal tree

        match matchroot:
            case G('kind_with_arg', [G('prekind_to_kind', [core]), G('lex_argmark_of'), G('math_term', [X('math') as formula])]):
                pass
            case _:
                return False



        # step 1: check if the formula is a set comprehension of the right form
        if len(formula.children) != 1:
            return False
        compr = formula.children[0]
        if not isinstance(compr, X) or compr.attrs.get('data-ftml-head') != 'https://mathhub.info?a=smglom/sets&p=mod&m=set&s=set comprehension':
            return False
        comprargs = get_function_arg_vals(compr)
        assert len(comprargs) == 3
        if not comprargs[0].equals(comprargs[1]):
            return False
        match comprargs[2]:
            case X('mtext', [G('term_is_term_stmt', [G('math_term', [X('math', [subj])]), G('quantified_nkind', [
                G('existential_quantification'), G('name_kind', [G('prekind_to_kind', [obj]), G('no_ident')])])])]):
                if not subj.equals(comprargs[0]):
                    return False
            case _:
                return False

        # step 2: check if the core refers to elementhood
        while isinstance(core, G) and core.node == {'property_prekind'}:
            core = core.children[0]
        if not isinstance(core, X) and core.attrs.get('data-ftml-head') != 'https://mathhub.info?a=smglom/sets&amp;p=mod&amp;m=set&amp;s=element':
            return False

        # Success!!! We can simplify
        parents = parent_dict(tree)
        parents.replace_node_in_parent(core, obj)
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


def get_args(node: X) -> dict[str, X]:
    result: dict[str, X] = {}

    def _recurse(n: X):
        if n != node and 'data-ftml-head' in n.attrs:
            return   # now args will be for children of n not node
        if 'data-ftml-arg' in n.attrs:
            result[n.attrs['data-ftml-arg']] = n
            return
        for child in n.children:
            if isinstance(child, X):
                _recurse(child)

    _recurse(node)
    return result


def is_identifier(node: X) -> bool:
    return node.attrs.get('data-ftml-term') == 'OMV' or \
        node.attrs.get('data-ftml-head', '').endswith('seq')   # TODO: This info is not exactly carried around


def get_introduction_locations(variable_tree: X, context: Node) -> list[Node]:
    assert variable_tree.attrs.get('data-ftml-head')
    # find first occurrence
    def _recurse(node: Node):
        if isinstance(node, X) and node.attrs.get('data-ftml-head') == variable_tree.attrs['data-ftml-head']:
            yield node
            return
        for child in node.children:
            yield from _recurse(child)

    return list(_recurse(context))

def get_unused_identifier(tree: Node, options: list[str]) -> str:
    for option in options:
        if not list(find_nodes(tree, lambda n: isinstance(n, XT) and n.text.strip() == option)):
            return option

    assert False


def locate_structure(name: str) -> Optional[X]:
    for sentence in SIMPLIFICATION_CTX.get(name, []):
        for tree in sentence.trees:
            for definiendum in find_nodes(tree, lambda n: isinstance(n, X) and n.attrs.get('data-ftml-definiendum') == name):
                parents = parent_dict(tree)
                defcore = definiendum
                while defcore and get_node_type(defcore) != 'DefCore':
                    defcore = parents.get_parent(defcore)
                if defcore is None:
                    continue
                assert isinstance(defcore, G)
                if defcore.node.startswith('define_nkind_as_nkind'):
                    named_kind = defcore.children[1]
                    while named_kind and not (isinstance(named_kind, G) and named_kind.node == 'name_kind'):
                        if len(named_kind.children) == 1:
                            named_kind = named_kind.children[0]
                        elif isinstance(named_kind, G):
                            if named_kind.node.startswith('such_that_named_kind'):
                                named_kind = named_kind.children[0]
                            else:
                                named_kind = None
                        else:
                            named_kind = None
                    if named_kind is None:
                        continue
                    name = named_kind.children[1]
                    assert isinstance(name, G)
                    if name.node == 'math_ident':
                        structure = name.children[0].children[0]
                        assert isinstance(structure, X)
                        if structure.attrs.get('data-ftml-head') == 'https://mathhub.info?a=smglom/sets&p=mod&m=cartesian-product&s=tuple':
                            return deepcopy(structure)
    return None


def variable_structure_expansion(variable_tree: X, context: Node) -> bool:
    print('-----------------------VARSTRUCTEXP----------------------------')
    intros = get_introduction_locations(variable_tree, context)
    parents = parent_dict(context)

    for intro in intros:
        parent = parents.get_parent(intro)
        assert parent is not None
        pp = parents.get_parent(parent)
        ppp = parents.get_parent(pp)
        if isinstance(parent, X) and parent.tag == 'math' and isinstance(pp, G) and pp.node == 'math_ident' and isinstance(ppp, G) and ppp.node == 'name_kind':
            if variable_tree.attrs['data-ftml-head'].endswith('seq'):   # todo: improve sequence recognition
                # if e_1, ..., e_n, then look for "sequence e_1, ..., e_n of foos" and make it "sequence e_1, ..., e_n of foos e_i"
                # can only expand if we have a sequence "of" something
                child = ppp.children[0]
                while True:
                    if not isinstance(child, G):
                        break
                    if child.node != 'kind_with_arg':
                        break
                    if child.children[1].node == 'lex_argmark_of':
                        # iterate downwards through terms and namedkinds until we find a `name_kind`
                        def _recurse(n: G) -> Optional[G]:
                            if get_node_type(n) not in {'Term', 'NamedKind'}:
                                return None
                            if n.node == 'name_kind':
                                return n
                            for child in n.children:
                                if isinstance(child, G):
                                    result = _recurse(child)
                                    if result is not None:
                                        return result
                            return None

                        namekind = _recurse(child.children[2])
                        if not namekind:
                            break
                        name = namekind.children[1]
                        assert isinstance(name, G)
                        if name.node == 'no_ident':
                            # introduce variable
                            newvar = deepcopy(variable_tree)
                            if newvar.attrs['data-ftml-head'].endswith('seq'):
                                # TODO: use unicode italics ijklmn
                                index = get_unused_identifier(context, [chr(119894 + i) for i in range(5)])
                                get_args(newvar)['1'].children[0] = X('mi', [XT(index)])
                            namekind.children[1] = G('math_ident', [X('math', [newvar])])
                            return True
                    break

                # If the previous didn't do anything, new plan:
                # Maybe we don't have `sequence [A] of [B]` but are in the `[B]` part
                # (this could be possible because in a previous step, the previous iteration may have introduced an identifier in [B])
                # Then we can try to now do the actual structure expansion
                prekind = ppp.children[0].children[0]
                while isinstance(prekind, G) and prekind.node == 'property_prekind':
                    prekind = prekind.children[1]

                formula = ppp.children[1]
                assert isinstance(formula, G)
                if formula.node == 'math_ident':
                    root = formula.children[0]
                    assert isinstance(root, X)
                    print('ROOT')
                    print(root)
                    if root.children[0].attrs.get('data-ftml-head') == variable_tree.attrs['data-ftml-head']:
                        print('A')
                        # have to assign structure
                        if isinstance(prekind, X) and prekind.attrs['data-ftml-term'] == 'OMID' and (structure := locate_structure(prekind.attrs['data-ftml-head'])):
                            print('FOUND STRUCTURE', structure)
                            # instantiate structure
                            index = get_args(root.children[0])['1']
                            instantiation_success = True
                            for v in get_args(structure).values():
                                if not v.children[0].attrs.get('data-ftml-term') == 'OMV':
                                    instantiation_success = False
                                    break
                                v.children = [X('msub', [v.children[0], deepcopy(index)])]

                            if instantiation_success:
                                root.children[0] = X('mrow', [
                                    X('mrow', [root.children[0]], attrs={'data-ftml-arg-mode': 'i', 'data-ftml-arg': '1'}),
                                    X('mrow', [X('mo', [XT(':=')])], attrs={'data-ftml-comp': ''}),
                                    X('mrow', [structure], attrs={'data-ftml-arg-mode': 'i', 'data-ftml-arg': '2'}),
                                ], attrs={'data-ftml-term': 'OMA', 'data-ftml-head': 'https://mathhub.info?a=smglom/mv&p=mod&m=defeq&s=definitional equation'})
                                return True
        elif pp.attrs.get('data-ftml-head') == 'https://mathhub.info?a=smglom/mv&p=mod&m=defeq&s=definitional equation'\
                and (args := get_args(pp)) and (head := args['1'].children[0]) and head.attrs.get('data-ftml-head') == variable_tree.attrs['data-ftml-head']\
                    and (index := get_args(head).get('1')) and (struct := args['2'].children[0]) and (struct.attrs.get('data-ftml-head') == 'https://mathhub.info?a=smglom/sets&p=mod&m=cartesian-product&s=tuple'):
            # already structure declared => can hoist a copy to replace the variable tree
            print('HERE', pp)
            struct = deepcopy(struct)

            def _recurse(x: Node):
                for i in range(len(x.children)):
                    child = x.children[i]
                    if child.equals(index):
                        x.children = x.children[:i] + deepcopy(
                            get_args(variable_tree)['1'].children
                        ) + x.children[i + 1:]
                    else:
                        _recurse(child)
            _recurse(struct)
            parents.replace_node_in_parent(variable_tree, struct)
            return True

            # break    # do not consider any other intros

    return False



def projection_simplification(tree: Node) -> bool:
    parents = parent_dict(tree)
    for projectionfn in find_nodes(tree, lambda n: isinstance(n, X) and n.tag == 'mrow' and n.attrs.get('data-ftml-head') == 'https://mathhub.info?a=smglom/sets&p=mod&m=cartesian-product&s=projectionFN'):
        application = parents.get_parent(parents.get_parent(projectionfn))
        assert isinstance(application, X)
        assert application.tag == 'mrow' and application.attrs.get('data-ftml-head') == 'http://mathhub.info?a=sTeX/meta-inf&m=Metatheory&s=apply'
        name = application.children

        args = get_args(application)
        assert '21' in args and '22' not in args
        main_arg = args['21']
        while 'data-ftml-arg' in main_arg.attrs:   # why twice?
            main_arg = main_arg.children[0]

        projectionval = get_args(args['1'].children[0])['1'].children[0]
        number = None
        if isinstance(projectionval, X) and projectionval.tag in {'mi', 'mn'}:
            child = projectionval.children[0]
            if isinstance(child, XT):
                if re.match(r'^[0-9]+$', child.text):
                    number = child.text

        if number is None:   # can only work with concrete numbers
            print('NO', projectionval)
            continue

        if main_arg.attrs.get('data-ftml-head') == 'https://mathhub.info?a=smglom/sets&p=mod&m=cartesian-product&s=tuple':
            # apply projection
            newval = get_args(main_arg)['1' + number].children[0]
            parents.replace_node_in_parent(application, newval)
            return True

        elif is_identifier(main_arg):
            if variable_structure_expansion(main_arg, tree):
                return True    # changed something -> have to re-run simplifications


        # else: complex expression => cannot do anything

    return False



SIMPLIFIER_T = Callable[[Node], bool]

# should be attempted in order, and (on success) be restarted from the beginning
SIMPLIFIERS: list[SIMPLIFIER_T] = [
    simplify_comprehension_plain,
    projection_simplification,
]


def basic_simplify(tree: Node) -> Node:
    """ "greedily" applies all simplifications """
    tree = deepcopy(tree)

    with details('Simplification process'): # ('Sentence: ' + linearize_tree(sentence.trees[0], input_doc.shell)):
        while True:
            push_sentence_tree(tree)
            changed = False
            for simplifier in SIMPLIFIERS:
                if simplifier(tree):
                    changed = True
                    break
            if not changed:
                break

    return tree
