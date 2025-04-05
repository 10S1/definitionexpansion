import functools
import re
import shutil
from pathlib import Path
from typing import Optional, Callable

from Resources.gf import GFShellRaw
from cnltransforms.gfxml import parse_shtml, get_gfxml_string, sentence_tokenize, Node, linearize_mtree_contents, \
    final_recovery
from cnltransforms.gfxml import build_tree


@functools.cache
def get_shell(lang: str):
    shell = GFShellRaw(shutil.which('gf'))
    gflang = {'de': 'Ger', 'en': 'Eng'}[lang]
    path = Path(__file__).parent.parent / 'cnl' / f'Top{gflang}.gf'
    result = shell.handle_command(f'i {path.absolute()}')
    assert not result, result
    return shell


def no_filter(input: list[Node]) -> list[Node]:
    return input


class Document:
    def __init__(self, path: Path, readings_filter: Callable[[list[Node]], list[Node]] = no_filter):
        self.path = path
        self.shell = get_shell(path.name.split('.')[-2])
        self.shtml = parse_shtml(path)
        self.recovery_info, self.string = get_gfxml_string(self.shtml)

        sentence_strs = sentence_tokenize(self.string)
        self.sentences = [
            Sentence(sentence_str, self.shell, self.recovery_info, readings_filter)
            for sentence_str in sentence_strs
        ]


class Sentence:
    def __init__(self, string: str, shell: GFShellRaw, recovery_info,
                 readings_filter: Callable[[list[Node]], list[Node]] = no_filter):
        self.string = string
        self.shell = shell
        self.recovery_info = recovery_info

        self.trees = []
        self.parser_error = None

        # a few quick pre-processing hacks
        # lower-case first letter
        first_letter = re.search(r'[a-zA-Z]', string)
        if first_letter and not (
            # actually, not necessary as `m` is already lower-case...
            first_letter.string == 'm' and first_letter.pos > 0 and string[first_letter.pos - 1] == '<'  # math
        ):
            string = string[:first_letter.start()] + string[first_letter.start()].lower() + string[first_letter.start()+1:]
        # put space before last period
        string = re.sub(r'\.([0-9m<>/]*)', r' . \1', string)

        cmd = f'p -cat=Sentence "{string}"'
        # print(f'Command: {cmd}')
        shell_output = shell.handle_command(cmd)
        assert shell_output

        if shell_output.startswith('The parser failed at token'):
            self.parser_error = shell_output
            print(f'Parser error for "{string}": {shell_output}')
            print(f'Command: {cmd}')
            return

        tree_candidates: list[Node] = [
            build_tree(recovery_info, tree_str)
            for tree_str in shell_output.split('\n')
        ]
        self.trees = readings_filter(tree_candidates)
        # print(self.trees)


def linearize_tree(tree: Node, shell: GFShellRaw) -> str:
    linearize_mtree_contents(lambda s: shell.handle_command(f'linearize {s}'), tree)
    recovery_info, gf_input = tree.to_gf()
    gf_lin = shell.handle_command(f'linearize {gf_input}')
    return final_recovery(gf_lin, recovery_info)
