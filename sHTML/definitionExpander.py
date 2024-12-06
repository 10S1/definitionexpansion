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

def get_outerNode(tree, subtree):
    if isinstance(tree, gfxml.G) or isinstance(tree, gfxml.X):
        if subtree in tree.children:
            return tree
        else:
            for child in tree.children:
                outerTree = get_outerNode(child, subtree)
                if outerTree is not None:
                    return outerTree
    return None

def replaceNode(tree, removeNode, addNode):
    if tree == removeNode:
        return addNode
    elif isinstance(tree, gfxml.X) or isinstance(tree, gfxml.G):
        new_children = []
        for child in tree.children:
            new_children.append(replaceNode(child, removeNode, addNode))
        tree.children = new_children
        return tree
    else:
        return tree

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
    merged_tree = None
    #Get actual definiens content tree (= definiens content tree without wrapper)
    ADC_tree = definiens_content_tree.children[0].children[0]
    print("\nADC_tree: " + str(ADC_tree))
    #Get the subtree from the statement tree, which needs to be removed (= the reference to the definiendum)
    delete_tree = get_deleteTree(definiendum, statement_tree)
    print("\ndelete_tree: " + str(delete_tree))

    #Replace the delete_tree by the ADC_tree. Modifications necessary, if categories do not align.
    if isinstance(delete_tree, gfxml.X) and isinstance(definiens_content_tree, gfxml.X):
        print("delete_tree.wrapfun: " + str(delete_tree.wrapfun))
        print("definiens_content_tree.wrapfun: " + str(definiens_content_tree.wrapfun))

        #Same category
        #if (delete_tree.wrapfun == definiens_content_tree.wrapfun): #Stimmt das überhaupt?
        #    merged_tree = statement_tree.replace(delete_tree, ADC_tree)
        
        if (delete_tree.wrapfun == "WRAP_A") and (ADC_tree.node == "PredVP"):
            # "is" <adjective which is the definiendum>     =>     <definiens content>
            delete_tree_temp = get_outerNode(statement_tree, get_outerNode(statement_tree, get_outerNode(statement_tree, get_outerNode(statement_tree, delete_tree))))
            match delete_tree_temp:
                case gfxml.G('PredVP', [np, gfxml.G('UseComp', [gfxml.G('CompAP', [gfxml.G('PositA', delete_tree)])])]):
                    merged_tree = replaceNode(statement_tree, delete_tree_temp, ADC_tree)
        
        elif (delete_tree.wrapfun == "WRAP_A") and (ADC_tree.node == "formula_NP"):
            # <adjective which is the definiendum> <noun>     =>     <noun> "such that" <definiens content>
            delete_tree_temp = get_outerNode(statement_tree, get_outerNode(statement_tree, get_outerNode(statement_tree, delete_tree)))
            match delete_tree_temp:
                case gfxml.G('DetCN', [R_DetQuant, gfxml.G('AdjCN', [gfxml.G('PositA', deletedTree), R_Noun])]):
                    new_tree = gfxml.G('DetCN', [R_DetQuant, gfxml.G('ApposCN', [gfxml.G('ApposCN', [gfxml.G('AdvCN', [R_Noun, gfxml.G('such_Adv', [])]), gfxml.G('DetNP', [gfxml.G('DetQuant', [gfxml.G('that_Quant', []), gfxml.G('NumSg')])])]), ADC_tree])])
                    merged_tree = replaceNode(statement_tree, delete_tree_temp, new_tree)

    return merged_tree

def get_extendedVariables_tree(statement_tree):
    #TODO: Add Variable after Nouns, which are in relation to the definiendum
    return statement_tree

def get_alignedVariables_tree(definiens_content_tree, assignedVariables):
    for variable in assignedVariables:
        node = ""
        node_new = node.replace(variable, assignedVariables[variable])
    return definiens_content_tree
    #TODO: Replace variables/tags through their assigned variables/tags

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
    #print("\nstatement_xs: " + str(statement_xs))
    statement_sentences = gfxml.sentence_tokenize(statement_string)
    for s in statement_sentences:
        #print("\ns: " + str(s))
        statement_sentence_preprocessed = make_sentence_GfConform(s)
        print("\nstatement_sentence_preprocessed: " + str(statement_sentence_preprocessed))
        gf_ast = shell.handle_command(f'p "{statement_sentence_preprocessed}"')
        #print("gf_ast: " + str(gf_ast))
        all_statement_trees = []
        for line in gf_ast.splitlines():
            #print("line: " + str(line))
            statement_tree_temp = gfxml.build_tree(statement_xs, line)
            all_statement_trees.append(statement_tree_temp)
        statement_tree = all_statement_trees[0] #For now... TODO: Go through all trees. But which one to choose?
        print("\nstatement_tree: " + str(statement_tree))

    ### DEFINITION ###
    #Parse the definition sentence
    definition_shtml = gfxml.parse_shtml(definition_htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    definition_xs, definition_string = gfxml.get_gfxml_string(definition_shtml)
    #print("\ndefinition_xs: " + str(definition_xs))
    definition_sentences = gfxml.sentence_tokenize(definition_string)

    for s in definition_sentences:
        #print("\ns: " + str(s))
        definition_sentence_preprocessed = make_sentence_GfConform(s)
        print("\ndefinition_sentence_preprocessed: " + str(definition_sentence_preprocessed))
        gf_ast = shell.handle_command(f'p "{definition_sentence_preprocessed}"')
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
    #for var in assignedVariables: TODO
    #    if assignedVariables[var] not in statement_tree:
    #        statement_tree = statement_tree_extendedVariables
    print("\nassignedVariables: " + str(assignedVariables))

    #Modify definiens content tree 
    definiens_content_tree = get_alignedVariables_tree(definiens_content_tree, assignedVariables) #TODO

    #Align the category of the definiens content to the category of the definiendum
    merged_tree = get_merged_tree(statement_tree, definiens_content_tree, definiendum) #TODO
    print("\nmerged_tree: " + str(merged_tree))
    ##############################################################################################################



    ########## CREATE OUTPUT #####################################################################################
    #Linearize definiens content
    recovery_info, gf_input = merged_tree.to_gf()
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

testExample("E002")