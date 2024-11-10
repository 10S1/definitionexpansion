import gfxml
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Resources')))
import gf
from pathlib import Path
import json
import shutil


###----- Paths ------------------------------------------------------------------------------------------------------------------------------------------###
PATH_exe_gf = shutil.which('gf')
if PATH_exe_gf is None:
    print("ERROR: Path to gf.exe not found. \nCheck whether the Grammatical Framework is installed and the environment variable is set.")
PATH_gf_concrGrammar = "definitionexpansion\sTeX\Grammar\BaseGrammar_concr.gf"
###------------------------------------------------------------------------------------------------------------------------------------------------------###

def lowercase_first_letter(s: str) -> str:
    if s and s[0].isupper():
        return s[0].lower() + s[1:]
    return s
def uppercase_first_letter(s: str) -> str:
    if s and s[0].islower():
        return s[0].upper() + s[1:]
    return s

def linearizeTree(shell: gf.GFShellRaw, tree) -> str:
    cmd_linearize = 'linearize ' + str(tree)
    linearizedTree = shell.handle_command(cmd_linearize)
    res_sentence = uppercase_first_letter(linearizedTree)
    return res_sentence

def get_definiensContent(definiendum, definition_tree):
    match definition_tree:
        #TODO: What does definiens node look like?
        case gfxml.G(_, [gfxml.X(_, [gfxml.G('john') as g], _), _]):
            #g.node = 'mary'
            return ""
    for child in definition_tree:
        definiensContent_tree = get_definiensContent(definiendum, child)
        if definiensContent_tree != None:
            return definiensContent_tree
    return None

def get_Cat_of_String(shell: gf.GFShellRaw, IN_string: str) -> str:
    #TODO: How to add PlaceholderCat in RGL?
    return ""

def get_alignedCategories_tree(shell: gf.GFShellRaw, IN_string_supposed: str, IN_tree_actual: str):
    cat_supposed = get_Cat_of_String(shell, IN_string_supposed)
    cat_actual = IN_tree_actual
    if cat_supposed != cat_actual:
        match cat_supposed, cat_actual:
            case "N", "V":
                string_actual = "" #TODO

            #TODO: All the other cases...
    else:
        tree_actual = IN_tree_actual
    return tree_actual

def get_alignedVariables_tree():
    return ""

def main(statement_htmlfile_path: str, definition_htmlfile_path: str, definiendum: str):
    #Initialize GF shell
    shell = gf.GFShellRaw(PATH_exe_gf)
    print(shell.handle_command(f"import {PATH_gf_concrGrammar}"))

    #Parse the definition sentence
    definition_shtml = gfxml.parse_shtml(definition_htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    xs, string = gfxml.get_gfxml_string(definition_shtml)
    sentences = gfxml.sentence_tokenize(string)
    for s in sentences:
        print(s)
        gf_ast = shell.handle_command(f'p "{s}"')
        print(gf_ast)
        definition_tree = gfxml.build_tree(xs, gf_ast)
        print(definition_tree)

    #Extract the definiens content out of the definition sentence
    definiens_content_tree = get_definiensContent(definiendum, definition_tree)

    #If necessary: Modify definiens content tree
    #Align the category of the definiens content to the category of the definiendum
    definiens_content_tree = get_alignedCategories_tree(shell, definiendum, definiens_content_tree)
    #Align variable names
    definiens_content_tree = get_alignedVariables_tree(definiens_content_tree) #TODO

    #Linearize definiens content
    recovery_info, gf_input = definiens_content_tree.to_gf()
    print(gf_input)
    gf_lin = shell.handle_command(f'linearize {gf_input}')
    print(gf_lin)
    ie_sentence = gfxml.final_recovery(gf_lin, recovery_info)
    print(ie_sentence)

    #In the statement: Replace "<definiendum>" by "<definiendum> (i.e. XYZYX)"
    #<span shtml:notationid="" shtml:head="http://mathhub.info/smglom/algebra/mod?monoid?monoid" shtml:term="OMID" shtml:sourceref="http://mathhub.info/smglom/algebra/mod/ring.en.tex#866.24.5:876.24.15" class="rustex-contents"><span style="display:none;" shtml:visible="false" class="rustex-contents"></span><span shtml:comp="http://mathhub.info/smglom/algebra/mod?monoid?monoid" class="rustex-contents">monoid</span><span style="display:none;" shtml:visible="false" class="rustex-contents"></span></span>
        #Parse the definition sentence
    statement_shtml = gfxml.parse_shtml(statement_htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    xs, statement_sentences = gfxml.get_gfxml_string(statement_shtml)
    definiendum_part = "" #TODO: How to get the definiendum part?
    new_statement_sentence = statement_sentences.replace(definiendum_part, definiendum_part + "(i.e. " + ie_sentence + ")")
    return new_statement_sentence

def test(example_name):
    examples = json.loads("definitionexpansion\\sHTML\\Examples\\examples.json")
    example = examples[example_name]
    statement_htmlfile_path = example["statement"]
    definition_htmlfile_path = example["definition"]
    definiendum = example["definiendum"]
    main(statement_htmlfile_path, definition_htmlfile_path, definiendum)

test("E001")