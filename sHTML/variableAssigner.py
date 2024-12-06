import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Resources')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../gfxml')))
import gf
import gfxml
import shutil 
import re
import spacy
from spacy import displacy
nlp_en = spacy.load("en_core_web_sm")



###----- Paths ------------------------------------------------------------------------------------------------------------------------------------------###
PATH_exe_gf = shutil.which('gf')
if PATH_exe_gf is None:
    print("ERROR: Path to gf.exe not found. \nCheck whether the Grammatical Framework is installed and the environment variable is set.")
PATH_gf_concrGrammar = "sHTML\Grammar\BaseGrammar_concr.gf"
###------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Helper functions -------------------------------------------------------------------------------------------------------------------------------###
def uppercase_first_letter(s: str) -> str:
    if s and s[0].islower():
        return s[0].upper() + s[1:]
    return s

def postprocessSentence(sentence: str) -> str:
    """Brings a sentence, which is in a format, which is parsable by the Grammatical Framework, back to a normal format."""
    sentence = (uppercase_first_letter(sentence).replace("\\\\", "\\")) + "."
    return sentence

def transform_string(input_string):
    # Remove <x> und </x>, if x is a number
    input_string = re.sub(r"< (\d+) >(.*?)</ \1 >", lambda m: m.group(2).strip(), input_string)

    # Replace <m x> and </m x> through formula_x
    input_string = re.sub(r"<m (\d+) >\s*</m \1 >", r"formula_\1", input_string)

    return input_string

def tree_to_sentence(shell, tree):
    recovery_info, gf_input = tree.to_gf()
    #print("\ngf_input: " + str(gf_input))
    #print("\nrecovery_info: " + str(recovery_info))
    gf_lin = shell.handle_command(f'linearize {gf_input}')
    #print("\ngf_lin: " + str(gf_lin)
    return gf_lin, recovery_info
###------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Functions --------------------------------------------------------------------------------------------------------------------------------------###
def get_sentences(statement_tree, definition_tree, definiensContent_tree):
    #Initialize GF shell
    shell = gf.GFShellRaw(PATH_exe_gf)
    print(shell.handle_command(f"import {PATH_gf_concrGrammar}"))

    statement_sntc, statement_recovery = tree_to_sentence(shell, statement_tree)
    definition_sntc, definition_recovery = tree_to_sentence(shell, definition_tree)
    definiensContent_sntc, definiensContent_recovery = tree_to_sentence(shell, definiensContent_tree)

    statement_sntc = transform_string(postprocessSentence(statement_sntc))
    definition_sntc = transform_string(postprocessSentence(definition_sntc))
    definiensContent_sntc = transform_string(definiensContent_sntc)

    statement_formulas = {}
    for i in range(0, len(statement_recovery)):
        name = "formula_" + str(i)
        if name in statement_sntc:
            statement_formulas[name] = statement_recovery[i]
    
    definition_formulas = {}
    for i in range(0, len(definition_recovery)):
        name = "formula_" + str(i)
        if name in definition_sntc:
            definition_formulas[name] = definition_recovery[i]

    definiensContent_formulas = {}
    for i in range(0, len(definiensContent_recovery)):
        name = "formula_" + str(i)
        if name in definiensContent_sntc:
            definiensContent_formulas[name] = definiensContent_recovery[i]

    return statement_sntc, definition_sntc, definiensContent_sntc, statement_formulas, definition_formulas, definiensContent_formulas

def match_formulas_by_context(statement_formulas, definition_formulas):
    """Matches formulas based on dependency roles and context."""
    matches = {}
    for stmt_formula in statement_formulas:
        best_match = None
        highest_score = -1

        for def_formula in definition_formulas:
            score = 0
            if stmt_formula["dependency"] == def_formula["dependency"]:
                score += 2
            if stmt_formula["head"] == def_formula["head"]:
                score += 3
            # Compare subtree overlap
            stmt_subtree = set(stmt_formula["subtree"])
            def_subtree = set(def_formula["subtree"])
            score += len(stmt_subtree.intersection(def_subtree))
            
            # Update the best match
            if score > highest_score:
                highest_score = score
                best_match = def_formula

        matches[stmt_formula["text"]] = best_match["text"] if best_match else None
    return matches

def get_assignedVariables(statement_tree, definition_tree, definiensContent_tree):
    
    statement_sntc, definition_sntc, definiensContent_sntc, statement_formulas, definition_formulas, definiensContent_formulas = get_sentences(statement_tree, definition_tree, definiensContent_tree)

    statement_doc = nlp_en(statement_sntc)
    statement_dependencies = [
        {
            "text": token.text,
            "lemma": token.lemma_,
            "lower": token.lower_,
            "shape": token.shape_,
            "is_alpha": token.is_alpha,
            "is_stop": token.is_stop,
            "pos": token.pos_,
            "tag": token.tag_,
            "morph": token.morph,
            "dependency": token.dep_,
            "head": token.head.text,
            "children": [child.text for child in token.children],
            "ancestors": [ancestor.text for ancestor in token.ancestors],
            "subtree": [sub_token.text for sub_token in token.subtree]
        }
        for token in statement_doc
    ]
    definition_doc = nlp_en(definition_sntc)
    definition_dependencies = [
        {
            "text": token.text,
            "lemma": token.lemma_,
            "lower": token.lower_,
            "shape": token.shape_,
            "is_alpha": token.is_alpha,
            "is_stop": token.is_stop,
            "pos": token.pos_,
            "tag": token.tag_,
            "morph": token.morph,
            "dependency": token.dep_,
            "head": token.head.text,
            "children": [child.text for child in token.children],
            "ancestors": [ancestor.text for ancestor in token.ancestors],
            "subtree": [sub_token.text for sub_token in token.subtree]
        }
        for token in definition_doc
    ]

    statement_dependencies_formulas = [dep for dep in statement_dependencies if re.match(r"formula_\d+", dep["text"])] 
    definition_dependencies_formulas = [dep for dep in definition_dependencies if re.match(r"formula_\d+", dep["text"])]

    #For debugging
    # print("\nstatement_tree: " + str(statement_tree))
    # print("\ndefinition_tree: " + str(definition_tree))
    # print("\ndefiniensContent_tree: " + str(definiensContent_tree))

    print("\nstatement_sntc: " + str(statement_sntc))
    print("\ndefinition_sntc: " + str(definition_sntc))
    print("\ndefiniensContent_sntc: " + str(definiensContent_sntc))

    print("\nstatement_formulas: " + str(statement_formulas))
    print("\ndefinition_formulas: " + str(definition_formulas))
    print("\ndefiniensContent_formulas: " + str(definiensContent_formulas))

    print("\nstatement_dependencies: " + str(statement_dependencies))
    print("\ndefinition_dependencies: " + str(definition_dependencies))

    print("\nstatement_dependencies_formulas: " + str(statement_dependencies_formulas))
    print("\ndefinition_dependencies_formulas: " + str(definition_dependencies_formulas))

    statement_doc_html = displacy.render(statement_doc, style='dep', page=True)
    with open('dependency_statement.html', 'w', encoding='utf-8') as file:
        file.write(statement_doc_html)
    definition_doc_html = displacy.render(definition_doc, style='dep', page=True)
    with open('dependency_definition.html', 'w', encoding='utf-8') as file:
        file.write(definition_doc_html)

    ###
    aligned_formulas = match_formulas_by_context(statement_dependencies_formulas, definition_dependencies_formulas) 
    print("\naligned_formulas: " + str(aligned_formulas))

    aligned_variables = {}
    for formula in aligned_formulas:
        var_statement = statement_formulas[formula]
        var_definition = definition_formulas[aligned_formulas[formula]]
        aligned_variables[var_definition] = var_statement
    print("\naligned_variables: " + str(aligned_variables))

    return aligned_variables
###------------------------------------------------------------------------------------------------------------------------------------------------------###



def test():
    statement_tree = gfxml.G('let_np_be_np_S', [gfxml.G('formula_NP', [gfxml.X('math', [gfxml.X('mi', [gfxml.XT('m')], {}, None)], {}, 'wrap_math')]), gfxml.G('DetCN', [gfxml.G('DetQuant', [gfxml.G('IndefArt', []), gfxml.G('NumSg', [])]), gfxml.G('AdjCN', [gfxml.G('PositA', [gfxml.X('span', [gfxml.G('positive_A', [])], {'data-symref': 'http://example.org/arith?positive'}, 'WRAP_A')]), gfxml.G('UseN', [gfxml.X('span', [gfxml.G('integer_N', [])], {'data-symref': 'http://example.org/arith?integer'}, 'WRAP_N')])])])])
    definition_tree = gfxml.G('UseCl', [gfxml.G('TTAnt', [gfxml.G('TPres', []), gfxml.G('ASimul', [])]), gfxml.G('PPos', []), gfxml.G('PredVP', [gfxml.G('formula_NP', [gfxml.X('math', [gfxml.X('mi', [gfxml.XT('n')], {}, None)], {}, 'wrap_math')]), gfxml.G('UseComp', [gfxml.G('CompNP', [gfxml.G('ConjNP', [gfxml.G('iff_Conj', []), gfxml.G('BaseNP', [gfxml.G('MassNP', [gfxml.G('ApposCN', [gfxml.G('UseN', [gfxml.X('span', [gfxml.G('positive_N', [])], {'data-definiendum': 'http://example.org/arith?positive'}, 'WRAP_N')]), gfxml.G('DetNP', [gfxml.G('DetQuant', [gfxml.G('IndefArt', []), gfxml.G('NumPl', [])])])])]), gfxml.X('span', [gfxml.G('', [gfxml.G('formula_NP', [gfxml.X('math', [gfxml.X('mrow', [gfxml.X('mi', [gfxml.XT('n')], {}, None), gfxml.X('mo', [gfxml.XT('>')], {}, None), gfxml.X('mn', [gfxml.XT('0')], {}, None)], {}, None)], {}, 'wrap_math')])])], {'data-definiens-of': 'http://example.org/arith?positive'}, 'WRAP_NP')])])])])])])
    definiensContent_tree = gfxml.X('span', [gfxml.G('', [gfxml.G('formula_NP', [gfxml.X('math', [gfxml.X('mrow', [gfxml.X('mi', [gfxml.XT('n')], {}, None), gfxml.X('mo', [gfxml.XT('>')], {}, None), gfxml.X('mn', [gfxml.XT('0')], {}, None)], {}, None)], {}, 'wrap_math')])])], {'data-definiens-of': 'http://example.org/arith?positive'}, 'WRAP_NP')
    
    get_assignedVariables(statement_tree, definition_tree, definiensContent_tree)


test()