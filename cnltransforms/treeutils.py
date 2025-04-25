"""
Various utitilies for working with the trees.
"""

import dataclasses
import functools
import subprocess
from pathlib import Path
from typing import Optional, Callable, Iterator

import pgf

from cnltransforms.gfxml import Node, X, XT, G


@dataclasses.dataclass
class ParentInfo:
    parent: Node
    position: int


class ParentStructure(dict[Node, Optional[ParentInfo]]):
    def filter_parent(self, node: Node, filter: Callable[[Node], bool]) -> Optional[Node]:
        parent_info = self[node]
        while parent_info is not None:
            if filter(parent_info.parent):
                return parent_info.parent
            parent_info = self[parent_info.parent]
        return None

    def replace_node_in_parent(self, node: Node, new_node: Node):
        parent_info = self[node]
        if parent_info is None:
            raise ValueError('Node has no parent')
        parent_info.parent.children[parent_info.position] = new_node
        self[new_node] = parent_info
        del self[node]

    def get_parentinfo(self, node: Node, skip_X: bool = False) -> Optional[ParentInfo]:
        if not skip_X:
            return self[node]
        parent_info = self[node]
        while parent_info is not None and isinstance(parent_info.parent, X):
            parent_info = self[parent_info.parent]
        return parent_info

    def get_parent(self, node: Node, skip_X: bool = False) -> Optional[Node]:
        parent_info = self.get_parentinfo(node, skip_X)
        return parent_info.parent if parent_info is not None else None

    def get_parent_pos(self, node: Node, skip_X: bool = False) -> Optional[int]:
        parent_info = self.get_parentinfo(node, skip_X)
        return parent_info.position if parent_info is not None else None


def parent_dict(tree: Node) -> ParentStructure:
    result: dict[Node, Optional[ParentInfo]] = {tree: None}

    def _recurse(node: Node):
        for i, child in enumerate(node.children):
            if child in result:
                raise RuntimeError('Node occurs multiple times in tree')
            result[child] = ParentInfo(node, i)
            _recurse(child)

    _recurse(tree)

    return ParentStructure(result)


def find_nodes(root: Node, filter: Callable[[Node], bool], search_matches: bool = True) -> Iterator[Node]:
    if filter(root):
        yield root
        if not search_matches:
            return

    for child in root.children:
        yield from find_nodes(child, filter)


@functools.cache
def get_pgf():
    cnl_dir = (Path(__file__).parent.parent / 'cnl').absolute()
    pgf_file = cnl_dir / 'Top.pgf'

    if not pgf_file.exists() or any(
        pgf_file.stat().st_mtime < gf_file.stat().st_mtime
        for gf_file in cnl_dir.rglob('*.gf')
    ):
        print('(Re)compiling PGF')
        result = subprocess.run(['gf', '--make', 'TopEng.gf'], cwd=cnl_dir)
        if result.returncode:
            raise RuntimeError('GF compilation failed')

    return pgf.readPGF(str(pgf_file))


def get_node_type(node: Node) -> str:
    if isinstance(node, X):
        return f'<{node.tag}>'
    elif isinstance(node, XT):
        return '<text>'
    elif isinstance(node, G):
        return get_pgf().functionType(node.node).cat
    else:
        raise ValueError(f'Unexpected node type: {type(node)}')
