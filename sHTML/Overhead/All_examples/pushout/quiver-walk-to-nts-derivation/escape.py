import pathlib
import re
import sys


for path in sys.argv[1:]:
    p = pathlib.Path(path)
    content = p.read_text()
    content = re.sub(r'&([amsp]=)', r'&amp;\1', content)
    content = re.sub(r'display>', r'display="block">', content)
    p.write_text(content)

