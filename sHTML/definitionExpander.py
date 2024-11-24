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
    #res_sentence = uppercase_first_letter(linearizedTree)
    return linearizedTree #res_sentence

def get_definiensContent(definiendum, tree):
    if isinstance(tree, gfxml.X) and tree.tag == 'span':
        attrs = tree.attrs
        if ("data-definiens-of" in attrs) and (attrs["data-definiens-of"] == definiendum):
            return tree
        for child in tree.children:
            definiensContent_tree = get_definiensContent(definiendum, child)
            if definiensContent_tree is not None:
                return definiensContent_tree
            
    elif isinstance(tree, gfxml.G):
        for child in tree.children:
            definiensContent_tree = get_definiensContent(definiendum, child)
            if definiensContent_tree is not None:
                return definiensContent_tree
            
    return None


def get_deleteTree(definiendum, tree):
    if isinstance(tree, gfxml.X) and tree.tag == 'span':
        attrs = tree.attrs
        if ("data-symref" in attrs) and (attrs["data-symref"] == definiendum):
            return tree
        for child in tree.children:
            delete_tree = get_deleteTree(definiendum, child)
            if delete_tree is not None:
                return delete_tree

    elif isinstance(tree, gfxml.G):
        for child in tree.children:
            delete_tree = get_deleteTree(definiendum, child)
            if delete_tree is not None:
                return delete_tree
            
    return None

def rename_vars(definiens_content_tree, statement_tree):
    #TODO: Wie kann ich innerhalb von Tag-Nodes überhaupt einzelne Variablen erkennen?
    return definiens_content_tree

def get_merged_tree(statement_tree, definiens_content_tree, definiendum):
    deleteTree = get_deleteTree(definiendum, statement_tree)
    print("\ndeletedTree: " + str(deleteTree))
    return definiens_content_tree

def get_extendedVariables_tree(statement_tree):
    #TODO: Add Variable after Nouns, which are in relation to the definiendum
    return statement_tree

def get_alignedVariables_tree(definition_tree, assignedVariables):
    #TODO: Replace variables/tags through their assigned variables/tags
    return definition_tree

def main(statement_htmlfile_path: str, definition_htmlfile_path: str, definiendum: str):
    #Initialize GF shell
    shell = gf.GFShellRaw(PATH_exe_gf)
    print(shell.handle_command(f"import {PATH_gf_concrGrammar}"))


    ########## PROCESS INPUT #####################################################################################
    ### STATEMENT ###
    #Parse the statement sentence
    statement_shtml = gfxml.parse_shtml(statement_htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    statement_xs, statement_string = gfxml.get_gfxml_string(statement_shtml)
    print("\nstatement_xs: " + str(statement_xs))
    statement_sentences = gfxml.sentence_tokenize(statement_string)
    for s in statement_sentences:
        print("\ns: " + str(s))
        s_preprocessed = make_sentence_GfConform(s)
        print("\ns_preprocessed: " + str(s_preprocessed))
        gf_ast = shell.handle_command(f'p "{s_preprocessed}"')
        #print("gf_ast: " + str(gf_ast))
        all_statement_trees = []
        for line in gf_ast.splitlines():
            #print("line: " + str(line))
            statement_tree_temp = gfxml.build_tree(statement_xs, line)
            all_statement_trees.append(statement_tree_temp)
        statement_tree = all_statement_trees[0] #For now... TODO: Go through all trees. But which one to choose?
        print("\nstatement_tree: " + str(statement_tree))
        print()

    ### DEFINITION ###
    #Parse the definition sentence
    definition_shtml = gfxml.parse_shtml(definition_htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    definition_xs, definition_string = gfxml.get_gfxml_string(definition_shtml)
    print("\ndefinition_xs: " + str(definition_xs))
    definition_sentences = gfxml.sentence_tokenize(definition_string)

    for s in definition_sentences:
        print("\ns: " + str(s))
        s_preprocessed = make_sentence_GfConform(s)
        print("\ns_preprocessed: " + str(s_preprocessed))
        gf_ast = shell.handle_command(f'p "{s_preprocessed}"')
        #print("gf_ast: " + str(gf_ast))
        all_definition_trees = []
        for line in gf_ast.splitlines():
            #print("line: " + str(line))
            definition_tree_temp = gfxml.build_tree(definition_xs, line)
            all_definition_trees.append(definition_tree_temp)
        definition_tree = all_definition_trees[0] #For now... TODO: Go through all trees. But which one to choose?
        print("\ndefinition_tree: " + str(definition_tree))

    #Extract the definiens content out of the definition sentence
    definiens_content_tree = get_definiensContent(definiendum, definition_tree)
    if definiens_content_tree == None: print("ERROR: No definiens_content_tree found in the definition sentence.")
    print("\ndefiniens_content_tree: " + str(definiens_content_tree))
    ##############################################################################################################



    ########## MERGE TREES #######################################################################################
    #IF NECESSARY: Align variables
    #Rename variables in definiens content tree
    definiens_content_tree = rename_vars(definiens_content_tree, statement_tree) #TODO: Does not need the trees but the tag contents

    #Assign variables and introduce variables in statement tree (if necessary)
    statement_tree_extendedVariables = get_extendedVariables_tree(statement_tree) #TODO
    assignedVariables = variableAssigner.get_assignedVariables(statement_tree_extendedVariables, definition_tree, definiens_content_tree) #TODO
    for var in assignedVariables:
        if var["replacedVar"] not in definiens_content_tree:
            statement_tree = statement_tree_extendedVariables

    #Modify definiens content tree 
    definiens_content_tree = get_alignedVariables_tree(statement_tree, assignedVariables) #TODO

    #Align the category of the definiens content to the category of the definiendum
    merged_tree = get_merged_tree(statement_tree, definiens_content_tree, definiendum) #TODO
    print("\nmerged_tree: " + str(merged_tree))
    ##############################################################################################################



    ########## CREATE OUTPUT #####################################################################################
    #Linearize definiens content
    recovery_info, gf_input = merged_tree.to_gf()
    print("\ngf_input: " + str(gf_input))
    print("\nrecovery_info: " + str(recovery_info))
    gf_lin = shell.handle_command(f'linearize {gf_input}')
    print("\ngf_lin: " + str(gf_lin))
    merged_sentence = gfxml.final_recovery(gf_lin, recovery_info)
    print("\nmerged_sentence: " + str(merged_sentence))
    final_sentence = postprocessSentence(merged_sentence)
    print("\nfinal_sentence: " + str(final_sentence))
    ##############################################################################################################


    return final_sentence





def testE001(example_name):
    with open("sHTML\Examples\examples.json", 'r') as file:
        examples = json.load(file)
    example = examples[example_name]
    statement_htmlfile_path = example["statement"]
    definition_htmlfile_path = example["definition"]
    definiendum = example["definiendum"]
    main(statement_htmlfile_path, definition_htmlfile_path, definiendum)

testE001("E001")