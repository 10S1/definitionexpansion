"""
Input: statement URI [str], definition URI [str] and definiendum name [str]
Output: merged sentence [str], (optionally: merged sTeX file)



The definitionExpander [sTeX/definitionExpander.py] gets three Strings as inputs: A statement URI, a definition URI and the name of the definiendum (= a mathematical term).
The definiendum is definiend in the paragraph P_2, which the definition URI refers to and gets used in the paragraph P_1, which the statement URI refers to.
P_1 and P_2 are appear in SMGloM modules M_1 and M_2. THe SMGloM uses sTeX to create a glossary of mathematical terms, which can refer and import each other.
The Preprocessor is used to extract and format P_1 and P_2 and to collect commands and variables, which could be used in M_1 and M_2.

The grammarGenerator [sTeX/grammarGenerator.py] uses the extraced commands and variables and a list of definiendums [Resources\definiendums.json] to create 
a grammar G [sTeX\Grammar\GEN_grammar_abstr.gf and sTeX\Grammar\GEN_grammar_concr.gf] for parsing the sentences in P_1 and P_2. 
    => Currently, this only works, if there is just a single sentence S_1 in P_1 and a single sentence S_2 in P_2.
The grammar G imports multiple grammars [sTeX\Grammar] to include more mathematical terms.

The grammar G is used to parse the sentences S_1 and S_2 through the Grammatical Framework [Resources/gf.py]. 
The parsed sentences are then converted into ASTs [Resources/gf_ast.py] A_1 and A_2. 
Since there are multiple A_1s and A_2s, the algorithm goes to the combinations, until it finds a working combination.

The definitionExpander replaces the definiendum in S_1 through its definition, which is extraced out of S_2.
This is done by working with A_1 and A_2: 
    At first, new variables in A_1 are introduced, if those are needed for the merging.
    Secondly, the subtree A_delete, which needs to be removed from A_1 gets extraceted.
    Afterwards, the definiens subtree for the definiendum A_definiens gets extraced out of A_2. If necessary, the variables in A_2 are renamed.
    Then, a replacement tree A_replace gets created based on the part of speech (POS) tag of the deleted tree and the POS tag of the A_definiens.
    In A_replace the variables from A_2 are replaced by the corresponding variables out of A_1.
    At last, in A_1 the subtree A_delete is replaced through A_replace.

The resulting AST A_3 is linearized again into the sentence S_3, which is the output.
Optionally [set active_stexOutput = True], a new SMGloM module M_3 can be generated.
M_3 is M_1, but S_1 is replaced with S_3 and the necessary sTeX commands from M_2 are added.
"""

###----- Imports --------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
import json
import random
import string
import regex as re
import shutil
import os
import sys
from typing import List, Any, Tuple, Dict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Resources')))
import grammarGenerator
import preprocessingInterface
import stexGenerator
import gf
from gf_ast import GfAst
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Paths ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
PATH_exe_preprocessor = shutil.which('relocate')
if PATH_exe_preprocessor is None:
    print("ERROR: Path to relocate.exe not found. \nCheck whether the Preprocessor is installed and the environment variable is set.")

PATH_exe_gf = shutil.which('gf')
if PATH_exe_gf is None:
    print("ERROR: Path to gf.exe not found. \nCheck whether the Grammatical Framework is installed and the environment variable is set.")

PATH_dict_mathhub = os.getenv('MATHHUB').strip('"')
if (PATH_dict_mathhub is None) or (not os.path.isdir(PATH_dict_mathhub)):
    print("ERROR: Path to MathHub not found. \nCheck whether the SMGloM is installed and the environment variable is set.")
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Variables ------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----###
#Length of the names, which are generated for new or renamed variables
length_randomVariablenames = 20

#Paths where the base grammar (= the grammar which gets extended by additonally generated rules) is placed.
PATH_gf_grammar = r'sTeX/Grammar/'
basename = r"sTeX\Grammar\BaseGrammar"

#Variables which are introduced during merging or renamed.
introducedVariables = []

#Paths where the generated grammars will be placed.
PATH_gf_concrGrammar = 'sTeX\Grammar\GEN_grammar_concr.gf'
PATH_gf_abstrGrammar = 'sTeX\Grammar\GEN_grammar_abstr.gf'
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Irrelevant Functions -------------------------------------------------------------------------------------------------------------------------------------------------------------###
def flatten_list_of_lists(nested_lists: List[List[Any]]) -> List[Any]:
    return [item for sublist in nested_lists for item in sublist]

def random_variable_name(lengthOfNumber: int) -> str:
    """Generates a string in the format of: "X_" + <digit><digit>...<digit>"""
    return 'X_' + ''.join(random.choice(string.digits) for _ in range(lengthOfNumber))

def alphaRenamingOfVariables(variables_definition: List[Dict[str, Any]], variables_statement: List[Dict[str, Any]], tree_definition: str) -> List[Any]:
    """Renames variables in the definition sentence/AST if they also appear in the statement sentence/AST."""
    newIntroducedVariables = []
    for var in variables_definition:
        if var in variables_statement:
            #Generate cryptic (= hopefully not already existing) variable name
            newVar = {'name': "\\" + str(random_variable_name(length_randomVariablenames)), 'parameters': var["parameters"]}
            tree_definition.replace(var["name"], newVar["name"])
            newIntroducedVariables.append(newVar)
    return [tree_definition, newIntroducedVariables]

def get_varsOfPrepositions(ast: GfAst) -> List[List[str]]:
    """Extracts variables out of an AST if they occur after a preposition."""
    vars = []
    match ast:
        case GfAst("PrepNP", [preposition_1, np_1]):
            type_prep = preposition_1.to_str()
            match np_1:
                case GfAst("R_np_formula", [GfAst("R_formula_symbolicExpression", [symbolicExpression_11])]):
                    vars.append([type_prep, symbolicExpression_11])
                case GfAst("R_AdvNP", [GfAst("R_formula_symbolicExpression", [symbolicExpression_12]), adv_12]):
                    vars.append([type_prep, symbolicExpression_12])

    for child in ast.children:
        res = get_varsOfPrepositions(child)         
        if len(res) >= 1:
            vars.extend(res)

    return vars

def get_assignedVariables_definition(ast: GfAst, definiendum: str) -> List[List[str]]:
    """Extracts variables and their category (e.g. "main", "from", "to", ...) out of the definitions AST."""
    vars = []
    vars.extend(get_varsOfPrepositions(ast))
    match ast:
        #"main"
        #TODO: TODOTODO : Im uebrigen Teil des Baums muss das definiendum vorkommen. Eigentlich komplett anders.
        case GfAst("UseCl", [temp_1, pol_1, cl_1]):
            match cl_1:
                case GfAst("PredVP", [np_11, vp_11]):
                    match np_11:
                        case GfAst("R_np_formula", [GfAst("R_formula_symbolicExpression", [symbolicExpression_111])]):
                            vars.append(["main", symbolicExpression_111.to_str()])
                        case GfAst("DetCN", [det_112, GfAst("ApposCN", [cn_112, GfAst("R_np_formula", [GfAst("R_formula_symbolicExpression", [symbolicExpression_112])])])]):
                            vars.append(["main", symbolicExpression_112.to_str()])
        
        #TODO: Other definition cases

    for child in ast.children:
        res = get_assignedVariables_definition(child, definiendum)         
        if len(res) >= 1:
            vars.extend(res)

    return vars

def get_assignedVariables_statement(ast: GfAst, definiendum: str) -> List[List[str]]:
    """Extracts variables and their category (e.g. "main", "from", "to", ...) out of the statement AST."""
    vars = []
    vars.extend(get_varsOfPrepositions(ast))
    match ast:
        #"main"
        #Case: <adjective, which is the definiendum> <noun> <variable>
        case GfAst("AdjCN", [GfAst("PositA", [GfAst("A_sn_A", [GfAst(definiendum_rule, [])])]), cn_1]):
            if (definiendum_rule == str(definiendum) + "_A"):
                match cn_1:
                    case GfAst("ApposCN", [cn_11, GfAst("R_np_formula", [GfAst("R_formula_symbolicExpression", [symbolicExpression_11])])]):
                        vars.append(["main", symbolicExpression_11.to_str()])
        #TODO: Other statement cases
        #Case: <noun> <variable> "is" <adjective, which is the definiendum>
        case GfAst('UseCl', [
            TTAnt_2, 
            PPos_2, 
            GfAst('PredVP', [
                GfAst("R_np_formula", [
                    GfAst("R_formula_symbolicExpression", [symbolicExpression_2])
                ]), 
                GfAst("UseComp", [
                    GfAst("CompAP", [
                        GfAst("PositA", [
                            GfAst("A_sn_A", [GfAst(definiendum_rule, [])])
                            ])
                        ])
                    ])
                ])
            ]):
            if (definiendum_rule == str(definiendum) + "_A"):
                vars.append(["main", symbolicExpression_2.to_str()])
        #test = fAst('UseCl', [GfAst('TTAnt', [GfAst('TPres', []), GfAst('ASimul', [])]), GfAst('PPos', []), GfAst('PredVP', [GfAst('R_np_formula', [GfAst('R_formula_symbolicExpression', [GfAst('R_symbolicExpression_texCommand', [GfAst('G_texCommand_TEXZFC_', [])])])]), GfAst('UseComp', [GfAst('CompAP', [GfAst('PositA', [GfAst('A_sn_A', [GfAst('consistent_A', [])])])])])])])])
        
        #Case: <noun> "is a" <noun, which is the definiendum>
        #...
            
        #STATEMENT CASES
        #TODO: Only if tree is part of deleted part?
        #TODO: Special case: Multiple variables

    for child in ast.children:
        res = get_assignedVariables_statement(child, definiendum)         
        if len(res) >= 1:
            vars.extend(res)

    return vars

def assignedVariableRenaming(tree_replacement: str, ast_definition: GfAst, ast_statement: GfAst, definiendum: str) -> List[Any]:
    """
    The variables in the statement and the definition (execluding the definiens content), which can be assigned to each other, 
    get accordingly replaced in the definition AST.
    """
    replaceVar_dict = {}   #E.g. like: ["main", "xVar"], ["from", "yVar"]
    vars_definition = get_assignedVariables_definition(ast_definition, definiendum)
    vars_statement = get_assignedVariables_statement(ast_statement, definiendum)
    vars_unassigned = vars_definition

    for varDef in vars_definition:
        for varSt in vars_statement:
            if varDef[0] == varSt[0]:
                replaceVar_dict[varDef[1]] = varSt[1]
                if varDef in vars_unassigned:
                    vars_unassigned.remove(varDef)
                vars_statement.remove(varSt)

    vars_unassigned = vars_definition

    #Replace assigned vars in replacement tree
    for key in replaceVar_dict:
        tree_replacement = tree_replacement.replace(key, replaceVar_dict[key])  

    print("\nreplaceVar_dict: " + str(replaceVar_dict))
    return [tree_replacement, vars_unassigned]

def introduceVariables(ast: GfAst, definiendum: str) -> List[Any]:
    """If there is a noun in the statement sentence, which is [connected to] the definiendum, a variable gets introduced after it."""
    introducedVars = []
    tree_statement = ast
    match ast:
        #"main"
        #Case: <adjective, which is the definiendum> <noun>
        case GfAst("AdjCN", [GfAst("PositA", [GfAst("A_sn_A", [GfAst(definiendum_rule, [])])]), cn_1]):
            if (definiendum_rule == str(definiendum) + "_A"):
                match cn_1:
                    case GfAst("UseN", [cn_12]):
                        #Introduce symbol
                        newVar = {'name': "\\" + str(random_variable_name(length_randomVariablenames)), 'parameters': []}
                        introducedVars.append(newVar)
                        rulename = "G_variable_VAR" + preprocessingInterface.makeNameGfConform(newVar["name"][1:])
                        newSymbolicExpression_12 = GfAst("R_symbolicExpression_variable", [GfAst(rulename, [])])
                        tree_statement = GfAst("AdjCN", [GfAst("PositA", [GfAst("A_sn_A", [GfAst(definiendum_rule, [])])]), GfAst("ApposCN", [GfAst("UseN",[cn_12]), GfAst("R_np_formula", [GfAst("R_formula_symbolicExpression", [newSymbolicExpression_12])])])])
                        return [tree_statement, introducedVars]
        #TODO: Other statement cases
        #Case: <noun> "is" <adjective, which is the definiendum>
        #Case: <noun> "is a" <noun, which is the definiendum>
        #...
            
        #STATEMENT CASES
        #TODO: Only if tree is part of deleted part?
        #TODO: Special case: Multiple variables

    for i, child in enumerate(ast.children):
        treeStatement_and_introducedVars = introduceVariables(child, definiendum)  
        ast.children[i] = treeStatement_and_introducedVars[0]  # Update the child in the original AST
        introducedVars.extend(treeStatement_and_introducedVars[1])

    return [tree_statement, introducedVars]


#AST STUFF
def get_replacementTree(deletedTree: str, definiensContentTree: str, definiendumAst: GfAst) -> str:
    """Generates the AST, which will replace the delete AST in the statement AST."""
    deletedAst = GfAst.from_str(deletedTree)
    definiensContentAst = GfAst.from_str(definiensContentTree)
    replacementAst = None
    match deletedAst:
        case GfAst("UseCl", [temp_1, pol_1, GfAst("PredVP", [np_1, GfAst("UseComp", [GfAst("PositA", [defi_1])])])]):
            match definiensContentAst:
                case GfAst("UseCl", rest_11):
                    replacementAst = definiensContentAst
        
        case GfAst("UseCl", [temp_2, pol_2, GfAst("PredVP", [np_2, GfAst("UseComp", [GfAst("CompAP", [GfAst("PositA", [defi_2])])])])]):
            match definiensContentAst:
                case GfAst("UseCl", rest_21):
                    replacementAst = definiensContentAst
        
        case GfAst("AdjCN", [GfAst("PositA", [defi_3]), GfAst("UseN", [n_3])]):
            match definiensContentAst:
                case GfAst("UseCl", [temp_31, pol_31, cl_31]):
                    replacementAst = GfAst("RelCN", [GfAst("UseN", [n_3]), GfAst("UseRCl", [temp_31, pol_31, GfAst("RelCl", [cl_31])])])
        
        case GfAst("AdjCN", [GfAst("PositA", [defi_4]), GfAst("ApposCN", [cn_4, np_4])]):
            match definiensContentAst:
                case GfAst("UseCl", [temp_41, pol_41, cl_41]):
                    replacementAst = GfAst("RelCN", [GfAst("ApposCN", [cn_4, np_4]), GfAst("UseRCl", [temp_41, pol_41, GfAst("RelCl", [cl_41])])])
        
        #case GfAst('AdjCN', [GfAst('PositA', [defi_5]), GfAst('CN_sn_CN', [GfAst('UseN', [GfAst('model_N', [])])])]):

    replacementTree = GfAst.to_str(replacementAst)
    return replacementTree

def get_definiendumAST_definiendumType(ast: GfAst, definiendum: str) -> Tuple[GfAst, str]:
    """Extracts the AST of the definiendum and the part of speech category of the definiendum."""
    definiendum = preprocessingInterface.makeNameGfConform(definiendum)
    match ast:
        case GfAst(name, [inner]) if name in {'N_sn_N', 'N_sns_N', 'N_Sn_N', 'N_Sns_N'}:
            if (inner == GfAst(definiendum + "_N", [])): return [ast, "noun"]
        case GfAst(name, [inner]) if name in {'A_sn_A', 'A_sns_A', 'A_Sn_A', 'A_Sns_A'}:
            if (inner == GfAst(definiendum + "_A", [])): 
                return [ast, "adjective"]
        case GfAst(name, [inner]) if name in {'V_sn_V', 'V_sns_V', 'V_Sn_V', 'V_Sns_V'}:
            if (inner == GfAst(definiendum + "_V", [])): return [ast, "verb"]
        #TODO: TODOTODO Other cases (U_transitiveAdjective, U_transitiveVerb, tex command; mAdjective; mVerb)
    if ast.children is not None:
        for child in ast.children:
            res = get_definiendumAST_definiendumType(child, definiendum)         
            if res is not None: return res
    return None                                                            

def get_definiensContentTree(ast_definition: GfAst, definiendum: str, definiendum_type: str) -> str:
    """Extracts the AST in the definiens command of the definiendum out of the definition AST."""
    # E.g.: "$ \\\\nvar $ is \\\\definame { positive } iff \\\\definiens [ positive ] { $ \\\\intmorethan { \\\\nvar } { 0 } $ } ."
    definiendum = preprocessingInterface.makeNameGfConform(definiendum)
    definiensContent = None
    if (ast_definition.node == "S_definiendum_WW" + str(definiendum) + "_S") or (ast_definition.node == "S_definiendum_WWS_definiendum_WW" + str(definiendum) + "_S"):
        definiensContent = ast_definition.children[0]

    #TODO: TODOTODO Can be other things too, not just sentences

    if (definiensContent is not None):  
        return GfAst.to_str(definiensContent)
    if ast_definition.children is not None:
        for child in ast_definition.children:
            res = get_definiensContentTree(child, definiendum, definiendum_type)        
            if res is not None: return res
    return None

def get_deleteTree_definiendumType_definiendumAST(ast_statement: GfAst, definiendum_gfCon: GfAst) -> List[Any]:
    """
    Returns the tree, which will be removed out of the statement AST (usually is or contains the definiendum)
    and the part of speech category of the definiendum and the AST of the definiendum.
    """
    definienumType = None
    match ast_statement:
        #TODO: adjective (allein stehend, gefolgt von noun, ...); noun; verb; command; ...
        case GfAst("UseCl", [temp_1, pol_1, GfAst("PredVP", [np_1, GfAst("UseComp", [GfAst("CompAP", [GfAst("PositA", [defi_1])])])])]):
            definiendumAST_definiendumType1 = get_definiendumAST_definiendumType(defi_1, definiendum_gfCon)
            if definiendumAST_definiendumType1 != None:
                [definiendumAST, definienumType] = definiendumAST_definiendumType1
                if defi_1 == definiendumAST:
                    return [GfAst("UseCl", [temp_1, pol_1, GfAst("PredVP", [np_1, GfAst("UseComp", [GfAst("CompAP", [GfAst("PositA", [defi_1])])])])]).to_str(), definienumType, definiendumAST.to_str()]
     
        case GfAst("UseCl", [temp_1, pol_1, GfAst("PredVP", [np_1, GfAst("UseComp", [GfAst("PositA", [defi_1])])])]):
            definiendumAST_definiendumType1 = get_definiendumAST_definiendumType(defi_1, definiendum_gfCon)
            if definiendumAST_definiendumType1 != None:
                [definiendumAST, definienumType] = definiendumAST_definiendumType1
                if defi_1 == definiendumAST:
                    return [GfAst("UseCl", [temp_1, pol_1, GfAst("PredVP", [np_1, GfAst("UseComp", [GfAst("PositA", [defi_1])])])]).to_str(), definienumType, definiendumAST.to_str()]

        # case GfAst("AdjCN", [GfAst("PositA", [defi_2]), rest]):
        #     print("TEST3")
        #     definiendumAST_definiendumType2 = get_definiendumAST_definiendumType(defi_2, definiendum_gfCon)
        #     if definiendumAST_definiendumType2 != None:
        #         [definiendumAST, definienumType] = definiendumAST_definiendumType2
        #         if defi_2 == definiendumAST:
        #             return [GfAst("AdjCN", [GfAst("PositA", [defi_2]), rest]).to_str(), definienumType, definiendumAST.to_str()]

        case GfAst('BlaBla', [bla1]):
            [definiendumTree, definienumType] = get_definiendumAST_definiendumType(bla1, definiendum_gfCon)

        #NOUNS:
        case GfAst("UseN", [defi_5]):
            definiendumAST_definiendumType5 = get_definiendumAST_definiendumType(defi_5, definiendum_gfCon)
            if definiendumAST_definiendumType5 != None:
                [definiendumAST, definienumType] = definiendumAST_definiendumType5
                if defi_5 == definiendumAST:
                    return [GfAst("UseN", [defi_5]).to_str(), definienumType, definiendumAST.to_str()]
        
        #TODO: More cases

    if ast_statement.children is not None:
        for child in ast_statement.children:
            res = get_deleteTree_definiendumType_definiendumAST(child, definiendum_gfCon)        
            if res is not None: return res
    return None 
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Functions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
def expandDefinitions(definition: str, statement: str, definiendum: str, variablesDefinition: List[Dict[str, Any]], variablesStatement: List[Dict[str, Any]], shell: gf.GFShellRaw) -> str:
    """
    Replaces the definiendum in the statement by the definiens content in the definition while 
    keeping a correct sytax and adapting the variables. Returns an AST.
    """
    #FROM STATEMENT: Get statement sentence trees
    cmd_parseStatement = 'parse "' + statement + '"'
    tree_statement_all = shell.handle_command(cmd_parseStatement)
    #Loop to handle multiple statement trees 
    tree_statements = tree_statement_all.split('\n')
    for i in range(len(tree_statements)):
        newIntroducedVariables = []
        tree_statement = tree_statements[i]
        og_tree_statement = tree_statements[i]
        ast_statement = GfAst.from_str(tree_statement)

        #IN STATEMENT: Introduce new variables if necessary
        treeStatement_and_introducedVars = introduceVariables(GfAst.from_str(tree_statement), definiendum) 
        ast_statement = treeStatement_and_introducedVars[0]
        tree_statement = treeStatement_and_introducedVars[0].to_str()
        newIntroducedVariables.extend(treeStatement_and_introducedVars[1])

        #FROM STATEMENT: Get the delete tree
        deleteTree_definiendumType_definiendumAST = get_deleteTree_definiendumType_definiendumAST(ast_statement, preprocessingInterface.makeNameGfConform(definiendum))
        if deleteTree_definiendumType_definiendumAST is None: 
            print("Error: deleteTree_and_definiendumType_definiendumAST == None")
            continue
        [tree_delete, type_definiendum, ast_definiendum] = deleteTree_definiendumType_definiendumAST

        #FROM DEFINITION: Get definition sentence trees
        cmd_parseDefinition = 'parse "' + definition + '"'
        tree_definition_all = shell.handle_command(cmd_parseDefinition)

        #Loop to handle multiple definition trees 
        tree_definitions = tree_definition_all.split('\n')
        for j in range(len(tree_definitions)):
            tree_definition = tree_definitions[j]

            #IN DEFINITION: Alpha-Renaming of variables, which also appear in the statement 
            [tree_definition, new_newIntroducedVariables] = alphaRenamingOfVariables(variablesDefinition, variablesStatement, tree_definition) 
            newIntroducedVariables.extend(new_newIntroducedVariables)
            ast_definition = GfAst.from_str(tree_definition)

            #HANDLE DEFINITION SENTENCE
            #Get content of "definiens [ ... ]"
            tree_definiensContent = get_definiensContentTree(ast_definition, definiendum, preprocessingInterface.makeNameGfConform(type_definiendum))
            if tree_definiensContent is None: 
                print("Error: tree_definiensContent == None")
                continue

            #CREATE REPLACEMENT TREE (MODIFIED DEFINIENS CONTENT) (depends on tree_delete)
            tree_replacement = get_replacementTree(tree_delete, tree_definiensContent, ast_definiendum)
            if tree_replacement is None: 
                print("Error: tree_replacement == None")
                continue

            #IN REPLACEMENT: Assign the corresponding variables from the statement
            ast_definition_without_definiens = GfAst.from_str(tree_definition.replace(tree_definiensContent, "R_DEFINIENS_CONTENT"))
            varRenaming = assignedVariableRenaming(tree_replacement, ast_definition_without_definiens, ast_statement, definiendum)
            tree_replacement = varRenaming[0] #Definition Baum mit ersetzen Variablen
            #TODO: TODOTODO Abbrechen, falls Variablen nicht passen?

            #Construct new tree
            tree_result = None
            tree_result = tree_statement.replace(tree_delete, tree_replacement)
            introducedVariables.append(newIntroducedVariables)
            print(f"\nDelete Tree:\n{tree_delete}\n\nReplace Tree:\n{tree_replacement}")
            print(f"\nTree of Definition:\n{tree_definition}\n\nOG Tree of Statement:\n{og_tree_statement}\n\nTree of Statement:\n{tree_statement}\n\nResult Tree:\n{tree_result}\n\n-----\n")
            
            return tree_result

def linearizeTree(shell: gf.GFShellRaw, tree: GfAst) -> str:
    """Linearizes an AST to a sentence through the grammar, which got loaded in the Grammatical Framework shell."""
    cmd_linearize = 'linearize ' + str(tree)
    linearizedTree = shell.handle_command(cmd_linearize)
    res_sentence = preprocessingInterface.uppercase_first_letter(linearizedTree)
    return res_sentence
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Main -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
#Input: Definition, Statement and Definiendum
def main(symname_uri: str, statement_id_uri: str, definiendum: str, stexOutput: bool) -> str:
    #HANDLE THE INPUT OF THE PREPROCESSOR
    input_str = preprocessingInterface.getInformation_defExp(symname_uri, statement_id_uri)
    input = json.loads(input_str)

    #Initialize variables
    input_variables_definition = []
    input_variables_statement = []
    og_definition = None
    og_statement = None
    macros = None
    all_commands_structure = []
    all_commands_math = []
    all_commands_text = []
    all_commands_symbolname = []

    # Iterate through the input list
    for item in input:
        # Check for 'definition' in the current dictionary
        if 'definition' in item:
            temp_input_variables_definition = item['definition']['variables']
            for temp_v in temp_input_variables_definition:
                input_variables_definition.append(temp_v["variable"])
            og_definition = item['definition']['sentence']
        
        # Check for 'statement' in the current dictionary
        if 'statement' in item:
            temp_input_variables_statement = item['statement']['variables']
            for temp_v in temp_input_variables_statement:
                input_variables_statement.append(temp_v["variable"])
            og_statement = item['statement']['sentence']
        
        # Check for 'macros' (assumed to be in the list as well)
        if 'macros' in item:
            macros = item['macros']

            # If macros exist, classify them into different categories
            for macro in macros:
                if "structure command" in macro:
                    all_commands_structure.append(macro["structure command"])
                if "math command" in macro:
                    all_commands_math.append(macro["math command"])
                if "text command" in macro:
                    all_commands_text.append(macro["text command"])
                if "symbol name" in macro:
                    all_commands_symbolname.append(macro["symbol name"])

    # If macros are not directly in the 'input', but part of the nested structure
    if macros is None:
        for sublist in input:
            if isinstance(sublist, list):
                for item in sublist:
                    if 'Module' in item and 'commands' in item['Module']:
                        for macro in item['Module']['commands']:
                            if "structure command" in macro:
                                all_commands_structure.append(macro["structure command"])
                            if "math command" in macro:
                                all_commands_math.append(macro["math command"])
                            if "text command" in macro:
                                all_commands_text.append(macro["text command"])
                            if "symbol name" in macro:
                                all_commands_symbolname.append(macro["symbol name"])

    gg_vars = input_variables_definition
    gg_vars.extend(input_variables_statement)
    definition = preprocessingInterface.make_sentence_GfConform(og_definition)
    statement = preprocessingInterface.make_sentence_GfConform(og_statement)

    special_variables = []
    grammarGenerator.generateGrammar(gg_vars, special_variables, all_commands_structure, all_commands_math, all_commands_text, all_commands_symbolname)

    #Initialize GF
    shell = gf.GFShellRaw(PATH_exe_gf)
    print(shell.handle_command(f"import {PATH_gf_concrGrammar}"))

    #Expand definitions
    result_mergedTree = expandDefinitions(definition, statement, definiendum, input_variables_definition, input_variables_statement, shell)

    #Generate grammar with new variables and initialize GF again
    newVars = flatten_list_of_lists(introducedVariables)
    if (newVars != []):
        gg_vars.extend(newVars)
        shell.do_shutdown()
        grammarGenerator.generateGrammar(gg_vars, special_variables, all_commands_structure, all_commands_math, all_commands_text, all_commands_symbolname)
        shell = gf.GFShellRaw(PATH_exe_gf)
        shell.handle_command(f"import {PATH_gf_concrGrammar}")

    #Linearize the merged tree
    result_sentence = str(linearizeTree(shell, result_mergedTree))

    #Postprocess sentence
    result_sentence_postprocessed = preprocessingInterface.postprocessSentence(result_sentence)
    print("\nPostprocessed sentence: " + str(result_sentence_postprocessed))

    #Generate stex output file
    if stexOutput:
        stexGenerator.main(newVars, og_statement, result_sentence_postprocessed, symname_uri, statement_id_uri)

    return result_sentence_postprocessed
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###