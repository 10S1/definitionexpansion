from pathlib import Path
from gfxml import *


def get_defining_document(uri) -> Path:
    # TODO: Implement this
    assert uri == 'http://mathhub.info/smglom/search/mod?admissible?admissible', 'Not implemented'
    return Path(__file__).parent / 'example-files' / 'admissible.en.xhtml'




def process_document(in_document: Path, out_document: Path, uri_to_be_expanded: str):
    shtml = parse_shtml(in_document)
    xs, string = get_gfxml_string(shtml)
    sentences = sentence_tokenize(string)
    print(string)
    print(47, xs[47])

    print(sentences)

    






if __name__ == '__main__':
    process_document(
            Path(__file__).parent / 'example-files' / 'astar-optimal.en.xhtml',
            Path('output.xhtml'),
            'http://mathhub.info/smglom/search/mod?admissible?admissible'
    )




