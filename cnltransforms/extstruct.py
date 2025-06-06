from pathlib import Path

from lxml import etree

from cnltransforms.document import get_shell
from cnltransforms.filters import default_readings_filter
from cnltransforms.gf import handle_parse_output
from cnltransforms.gfxml import parse_shtml, X, xify, parse_mtext_contents
from cnltransforms.htmldocu import push_tree, push_html


class ExtStruct:
    def __init__(self, path: Path):
        self.path = path

        self.shell = get_shell(path.name.split('.')[-2])
        self.shtml = parse_shtml(path)

        self.assignments: dict[str, etree._Element] = {}

        for asgnmtn in self.shtml.xpath('//mrow[@data-ftml-assign]'):
            symbol = asgnmtn.get('data-ftml-assign')
            assert len(asgnmtn.getchildren()) == 1
            self.assignments[symbol] = asgnmtn.getchildren()[0]

    def get_assignment_as_formula(self, symbol: str) -> list[X]:
        result : list[X] = []
        push_html('<h2>Assignment</h2>')
        for r in default_readings_filter(parse_mtext_contents(
            lambda s : handle_parse_output(get_shell(self.path.name.split('.')[-2]).handle_command(
                f'parse -cat=Stmt "{s}"'
            )),
            xify(self.assignments[symbol])
        )):
            push_tree(r)
            assert isinstance(r, X)
            result.append(r)

        return result


if __name__ == '__main__':
    import sys

    path = Path(sys.argv[1])
    extstruct = ExtStruct(path)
    print(extstruct.assignments)
