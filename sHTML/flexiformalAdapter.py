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


###----- Irrelevant Functions ---------------------------------------------------------------------------------------------------------------------------###
def make_sentence_GfConform(sentence: str) -> str:
    """Brings a normal sentence into a format, which is parsable by the generated grammar, which is used in the Grammatical Framework."""
    sentence_pp = sentence.replace("\\", "\\\\")
    sentence_pp = sentence_pp.strip()
    if sentence_pp.endswith(" ."):
        sentence_pp = sentence_pp[:-2]
    if len(sentence_pp) > 1 and sentence_pp[0].isupper():
        sentence_pp = sentence_pp[0].lower() + sentence_pp[1:]
    elif sentence_pp[0].isupper():
        sentence_pp = sentence_pp[0].lower()
    return sentence_pp

def getDefiniendumLink(sentence: str) -> str:
    return ""

#DEFINITION EXPANSION FUNCTIONS
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
            delete_tree_temp = gfxml.get_firstOuterNode(statement_tree, gfxml.get_firstOuterNode(statement_tree, gfxml.get_firstOuterNode(statement_tree, gfxml.get_firstOuterNode(statement_tree, delete_tree))))
            match delete_tree_temp:
                case gfxml.G('PredVP', [np, gfxml.G('UseComp', [gfxml.G('CompAP', [gfxml.G('PositA', delete_tree)])])]):
                    merged_tree = gfxml.tree_subst(statement_tree, delete_tree_temp, ADC_tree)
        
        elif (delete_tree.wrapfun == "WRAP_A") and (ADC_tree.node == "formula_NP"):
            # <adjective which is the definiendum> <noun>     =>     <noun> "such that" <definiens content>
            delete_tree_temp = gfxml.get_firstOuterNode(statement_tree, gfxml.get_firstOuterNode(statement_tree, gfxml.get_firstOuterNode(statement_tree, delete_tree)))
            match delete_tree_temp:
                case gfxml.G('DetCN', [R_DetQuant, gfxml.G('AdjCN', [gfxml.G('PositA', deletedTree), R_Noun])]):
                    new_tree = gfxml.G('DetCN', [R_DetQuant, gfxml.G('ApposCN', [gfxml.G('ApposCN', [gfxml.G('AdvCN', [R_Noun, gfxml.G('such_Adv', [])]), gfxml.G('DetNP', [gfxml.G('DetQuant', [gfxml.G('that_Quant', []), gfxml.G('NumSg')])])]), ADC_tree])])
                    merged_tree = gfxml.tree_subst(statement_tree, delete_tree_temp, new_tree)

    return merged_tree

def get_extendedVariables_tree(statement_tree):
    #TODO: Add Variable after Nouns, which are in relation to the definiendum
    return statement_tree

def get_alignedVariables_tree(definiens_content_tree, assignedVariables):
    for variable in assignedVariables:
        replaced_node = gfxml.xify(variable)
        replacement_node = gfxml.xify(assignedVariables[variable])
        definiens_content_tree = gfxml.tree_subst(definiens_content_tree, replaced_node, replacement_node)
        print("\nreplaced_node: " + str(replaced_node))
        print("\nreplacement_node: " + str(replacement_node))
    return definiens_content_tree

def defex(statement_htmlfile_path: str, definition_htmlfile_path: str):
    shell = initializeGfShell()

    #Parse the statement sentence
    PATH_gf_concrGrammar(statement_htmlfile_path)

    #definiendum
    definiendumLink = getDefiniendumLink(statement_htmlfile_path)

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
    print("\nassignedVariables: " + str(assignedVariables))
    for variable in assignedVariables:
        if not gfxml.tree_contains_node(statement_tree, gfxml.xify(assignedVariables[variable])):
            statement_tree = statement_tree_extendedVariables

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
###------------------------------------------------------------------------------------------------------------------------------------------------------###

def parseHtmltoTrees(shell: gf.GFShellRaw, htmlfile_path: str):
    #Returns all possible trees in an array
    input_shtml = gfxml.parse_shtml(htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    input_xs, input_string = gfxml.get_gfxml_string(input_shtml)
    input_sentences = gfxml.sentence_tokenize(input_string)
    for s in input_sentences:
        input_sentence_preprocessed = make_sentence_GfConform(s)
        print("\ninput_sentence_preprocessed: " + str(input_sentence_preprocessed))
        gf_ast = shell.handle_command(f'p "{input_sentence_preprocessed}"')
        print("\ninput_gf_ast: " + str(gf_ast))
        all_statement_trees = []
        for line in gf_ast.splitlines():
            #print("input_xs: " + str(input_xs))
            #print("line: " + str(line))
            statement_tree_temp = gfxml.build_tree(input_xs, line)
            all_statement_trees.append(statement_tree_temp)
        print("\nAmount of trees: " + str(len(all_statement_trees)))
        print("\nFirst tree: " + str(all_statement_trees[0]))
    return all_statement_trees

def linearizeTreeToString(shell: gf.GFShellRaw, tree):
    #Linearize definiens content
    recovery_info, gf_input = tree.to_gf()
    print("\ngf_input: " + str(gf_input))
    #print("\nrecovery_info: " + str(recovery_info))
    gf_lin = shell.handle_command(f'linearize {gf_input}')
    print("\ngf_lin: " + str(gf_lin))
    merged_sentence = gfxml.final_recovery(gf_lin, recovery_info)
    #print("\nmerged_sentence: " + str(merged_sentence))
    if len(merged_sentence) > 1 and merged_sentence[0].islower():
        merged_sentence = merged_sentence[0].upper() + merged_sentence[1:]
    elif merged_sentence[0].islower():
        merged_sentence = merged_sentence[0].upper()
    final_sentence = (merged_sentence.replace("\\\\", "\\")) + "."
    print("\nfinal_sentence: " + str(final_sentence))
    return final_sentence

#Initialization
def initializeGfShell():
    shell = gf.GFShellRaw(PATH_exe_gf)
    print(shell.handle_command(f"import {PATH_gf_concrGrammar}"))
    return shell

#Definition Expansion
def definitionExpansion(sentence: str, definition: str):
    return sentence

#Definition Reduction
def definitionReduction(sentence: str, definition: str):
    return sentence

#Comprehension Term Reduction
def comprehensionTermReduction(sentence: str, reduction: str):
    return sentence



def testExample(example_name):
    shell = initializeGfShell()
    with open("sHTML\Examples\examples.json", 'r') as file:
        examples = json.load(file)
    example = examples[example_name]
    trees = parseHtmltoTrees(shell, example["statement"])
    string = linearizeTreeToString(shell, trees[0])

testExample("E000")

#<m 3 > </m 3 > is  < 4 > positive </ 4 >  iff  < 5 > <m 6 > </m 6 > </ 5 >

#an  < 4 > element </ 4 >  <m 5 > </m 5 >  </ 3 >   < 6 >   < 7 >   < 8 > element </ 8 >  <m 9 > </m 9 > such that <m 10 > </m 10 > for some <m 11 > </m 11 >  </ 7 >   </ 6 >   < 12 >  a  < 13 > pair </ 13 >  <m 14 > </m 14 >