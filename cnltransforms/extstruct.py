from pathlib import Path

from lxml import etree

from cnltransforms.document import get_shell
from cnltransforms.gfxml import parse_shtml


class ExtStruct:
    def __init__(self, path: Path):
        self.path = path

        self.shell = get_shell(path.name.split('.')[-2])
        self.shtml = parse_shtml(path)

        self.assignments: dict[str, etree._Element] = {}

        for asgnmtn in self.shtml.xpath('//mrow[@data-ftml-assign]'):
            symbol = asgnmtn.get('data-ftml-assign')
            assert len(asgnmtn.children) == 1
            self.assignments[symbol] = asgnmtn.children[0]


if __name__ == '__main__':
    import sys

    path = Path(sys.argv[1])
    extstruct = ExtStruct(path)
