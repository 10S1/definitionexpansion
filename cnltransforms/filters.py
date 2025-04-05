"""
Code for removing "wrong" trees.
"""
from cnltransforms.gfxml import Node, X
from cnltransforms.treeutils import parent_dict, find_nodes, get_node_type


def definiendum_filter(
        trees: list[Node],
        remove_if_definiendum_not_in_defcore: bool = True,
        remove_if_no_definiendum_in_defcore: bool = True,
) -> list[Node]:
    """
    "X is even iff X is divisible by 2" could be a definition or a statement.
    That gives us two readings.
    If "even" is a definiendum, we can remove the statement reading.
    And if "even" is not a definiendum, we can remove the definition reading.
    """
    results: list[Node] = []
    for tree in trees:
        parents = parent_dict(tree)


        tree_ok = True

        if remove_if_definiendum_not_in_defcore:
            definienda = find_nodes(tree, lambda n: isinstance(n, X) and n.attrs.get('data-ftml-definiendum'), search_matches=True)

            for definiendum in definienda:
                p = parents.filter_parent(
                    definiendum,
                    lambda n: get_node_type(n) in {'DefCore', 'Stmt'}
                )
                if not p:
                    continue
                if get_node_type(p) == 'Stmt':
                    tree_ok = False
                    break

        if remove_if_no_definiendum_in_defcore:
            defcores = find_nodes(tree, lambda n: get_node_type(n) == 'DefCore', search_matches=True)
            for defcore in defcores:
                p = next(find_nodes(defcore, lambda n: isinstance(n, X) and n.attrs.get('data-ftml-definiendum')), None)
                if p is None:
                    tree_ok = False
                    break

        if tree_ok:
            results.append(tree)
            continue

    return results





