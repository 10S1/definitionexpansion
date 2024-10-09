###----- Imports --------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
import json
import random
import string
import regex as re
import shutil
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Resources')))

import subprocess
import grammarGenerator
import gf as gf
from gf_ast import GfAst
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Parameters -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
#Length of the names, which are generated for new or renamed variables
length_randomVariablenames = 20

#If false: The output is the merged sentence.
#If true: Additionally, a sTeX file gets generated.
#   The generateds file is the file, in which the sentence, which Statement URI refers to, occurs. However, in the file
#   the sentence itself is replaced by the new merged sentence and necessary commands from the Definition URI file are added.
active_stexOutput = False
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Input ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
#Choose an example from FDE_examples.json or set input_definiendum, symname_uri and statement_id_uri directly.
with open('sTeX\FDE_examples.json', 'r') as file:
        FDE_example = json.load(file)
VARIABLE_choosenExample = "2-5"

input_definiendum = FDE_example[VARIABLE_choosenExample]["input_definiendum"]
symname_uri = FDE_example[VARIABLE_choosenExample]["symname_uri"]
statement_id_uri = FDE_example[VARIABLE_choosenExample]["statement_id_uri"]
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Paths ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
PATH_exe_preprocessor = os.getenv('PP_EXE')
if PATH_exe_preprocessor is None:
    print("ERROR: Path to relocate.exe not found. \nCheck whether the Preprocessor is installed and the environment variable is set.")

PATH_exe_gf = os.getenv('GF_EXE')
if PATH_exe_gf is None:
    print("ERROR: Path to gf.exe not found. \nCheck whether the Grammatical Framework is installed and the environment variable is set.")

PATH_dict_mathhub = os.getenv('MATHHUB')
if (PATH_dict_mathhub is None) or (not os.path.isdir(PATH_dict_mathhub)):
    print("ERROR: Path to MathHub not found. \nCheck whether the SMGloM is installed and the environment variable is set.")
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Variables ------------------------------------------------------------------------------------------------------------------------------------------------------------------#-----###
#Paths where the base grammar (= the grammar which gets extended by additonally generated rules) is placed.
PATH_gf_grammar = r'definitionexpansion\sTeX/Grammar/'
basename = r"definitionexpansion\sTeX\Grammar\BaseGrammar"

#Variables which are introduced during merging or renamed.
introducedVariables = []

#Paths where the generated grammars will be placed.
PATH_gf_concrGrammar = 'definitionexpansion\sTeX\Grammar\GEN_grammar_concr.gf'
PATH_gf_abstrGrammar = 'definitionexpansion\sTeX\Grammar\GEN_grammar_abstr.gf'
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Irrelevant Functions -------------------------------------------------------------------------------------------------------------------------------------------------------------###
def flatten_list_of_lists(nested_lists):
    return [item for sublist in nested_lists for item in sublist]
def lowercase_first_letter(s: str) -> str:
    if s and s[0].isupper():
        return s[0].lower() + s[1:]
    return s
def uppercase_first_letter(s: str) -> str:
    if s and s[0].islower():
        return s[0].upper() + s[1:]
    return s
def read_file_with_fallback(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            return f.read()

#Replaces symbols, which are not allowed to appear in the names of the GF rules.
def makeNameGfConform(name):
    name = re.sub(r"\!", "Exlamation", name)
    name = re.sub(r"\?", "Questionmark", name)
    name = re.sub(r"\.", "Point", name)
    name = re.sub(r"\-", "Dash", name)
    name = re.sub(r"\{", "LeftCurlyBracket", name)
    name = re.sub(r"\}", "RightCurlyBracket", name)
    name = re.sub(r"\[", "LeftSquareBracket", name)
    name = re.sub(r"\]", "RightSquareBracket", name)
    name = re.sub(r"\(", "LeftParenthesis", name)
    name = re.sub(r"\)", "RightParenthesis", name)
    name = re.sub(r"\ ", "Space", name)
    name = re.sub(r"\\", "Slash", name)
    name = re.sub(r"[^A-Za-z0-9]", "OtherSymbol", name) 
    return name

#Adds spaces for postprocessing the result sentence.
def format_math_expressions(text):
    return re.sub(r'\$(.*?)\$', lambda m: "$" + m.group(1).replace(" ", "") + "$", text)

#Adds spaces around dollar signs for postprocessing the result sentence.
def adjust_dollar_sign_spacing(sentence):
    parts = sentence.split('$')
    new_sentence = ''

    for i in range(len(parts)):
        if i % 2 == 0:
            # Part before the dollar sign
            if parts[i].endswith(' '):
                part = parts[i][:-1]  # Remove only the last space if it's before a closing dollar sign
            else:
                part = parts[i]
        else:
            # Part after the dollar sign
            if parts[i].startswith(' '):
                part = parts[i][1:]  # Remove only the first space if it's after an opening dollar sign
            else:
                part = parts[i]

        # Reattach the dollar sign except for the last part
        if i < len(parts) - 1:
            new_sentence += part + '$'
        else:
            new_sentence += part

    return new_sentence

#Generates a string in the format of: "X_" + <number>
def random_variable_name(number):
    return 'X_' + ''.join(random.choice(string.digits) for _ in range(number))
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Helper Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------###
#Renames variables in the definition sentence/AST if they also appear in the statement sentence/AST.
def alphaRenamingOfVariables(variables_definition, variables_statement, tree_definition):
    newIntroducedVariables = []
    for var in variables_definition:
        if var in variables_statement:
            #Generate cryptic (= hopefully not already existing) variable name
            newVar = {'name': "\\" + str(random_variable_name(length_randomVariablenames)), 'parameters': var["parameters"]}
            tree_definition.replace(var["name"], newVar["name"])
            newIntroducedVariables.append(newVar)
    return [tree_definition, newIntroducedVariables]

#Extracts variables out of an AST if they occur after a preposition.
def get_varsOfPrepositions(ast):
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

#Extracts variables and their category (e.g. "main", "from", "to", ...) out of the definitions AST.
def get_assignedVariables_definition(ast, definiendum):
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

#Extracts variables and their category (e.g. "main", "from", "to", ...) out of the statement AST.
def get_assignedVariables_statement(ast, definiendum):
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

#The variables in the statement and the definition, which can be assigned to each other, get accordingly replaced in the definition AST.
def assignedVariableRenaming(tree_replacement, tree_definition_without_definiens, tree_statement, definiendum):
    replaceVar_dict = {}   #E.g. like: ["main", "xVar"], ["from", "yVar"]

    ast_definition = GfAst.from_str(tree_definition_without_definiens)
    ast_statement = GfAst.from_str(tree_statement)
    vars_definition = get_assignedVariables_definition(ast_definition, definiendum)
    vars_statement = get_assignedVariables_statement(ast_statement, definiendum)
    print("\nvars_definition: " + str(vars_definition))
    print("\nvars_statement: " + str(vars_statement))
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

#If there is a noun in the statement sentence, which is [connected to] the definiendum, a variable gets introduced after it.
def introduceVariables(ast, definiendum):
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
                        rulename = "G_variable_VAR" + makeNameGfConform(newVar["name"][1:])
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


#PREPROCESSOR STUFF
#Uses the Preprocessor to add spaces to a normal sTeX sentence, so it can be parsed by the Grammatical Framework.
def pp_preprocessString(input_string):
    executable_path = PATH_exe_preprocessor
    command = [executable_path, '--mode=gf', f'--input={input_string}']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

#Uses the Preprocessor to fetch the used variables and commands, which could be used in the SMGloM files, which the URIs refer to.
def pp_getInformation(symname_uri, statement_id_uri):
    executable_path = PATH_exe_preprocessor
    command = [executable_path, '--mode=def-exp', f'--mathhub={PATH_dict_mathhub}', f'--symname={symname_uri}', f'--statement={statement_id_uri}']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

#Brings a normal sentence into a format, which is parsable by the generated grammar, which is used in the Grammatical Framework.
def make_sentence_GfConform(sentence):
    sentence_pp = pp_preprocessString(sentence)
    sentence_pp = lowercase_first_letter(sentence_pp).replace("\\", "\\\\")
    sentence_pp = sentence_pp.strip()
    if sentence_pp.endswith(" ."):
        sentence_pp = sentence_pp[:-2]
    sentence_pp = sentence_pp.strip()
    sentence_pp = lowercase_first_letter(sentence_pp)
    return sentence_pp

#Brings a sentence, which is in a format, which is parsable by the Grammatical Framework, back to a normal format.
def postprocessSentence(sentence):
    sentence = (uppercase_first_letter(sentence).replace("\\\\", "\\")) + "."
    sentence = sentence.replace("{ ", "{")
    sentence = sentence.replace(" {", "{")
    sentence = sentence.replace(" }", "}")
    sentence = format_math_expressions(sentence)
    return sentence

#Brings a sentence, which is in a format, which is parsable by the Grammatical Framework, back to a normal format.
#   Special case, which is necessary for finding the sentences, which need to be replaced while generating the sTeX file.
def postprocessSentence_onlyremoveSpaces(sentence):
    sentence = sentence.replace("{ ", "{")
    sentence = sentence.replace(" {", "{")
    sentence = sentence.replace(" }", "}")
    sentence = format_math_expressions(sentence)
    sentence = sentence.replace("  ", " ")
    sentence = sentence.replace(" .", ".")
    sentence = sentence.strip()
    return sentence


#AST STUFF
#Generates the AST, which will replace the delete AST in the statement AST.
def get_replacementTree(deletedTree, definiensContentTree, definiendumAst):
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

#Extracts the AST of the definiendum and the part of speech category of the definiendum.
def get_definiendumAST_definiendumType(ast, definiendum):
    definiendum = makeNameGfConform(definiendum)
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

#Extracts the AST in the definiens command of the definiendum out of the definition AST.
def get_definiensContentTree(ast_definition, definiendum, definiendum_type):
    # E.g.: "$ \\\\nvar $ is \\\\definame { positive } iff \\\\definiens [ positive ] { $ \\\\intmorethan { \\\\nvar } { 0 } $ } ."
    definiendum = makeNameGfConform(definiendum)
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

#Returns the tree, which will be removed out of the statement AST (usually is or contains the definiendum) and the  part of 
#speech category of the definiendum and the AST of the definiendum.
def get_deleteTree_definiendumType_definiendumAST(ast_statement, definiendum_gfCon):
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

        case GfAst("AdjCN", [GfAst("PositA", [defi_2]), rest]):
            print("TEST3")
            definiendumAST_definiendumType2 = get_definiendumAST_definiendumType(defi_2, definiendum_gfCon)
            if definiendumAST_definiendumType2 != None:
                [definiendumAST, definienumType] = definiendumAST_definiendumType2
                if defi_2 == definiendumAST:
                    return [GfAst("AdjCN", [GfAst("PositA", [defi_2]), rest]).to_str(), definienumType, definiendumAST.to_str()]

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


#sTeX STUFF
#Extracts the importmodule, usemodel and symdecl lines out of a sTeX file.
def extract_latex_commands(latex_str):
    output = []

    #Remove \vardef commands if they are defined in the definition/assertion
    # Pattern to match \vardef commands
    vardef_pattern = r"\\vardef\{(.*?)\}\{(.*?)\}"
    # Find all matches in the input string
    matches = re.findall(vardef_pattern, latex_str)
    # Create the formatted output list
    for match in matches:
        arg1, arg2 = match
        output.append("\\vardef{" + arg1 + "}{" + arg2 + "}")

    # Pattern to match \usemodel and \importmodule commands
    command_pattern = r'\\(importmodule|usemodel|symdecl\*)(\[[^\]]*\])?\{([^}]+)\}'
    # Find all matches in the input string
    matches = re.findall(command_pattern, latex_str)
    # Create the formatted output list
    for match in matches:
        cmd, options, body = match
        if options:
            output.append(f"\\{cmd}{options}{{{body}}}")
        else:
            output.append(f"\\{cmd}{{{body}}}")

    return output

#Generates a sTeX file, which is the statement sTeX file, in which the original sentences are replaced by the merged sentences 
#and additonal lines are added for newly introduced variables and the relevant lines from the definition sTeX file are added.
def generate_stexFile(input_stex_definition, input_stex_statement, replacedSentences, newVariables):
    output_stex = input_stex_statement
    newLines = ""

    #Add lines for new intruduced variables
    for newVariable in newVariables:
        newVariable = newVariable.replace("\\", "")
        newLines = newLines + "\\vardef{" + newVariable + "}{" + newVariable.replace("var", "") + "}\n"

    #Add lines copied from the definition-stex-file
    extractedLines = extract_latex_commands(input_stex_definition)
    temp_newLines = '\n'.join(str(line) for line in extractedLines)
    newLines = newLines + temp_newLines
    newLines_split = newLines.splitlines()

    # Processing output_stex
    lines = output_stex.splitlines()
    for i in range(len(lines)):
        if "begin{smodule}" in lines[i]:
            # Properly inserting newLines_split into lines
            lines = lines[:i+1] + newLines_split + lines[i+1:]
            break  # Assuming you only want to insert once

    # Joining lines back into a string with proper line endings
    output_stex = '\r\n'.join(lines)

    #TODO: Insert after \begin{smodule}[creators=generated,title={hasCountableModel}]{hasCountableModel}

    #Replace sentences, which got extended
    for replacedSentence in replacedSentences:
        output_stex = output_stex.replace(replacedSentence, replacedSentences[replacedSentence])

    return output_stex

#Fetches the content of the SMGloM file, in which the URI appears.
def get_stexfile(uri):
    file_path = uri.replace("/mod", "/source/mod")
    file_path = file_path.replace("http://mathhub.info/smglom", "bachelor_arbeit/Resources/smglomRessources/smglom")
    file_path = file_path.replace("/", "\\")
    file_path = file_path.split("?")[0] 
    file_path = file_path + ".en.tex"
    file_path = file_path.replace(".en.en", ".en")
    file_path = file_path.replace("\defexp", "\defexp\source\def")
    file_content = read_file_with_fallback(file_path)
    return file_content
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Functions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
#Replaces the definiendum in the statement by the definiens content in the definition while keeping a correct sytax and adapting 
#the variables. Returns an AST.
def expandDefinitions(definition, statement, definiendum, variablesDefinition, variablesStatement, shell):
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
        deleteTree_definiendumType_definiendumAST = get_deleteTree_definiendumType_definiendumAST(ast_statement, makeNameGfConform(definiendum))
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
            tree_definiensContent = get_definiensContentTree(ast_definition, definiendum, makeNameGfConform(type_definiendum))
            if tree_definiensContent is None: 
                print("Error: tree_definiensContent == None")
                continue

            #CREATE REPLACEMENT TREE (MODIFIED DEFINIENS CONTENT) (depends on tree_delete)
            tree_replacement = get_replacementTree(tree_delete, tree_definiensContent, ast_definiendum)
            if tree_replacement is None: 
                print("Error: tree_replacement == None")
                continue

            #IN REPLACEMENT: Assign the corresponding variables from the statement
            tree_definition_without_definiens = tree_definition.replace(tree_definiensContent, "R_DEFINIENS_CONTENT")
            varRenaming = assignedVariableRenaming(tree_replacement, tree_definition_without_definiens, tree_statement, definiendum)
            tree_replacement = varRenaming[0] #Definition Baum mit ersetzen Variablen
            #TODO: TODOTODO Abbrechen, falls Variablen nicht passen?

            #Construct new tree
            tree_result = None
            tree_result = tree_statement.replace(tree_delete, tree_replacement)
            introducedVariables.append(newIntroducedVariables)
            print(f"\nDelete Tree:\n{tree_delete}\n\nReplace Tree:\n{tree_replacement}")
            print(f"\nTree of Definition:\n{tree_definition}\n\nOG Tree of Statement:\n{og_tree_statement}\n\nTree of Statement:\n{tree_statement}\n\nResult Tree:\n{tree_result}\n\n-----\n")
            
            return tree_result

#Linearizes an AST to a sentence through the grammar, which got loaded in the Grammatical Framework shell.
def linearizeTree(shell, tree):
    cmd_linearize = 'linearize ' + str(tree)
    linearizedTree = shell.handle_command(cmd_linearize)
    res_sentence = uppercase_first_letter(linearizedTree)
    return res_sentence
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Main -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
#Input: Definition, Statement and Definiendum
def main(symname_uri, statement_id_uri, definiendum):

    #HANDLE THE INPUT OF THE PREPROCESSOR
    input_str = pp_getInformation(symname_uri, statement_id_uri)
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
    definition = make_sentence_GfConform(og_definition)
    statement = make_sentence_GfConform(og_statement)

    special_variables = []
    grammarGenerator.generateGrammar(basename, gg_vars, special_variables, all_commands_structure, all_commands_math, all_commands_text, all_commands_symbolname, PATH_gf_grammar)

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
        grammarGenerator.generateGrammar(basename, gg_vars, special_variables, all_commands_structure, all_commands_math, all_commands_text, all_commands_symbolname, PATH_gf_grammar)
        shell = gf.GFShellRaw(PATH_exe_gf)
        shell.handle_command(f"import {PATH_gf_concrGrammar}")

    #Linearize the merged tree
    result_sentence = str(linearizeTree(shell, result_mergedTree))

    #Postprocess sentence
    result_sentence_postprocessed = postprocessSentence(result_sentence)
    print("\nPostprocessed sentence: " + str(result_sentence_postprocessed))

    #Generate stex output file
    if active_stexOutput:
        newVariables = [item['name'] for item in newVars]
        replacedSentences = {postprocessSentence_onlyremoveSpaces(og_statement): result_sentence_postprocessed}
        input_stex_definition = get_stexfile(symname_uri)
        input_stexStatement = get_stexfile(statement_id_uri)
        result_stex_output = generate_stexFile(input_stex_definition, input_stexStatement, replacedSentences, newVariables)
        name_outputStex = "generatedOutput.en.tex"
        with open("bachelor_arbeit\DefinitionExpansion_stexOutput\\" + name_outputStex, 'w') as gf_file:
            gf_file.write(result_stex_output)

    return result_sentence_postprocessed
  
output = main(symname_uri, statement_id_uri, input_definiendum)
print("\nOutput: " + str(output))
print("\nDONE.")
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###