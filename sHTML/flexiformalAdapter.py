#Definition Expansion
#

#Definition Reduction
#

#Comprehension Term Reduction
#


###----- Imports --------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
import json
import regex as re
import shutil
from pathlib import Path
import os
import sys
from typing import List, Any, Tuple, Dict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Resources')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../gfxml')))
import gf
import gfxml
import variableAssigner
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Paths ------------------------------------------------------------------------------------------------------------------------------------------###
PATH_exe_gf = shutil.which('gf')
if PATH_exe_gf is None:
    print("ERROR: Path to gf.exe not found. \nCheck whether the Grammatical Framework is installed and the environment variable is set.")
PATH_gf_concrGrammar = "sHTML\Grammar\BaseGrammar_concr.gf"
###------------------------------------------------------------------------------------------------------------------------------------------------------###

def lowercase_first_letter(s: str) -> str:
    if s and s[0].isupper():
        return s[0].lower() + s[1:]
    return s
def uppercase_first_letter(s: str) -> str:
    if s and s[0].islower():
        return s[0].upper() + s[1:]
    return s
def make_sentence_GfConform(sentence: str) -> str:
    """Brings a normal sentence into a format, which is parsable by the generated grammar, which is used in the Grammatical Framework."""
    sentence_pp = sentence.replace("\\", "\\\\")
    sentence_pp = sentence_pp.strip()
    if sentence_pp.endswith(" ."):
        sentence_pp = sentence_pp[:-2]
    sentence_pp = lowercase_first_letter(sentence_pp)
    return sentence_pp
def postprocessSentence(sentence: str) -> str:
    """Brings a sentence, which is in a format, which is parsable by the Grammatical Framework, back to a normal format."""
    sentence = (uppercase_first_letter(sentence).replace("\\\\", "\\")) + "."
    return sentence

def linearizeTree(shell: gf.GFShellRaw, tree) -> str:
    cmd_linearize = 'linearize ' + str(tree)
    linearizedTree = shell.handle_command(cmd_linearize)
    return linearizedTree


def main(statement_htmlfile_path: str, definition_htmlfile_path: str, definiendum: str):
    #Initialize GF shell
    shell = gf.GFShellRaw(PATH_exe_gf)
    print(shell.handle_command(f"import {PATH_gf_concrGrammar}"))

    #Parse the statement sentence
    statement_shtml = gfxml.parse_shtml(statement_htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    statement_xs, statement_string = gfxml.get_gfxml_string(statement_shtml)
    #print("\nstatement_xs: " + str(statement_xs))
    statement_sentences = gfxml.sentence_tokenize(statement_string)
    for s in statement_sentences:
        #print("\ns: " + str(s))
        statement_sentence_preprocessed = make_sentence_GfConform(s)
        print("\nstatement_sentence_preprocessed: " + str(statement_sentence_preprocessed))
        gf_ast = shell.handle_command(f'p "{statement_sentence_preprocessed}"')
        print("gf_ast: " + str(gf_ast))
        #print("gf_ast: " + str(gf_ast))
        all_statement_trees = []
        for line in gf_ast.splitlines():
            #print("line: " + str(line))
            print("statement_xs: " + str(statement_xs))
            print("line: " + str(line))
            statement_tree_temp = gfxml.build_tree(statement_xs, line)
            all_statement_trees.append(statement_tree_temp)
        statement_tree = all_statement_trees[0] #For now... TODO: Go through all trees. But which one to choose?
        print("\nstatement_tree: " + str(statement_tree))


    ########## CREATE OUTPUT #####################################################################################
    #Linearize definiens content
    recovery_info, gf_input = statement_tree.to_gf()
    print("\ngf_input: " + str(gf_input))
    #print("\nrecovery_info: " + str(recovery_info))
    gf_lin = shell.handle_command(f'linearize {gf_input}')
    print("\ngf_lin: " + str(gf_lin))
    merged_sentence = gfxml.final_recovery(gf_lin, recovery_info)
    #print("\nmerged_sentence: " + str(merged_sentence))
    final_sentence = postprocessSentence(merged_sentence)
    print("\nfinal_sentence: " + str(final_sentence))
    ##############################################################################################################


    return final_sentence





def testExample(example_name):
    with open("sHTML\Examples\examples.json", 'r') as file:
        examples = json.load(file)
    example = examples[example_name]
    statement_htmlfile_path = example["statement"]
    definition_htmlfile_path = example["definition"]
    definiendum = example["definiendum"]
    main(statement_htmlfile_path, definition_htmlfile_path, definiendum)

testExample("E000")

#<m 3 > </m 3 > is  < 4 > positive </ 4 >  iff  < 5 > <m 6 > </m 6 > </ 5 >

#an  < 4 > element </ 4 >  <m 5 > </m 5 >  </ 3 >   < 6 >   < 7 >   < 8 > element </ 8 >  <m 9 > </m 9 > such that <m 10 > </m 10 > for some <m 11 > </m 11 >  </ 7 >   </ 6 >   < 12 >  a  < 13 > pair </ 13 >  <m 14 > </m 14 >