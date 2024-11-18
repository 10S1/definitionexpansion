###----- Imports --------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
import json
import random
import string
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
PATH_gf_concrGrammar = "definitionexpansion\sHTML\Grammar\BaseGrammar_concr.gf"
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

def get_alignedCategories_tree(shell: gf.GFShellRaw, IN_string_supposed: str, IN_tree_actual: str):
    cat_supposed = "" # get_Cat_of_String(shell, IN_string_supposed)
    cat_actual = IN_tree_actual
    if cat_supposed != cat_actual:
        match cat_supposed, cat_actual:
            case "N", "V":
                string_actual = "" #TODO

            #TODO: All the other cases...
    else:
        tree_actual = IN_tree_actual
    return tree_actual

def get_extendedVariables_tree():
    return None

def get_alignedVariables_tree(statement_tree, statement_tree_extendedVariables, assignedVariables):
    return None

def main(statement_htmlfile_path: str, definition_htmlfile_path: str, definiendum: str):
    #Initialize GF shell
    shell = gf.GFShellRaw(PATH_exe_gf)
    print(shell.handle_command(f"import {PATH_gf_concrGrammar}"))


    ### STATEMENT ###
    #Parse the statement sentence
    print("PFAD: " + str(statement_htmlfile_path))
    statement_shtml = gfxml.parse_shtml(statement_htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    statement_xs, statement_string = gfxml.get_gfxml_string(statement_shtml)
    statement_sentences = gfxml.sentence_tokenize(statement_string)
    for s in statement_sentences:
        print(s)
        gf_ast = shell.handle_command(f'p "{s}"')
        print(gf_ast)
        statement_tree = gfxml.build_tree(statement_xs, gf_ast)
        print(statement_tree)


    ### DEFINITION ###
    #Parse the definition sentence
    definition_shtml = gfxml.parse_shtml(definition_htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    definition_xs, definition_string = gfxml.get_gfxml_string(definition_shtml)
    definition_sentences = gfxml.sentence_tokenize(definition_string)
    for s in definition_sentences:
        print(s)
        gf_ast = shell.handle_command(f'p "{s}"')
        print(gf_ast)
        definition_tree = gfxml.build_tree(definition_xs, gf_ast)
        print(definition_tree)

    #Extract the definiens content out of the definition sentence
    definiens_content_tree = get_definiensContent(definiendum, definition_tree)


    ##########-##########-##########-##########-##########


    #IF NECESSARY: Align variables
    #Rename variables in definiens content tree
    #TODO

    #Assign variables and introduce variables in statement tree (if necessary)
    statement_tree_extendedVariables = get_extendedVariables_tree()
    assignedVariables = variableAssigner.get_assignedVariables(statement_tree_extendedVariables, definition_tree, definiens_content_tree)
    for var in assignedVariables:
        if var["replacedVar"] not in definiens_content_tree:
            statement_tree = statement_tree_extendedVariables

    #Modify definiens content tree 
    definiens_content_tree = get_alignedVariables_tree(statement_tree, statement_tree_extendedVariables, assignedVariables) #TODO

    #Align the category of the definiens content to the category of the definiendum
    merged_tree = get_alignedCategories_tree(statement_tree, definiens_content_tree, definiendum) #TODO


    ##########-##########-##########-##########-#########


    #Linearize definiens content
    recovery_info, gf_input = merged_tree.to_gf()
    print(gf_input)
    gf_lin = shell.handle_command(f'linearize {gf_input}')
    print(gf_lin)
    merged_sentence = gfxml.final_recovery(gf_lin, recovery_info)
    print(merged_sentence)
    return merged_sentence





def testE001(example_name):
    with open("definitionexpansion\\sHTML\\Examples\\examples.json", 'r') as file:
        examples = json.load(file)
    example = examples[example_name]
    statement_htmlfile_path = example["statement"]
    definition_htmlfile_path = example["definition"]
    definiendum = example["definiendum"]
    main(statement_htmlfile_path, definition_htmlfile_path, definiendum)

testE001("E001")