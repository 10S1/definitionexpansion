###----- Imports --------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
import difflib
import json
import unicodedata
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



###----- Paths ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
PATH_exe_gf = shutil.which('gf')
if PATH_exe_gf is None:
    print("ERROR: Path to gf.exe not found. \nCheck whether the Grammatical Framework is installed and the environment variable is set.")
PATH_gf_concrGrammar = "sHTML\Grammar\BaseGrammar_concr.gf"
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Irrelevant Functions -------------------------------------------------------------------------------------------------------------------------------------------------------------###
def make_sentence_GfConform(sentence: str) -> str:
    """Brings a normal sentence into a format, which is parsable by the generated grammar, which is used in the Grammatical Framework."""
    sentence_pp = sentence.replace("\\", "\\\\")
    sentence_pp = sentence_pp.strip()
    if sentence_pp.endswith(" ."):
        sentence_pp = sentence_pp[:-2]
    if sentence_pp.endswith(">."):
        sentence_pp = sentence_pp[:-1]
    if len(sentence_pp) > 1 and sentence_pp[0].isupper():
        sentence_pp = sentence_pp[0].lower() + sentence_pp[1:]
    elif sentence_pp[0].isupper():
        sentence_pp = sentence_pp[0].lower()
    return sentence_pp

def getDefiniendumLink(shtml_path: str) -> str:
    result = "" 
    with open(shtml_path, "r", encoding="utf-8") as file:
        shtml_content = file.read()
    #print("\nshtml_content: " + str(shtml_content))
    match = re.search(r'data-ftml-definiendum="([^"]+)"', shtml_content)
    if match: result = match.group(1)
    return result.replace("&amp;", "&")

def get_definiensContent(definiendum_link, definition_tree):
    if isinstance(definition_tree, gfxml.X) and definition_tree.tag == 'span':
        attrs = definition_tree.attrs
        if ("data-ftml-definiens" in attrs) and (attrs["data-ftml-definiens"] == definiendum_link):
            return definition_tree
        for child in definition_tree.children:
            definiensContent_tree = get_definiensContent(definiendum_link, child)
            if definiensContent_tree is not None:
                return definiensContent_tree
            
    elif isinstance(definition_tree, gfxml.G):
        for child in definition_tree.children:
            definiensContent_tree = get_definiensContent(definiendum_link, child)
            if definiensContent_tree is not None:
                return definiensContent_tree
            
    return None

def rename_variables(definiens_content_tree, statement_tree): #TODO: Implementation.
    #Wie kann ich innerhalb von Tag-Nodes überhaupt einzelne Variablen erkennen?
    return definiens_content_tree
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Functions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
def initializeGfShell():
    shell = gf.GFShellRaw(PATH_exe_gf)
    print(shell.handle_command(f"import {PATH_gf_concrGrammar}"))
    return shell

def parseHtmltoTrees(shell: gf.GFShellRaw, htmlfile_path: str):
    #Returns all possible trees in an array
    input_shtml = gfxml.parse_shtml(htmlfile_path)
    #Simplify the tags (e.g. replace "<div shtml:sourceref="http://mathhub.info/smglom/algebra/mod/monoid.en.tex#367.15.1:380.15.14" class="rustex-VFil">" by "< 15 >")
    input_xs, input_string = gfxml.get_gfxml_string(input_shtml)
    input_sentences = gfxml.sentence_tokenize(input_string)
    for s in input_sentences:
        input_sentence_preprocessed = make_sentence_GfConform(s)
        print("\ninput_sentence_preprocessed: " + str(input_sentence_preprocessed))
        #input_sentence_preprocessed = "< 4 > " + str(input_sentence_preprocessed)
        gf_ast = shell.handle_command(f'p "{input_sentence_preprocessed}"')
        #print("\ninput_gf_ast: " + str(gf_ast))
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
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Definition Expansion -------------------------------------------------------------------------------------------------------------------------------------------------------------###
#Functions for Definition Expansion
def get_extendedVariables_tree(statement_tree): #TODO: Implementation.
    #TODO: Add Variable after Nouns, which are in relation to the definiendum
    return statement_tree

def get_alignedVariables_trees(definiens_content_tree, definition_tree, statement_tree): #TODO: Implementation.
    return definiens_content_tree, statement_tree
    statement_tree_extendedVariables = get_extendedVariables_tree(statement_tree) #TODO
    assignedVariables = variableAssigner.get_assignedVariables(statement_tree_extendedVariables, definition_tree, definiens_content_tree) #TODO
    print("\nassignedVariables: " + str(assignedVariables))
    for variable in assignedVariables:
        if not gfxml.tree_contains_node(statement_tree, gfxml.xify(assignedVariables[variable])):
            statement_tree = statement_tree_extendedVariables

    for variable in assignedVariables:
        replaced_node = gfxml.xify(variable)
        replacement_node = gfxml.xify(assignedVariables[variable])
        definiens_content_tree = gfxml.tree_subst(definiens_content_tree, replaced_node, replacement_node)
        print("\nreplaced_node: " + str(replaced_node))
        print("\nreplacement_node: " + str(replacement_node))
    return definiens_content_tree

def get_deleteTree_defExp(statement_tree, definiendum_link):
    print()
    print("definiendum_link: " + str(definiendum_link))
    print("statement_tree: " + str(statement_tree))
    if isinstance(statement_tree, gfxml.X) and statement_tree.tag == 'span':
        attrs = statement_tree.attrs
        if ("data-ftml-head" in attrs) and (attrs["data-ftml-head"] == definiendum_link):
            return statement_tree
        for child in statement_tree.children:
            delete_tree = get_deleteTree_defExp(child, definiendum_link)
            if delete_tree is not None:
                return delete_tree

    elif isinstance(statement_tree, gfxml.G):
        for child in statement_tree.children:
            delete_tree = get_deleteTree_defExp(child, definiendum_link)
            if delete_tree is not None:
                return delete_tree
            
    return None

def get_mergedTree(statement_tree, definiens_content_tree, definiendum_link):
    """Grammar dependent method."""
    merged_tree = None
    #Get actual definiens content tree (= definiens content tree without wrapper)
    ADC_tree = definiens_content_tree.children[0].children[0]
    print("\nADC_tree: " + str(ADC_tree))
    #Get the subtree from the statement tree, which needs to be removed (= the reference to the definiendum)
    delete_tree = get_deleteTree_defExp(statement_tree, definiendum_link)
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

        elif (delete_tree.wrapfun == "WRAP_N" and (ADC_tree.node == "AdvCN")):
            # <noun which is the definiendum> <variable name>     =>     <noun of definiens content> <variable name> <rest of the definiens content>
            delete_tree_temp = gfxml.get_firstOuterNode(statement_tree, gfxml.get_firstOuterNode(statement_tree, gfxml.get_firstOuterNode(statement_tree, delete_tree)))
            #match delete_tree_temp:
            #    case gfxml.G('DetCN', [R_DetQuant, gfxml.G('AdjCN', [gfxml.G('PositA', deletedTree), R_Noun])]):
            #        noun_tree = gfxml.G('DetCN', [R_DetQuant, gfxml.G('ApposCN', [gfxml.G('ApposCN', [gfxml.G('AdvCN', [R_Noun, gfxml.G('such_Adv', [])]), gfxml.G('DetNP', [gfxml.G('DetQuant', [gfxml.G('that_Quant', []), gfxml.G('NumSg')])])]), ADC_tree])])
            #        rest_tree =
            #        merged_tree = gfxml.tree_subst(statement_tree, delete_tree_temp, new_tree)
            #ADC_tree: G('AdvCN', [G('UseN', [X('span', [G('', [X('span', [G('element_N', [])], {'data-ftml-comp': ''}, 'WRAP_N')])], {'data-ftml-term': 'OMID', 'data-ftml-head': 'https://stexmmt.mathhub.info/:sTeX?a=smglom/sets&p=mod&m=set&s=element', 'data-ftml-notationid': ''}, 'WRAP_N')]), G('PrepNP', [G('of_Prep', []), G('formula_NP', [X('math', [X('mrow', [X('mi', [XT('Q')], {'data-ftml-comp': ''}, None)], {'data-ftml-term': 'OMID', 'data-ftml-head': 'https://stexmmt.mathhub.info/:sTeX?a=Papers/cicm25-ling&p=mod&m=nfa/non-deterministic finite automaton&s=states', 'data-ftml-notationid': ''}, None)], {}, 'wrap_math')])])])

    return merged_tree

#DEFINITION EXPANSION
def definitionExpansion(statement_tree: str, definition_treeS: str, definiendum_link: str):
    print("\n----------\nDefinition Expansion")
    for definition_tree in definition_treeS:
        print("\ndefinition_tree: " + str(definition_tree))

        #Extract the definiens content tree out of the definition tree
        definiens_content_tree = get_definiensContent(definiendum_link, definition_tree)
        if definiens_content_tree == None: 
            print("ERROR: No definiens_content_tree found in the definition sentence.")
            break
        else: print("\ndefiniens_content_tree: " + str(definiens_content_tree))

        #Rename variables in definiens content tree if they are already used in the statement tree
        definiens_content_tree = rename_variables(definiens_content_tree, statement_tree) #TODO: Does not need the trees but the tag contents

        #Assign variables (and introduce variables in statement tree if necessary)
        definiens_content_tree, statement_tree = get_alignedVariables_trees(definiens_content_tree, definition_tree, statement_tree) #TODO

        #Align the category of the definiens content to the category of the definiendum
        merged_tree = get_mergedTree(statement_tree, definiens_content_tree, definiendum_link) #TODO
        print("\nmerged_tree: " + str(merged_tree))
        return merged_tree
    return "Error."
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
            


###----- Definition Reduction -------------------------------------------------------------------------------------------------------------------------------------------------------------###
#Functions for Definition Reduction
global mappingCounter

def abstractTreeMapping(tree, mapping, seen_math_nodes):
    """
    Abstracts math nodes into unique VAR_X placeholders while ensuring identical math nodes
    are mapped to the same placeholder.
    Returns the abstracted tree and a mapping of VAR_X placeholders to their original math nodes.
    """
    if tree is None:
        return mapping

    #If the node is a math node, replace it with a MATH_X placeholder
    match tree:
        case gfxml.X('math', x):
            #Check if this math node was already seen
            seen = False
            for i, seen_tree in enumerate(seen_math_nodes):
                if seen_tree == tree:  # Direct structure comparison instead of hashing
                    var_name = f"MATH_{i}"
                    seen = True
            if not seen:
                #New math node -> assign new VAR_X
                var_name = f"MATH_{len(seen_math_nodes)}"
                seen_math_nodes.append(tree)
                mapping[var_name] = tree
            
    #Recursively process children
    if isinstance(tree, gfxml.G) or isinstance(tree, gfxml.X):
        for child in tree.children:
            mapping.update(abstractTreeMapping(child, mapping, seen_math_nodes))

    return mapping

def get_abstract_tree(tree):
    mappingCounter = 0
    mapping = abstractTreeMapping(tree, {}, [])
    for map in mapping:
        tree = gfxml.tree_subst(tree, mapping[map], map)
    return tree, mapping

def get_deleteTree_defRed(statement_tree, abstract_DCT): 
    #TODO: Get variants of definiens_content_tree => Use CNL grammar to get variants
    abstract_ST, ST_mapping = get_abstract_tree(statement_tree)
    if str(abstract_ST) == str(abstract_DCT): #gfxml.tree_eq(abstract_ST, abstract_DCT):
        return statement_tree, ST_mapping 
    
    elif isinstance(statement_tree, gfxml.G):
        for child in statement_tree.children:
            delete_tree, ST_mapping = get_deleteTree_defRed(child, abstract_DCT)
            if delete_tree is not None:
                return delete_tree, ST_mapping
            
    return None, {}

def get_definiendumTree(definition_tree, definiendum_link):
    if isinstance(definition_tree, gfxml.X) and definition_tree.tag == 'span':
        attrs = definition_tree.attrs
        if ("data-ftml-definiendum" in attrs) and (attrs["data-ftml-definiendum"] == definiendum_link):
            return definition_tree
        for child in definition_tree.children:
            delete_tree = get_definiendumTree(child, definiendum_link)
            if delete_tree is not None:
                return delete_tree

    elif isinstance(definition_tree, gfxml.G):
        for child in definition_tree.children:
            delete_tree = get_definiendumTree(child, definiendum_link)
            if delete_tree is not None:
                return delete_tree
            
    return None

#DEFINITION REDUCTION
def definitionReduction(statement_tree: str, definition_treeS: str, definiendum_link: str):
    print("\n----------\nDefinition Reduction")
    for definition_tree in definition_treeS:
        print("\ndefinition_tree: " + str(definition_tree))

        #Extract the definiens content tree out of the definition tree
        definiens_content_tree = get_definiensContent(definiendum_link, definition_tree)
        if definiens_content_tree == None: 
            print("ERROR: No definiens_content_tree found in the definition sentence.")
            break
        else: print("\ndefiniens_content_tree: " + str(definiens_content_tree))

        #Rename variables in definiens content tree if they are already used in the statement tree
        definiens_content_tree = rename_variables(definiens_content_tree, statement_tree)

        #Find definiens content tree in statement tree
        #print("\nstatement_tree: " + str(statement_tree))
        #print("\ndefiniens_content_tree: " + str(definiens_content_tree))
        for child in definiens_content_tree.children:
            definiens_content_tree = child
        for child in definiens_content_tree.children:
            definiens_content_tree = child
        abstract_DCT, DCT_mapping = get_abstract_tree(definiens_content_tree)
        replaced_node, statement_mapping = get_deleteTree_defRed(statement_tree, abstract_DCT)

        #Replace definiens content tree in statement tree by definiendum
        reduced_tree = ""
        replacement_node = get_definiendumTree(definition_tree, definiendum_link) #Node for definiendum depending on replaced node
        #for map in DCT_mapping: 
        #    gfxml.tree_subst(replacement_node, DCT_mapping[map], statement_mapping[map])

        print("\n-----")
        print("\nreplace_node/deleteTree: " + str(replaced_node))
        print("\nreplacement_node: " + str(replacement_node))
        print("\nstatement_tree: " + str(statement_tree))

        #Construct Replacement Node:  <span data-ftml-definiendum="X">S</span>   ->   <span data-ftml-head="X" data-ftml-term="OMID" data-ftml-notationid="" ><span data-ftml-comp="">S</span></span>
        match replacement_node:
            case gfxml.X('span', [gfxml.G(word_1, [])], {'data-ftml-definiendum': tag_1}, wrap_1):
                replacement_node = gfxml.X('span', [gfxml.G('', [gfxml.X('span', [gfxml.G(word_1, [])], {'data-ftml-comp': ''}, wrap_1)])], {'data-ftml-head': tag_1, 'data-ftml-term': 'OMID', 'data-ftml-notationid': ''}, wrap_1)

        if replaced_node.node == replacement_node.wrapfun: #gfxml.get_firstOuterNode(definition_tree, replaced_node) == gfxml.get_firstOuterNode(statement_tree, replaced_node):
            reduced_tree = gfxml.tree_subst(statement_tree, replaced_node, replacement_node)
            return reduced_tree
    
        elif (replacement_node.wrapfun == "WRAP_A") and (replaced_node.node == "PredVP"):
            # "has" + <bla>     =>     "is" + <adjective>
            match replaced_node:
                case gfxml.G('PredVP', [gfxml.G('formula_NP', c_1), gfxml.G('ComplSlash', c_2)]):
                    replacement_node = gfxml.G('PredVP', [gfxml.G('formula_NP', c_1), gfxml.G('UseComp', [gfxml.G('CompAP', [gfxml.G('PositA', [replacement_node])])])])
                    # [G('', [X('span', [G('empty_A', [])], {'data-ftml-comp': ''}, 'WRAP_A')])], {'data-ftml-head': 'https://stexmmt.mathhub.info/:sTeX?a=smglom/sets&p=mod&m=emptyset&s=empty', 'data-ftml-term': 'OMID', 'data-ftml-notationid': ''}, 'WRAP_A')])])])])])])
                    reduced_tree = gfxml.tree_subst(statement_tree, replaced_node, replacement_node)
                    print("\nresult_tree: " + str(reduced_tree))
                    return reduced_tree
            
        """
        elif (delete_tree.wrapfun == "WRAP_A") and (ADC_tree.node == "formula_NP"):
            # <adjective which is the definiendum> <noun>     =>     <noun> "such that" <definiens content>
            delete_tree_temp = gfxml.get_firstOuterNode(statement_tree, gfxml.get_firstOuterNode(statement_tree, gfxml.get_firstOuterNode(statement_tree, delete_tree)))
            match delete_tree_temp:
                case gfxml.G('DetCN', [R_DetQuant, gfxml.G('AdjCN', [gfxml.G('PositA', deletedTree), R_Noun])]):
                    new_tree = gfxml.G('DetCN', [R_DetQuant, gfxml.G('ApposCN', [gfxml.G('ApposCN', [gfxml.G('AdvCN', [R_Noun, gfxml.G('such_Adv', [])]), gfxml.G('DetNP', [gfxml.G('DetQuant', [gfxml.G('that_Quant', []), gfxml.G('NumSg')])])]), ADC_tree])])
                    merged_tree = gfxml.tree_subst(statement_tree, delete_tree_temp, new_tree)
        """


    print("\nMISSING: Add new grammatical structure to definitionReduction().")
    return statement_tree
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Comprehension Term Reduction -----------------------------------------------------------------------------------------------------------------------------------------------------###
#Functions for Comprehension Term Reduction
#...

#COMPREHENSION TERM REDUCTION
def comprehensionTermReduction(statement_tree, original_treeS: str, reduction_treeS: str):
    """ Concept: Find original tree in statement tree.
        Create reduction tree based on original tree
        Replace original tree in statement tree by reduction tree."""
    
    original_tree = original_treeS[0]
    reduction_tree = reduction_treeS[0]
    print("\noriginal_tree: " + str(original_tree))
    print("\nreduction_tree: " + str(reduction_tree))
    replaced_node = None 
    replacement_node = None

    if False: #"elements x of {y | z}"   =>   "elements x = y with z" 
        #replaced_node = tree for "elements x of {y | z}"
        #replacement_node = tree for "elements x = y with z" 
        print()
    
    elif False: #Other cases
        print()

    comprehensedTree = gfxml.tree_subst(statement_tree, replaced_node, replacement_node)
    return comprehensedTree
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Main -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
def main(input):
    shell = initializeGfShell()
    for element in input: #TODO: Not just for one tree, but try every tree until one passes all steps. => Exponentional

        if element == "statement": #IMPORTANT: Statement HAS to be the first input!
            statement_path = input[element]
            statement_treeS = parseHtmltoTrees(shell, statement_path)
            statement_tree = statement_treeS[0]

        if "definition expansion" in element:
            DefExp = input[element]
            definition_path = DefExp["definition"]
            definition_treeS = parseHtmltoTrees(shell, definition_path)
            definiendum_link = getDefiniendumLink(definition_path)
            statement_tree = definitionExpansion(statement_tree, definition_treeS, definiendum_link)

        if "definition reduction" in element:
            DefRed = input[element]
            definition_path = DefRed["definition"]
            definition_treeS = parseHtmltoTrees(shell, definition_path)
            definiendum_link = getDefiniendumLink(definition_path)
            statement_tree = definitionReduction(statement_tree, definition_treeS, definiendum_link)

        if "comprehension term reduction" in element:
            CTRed = input[element]
            original_path = CTRed["original"]
            original_treeS = parseHtmltoTrees(shell, original_path)
            comprehension_path = CTRed["comprehension"]
            comprehension_treeS = parseHtmltoTrees(shell, comprehension_path)
            statement_tree = comprehensionTermReduction(statement_tree, original_treeS, comprehension_treeS)

        if "result" in element:
            pass

    output = linearizeTreeToString(shell, statement_tree)
    print("\n==========\nOUTPUT: " + output)

def testExample(example_name):
    with open("sHTML\Examples\examples.json", 'r', encoding="utf-8") as file:
        examples = json.load(file)
    example = examples[example_name]
    main(example)
    #shell = initializeGfShell()
    #trees = parseHtmltoTrees(shell, example["comprehension term reduction 1"]["comprehension"])#["statement"])
    #string = linearizeTreeToString(shell, trees[0])
testExample("DR002")
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###