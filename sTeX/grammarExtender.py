import grammarGenerator
import preprocessingInterface
import json
from typing import List, Any, Tuple, Dict

def generate_grammar(folders: List[Any]):
    dictionary_fileSentences = {}
    all_variables = []
    all_commands_structure = []
    all_commands_math = []
    all_commands_text = []
    all_commands_symbolname = []
    for folder in folders:
        print("New folder started.")
        for file_path in folder["filepaths"]:
            file_uri = file_path.replace("\\", "/")
            tmp_parts = file_uri.split("/smglom", 1)
            file_uri = tmp_parts[1]
            file_uri = "http://mathhub.info/smglom" + file_uri
            file_uri = file_uri.replace("/source", "")
            file_uri = file_uri.replace(".tex", "")
            text_information_str = preprocessingInterface.getInformation(file_uri)
            if text_information_str == None:
                print("Not preprocessed: " + file_uri)
            else:
                text_information = json.loads(text_information_str)
                file_sentences = []

                for item in text_information:
                    for entry in item:
                        if 'Module' in entry:
                            amfc = entry['Module']
                            commands = amfc.get('commands', [])
                            for macro in commands:
                                if 'structure command' in macro:
                                    all_commands_structure.append(macro["structure command"])
                                if 'math command' in macro:
                                    all_commands_math.append(macro["math command"])
                                if 'text command' in macro:
                                    all_commands_text.append(macro["text command"])
                                #if 'symbol name' in macro:
                                    #all_symbol_names.append(macro["symbol name"])
                    for entry in item:
                        if 'statement' in entry:
                            statement = entry['statement']
                            for temp_v in statement['variables']:
                                if 'variable' in temp_v:
                                    all_variables.append(temp_v['variable'])
                                if 'sequence' in temp_v:
                                    all_variables.append(temp_v['sequence'])
                            file_sentences.append(statement['sentence'])

                dictionary_fileSentences[file_path] = file_sentences

    #ADD UNDECLARED VARIABLES (TODO: Add undecleared variables by extracting them out of the input: "$" + _ + "$")
    special_variables = []
    #Add $ A $, B and so on...
    special_variables.extend([{'name': 'A', 'parameters': [], 'notation': 'A'}, {'name': 'B', 'parameters': [], 'notation': 'B'}, {'name': 'C', 'parameters': [], 'notation': 'C'}, {'name': 'D', 'parameters': [], 'notation': 'D'}, {'name': 'E', 'parameters': [], 'notation': 'E'}, {'name': 'F', 'parameters': [], 'notation': 'F'}, {'name': 'G', 'parameters': [], 'notation': 'G'}, {'name': 'H', 'parameters': [], 'notation': 'H'}, {'name': 'I', 'parameters': [], 'notation': 'I'}, {'name': 'J', 'parameters': [], 'notation': 'J'}, {'name': 'K', 'parameters': [], 'notation': 'K'}, {'name': 'L', 'parameters': [], 'notation': 'L'}, {'name': 'M', 'parameters': [], 'notation': 'M'}, {'name': 'N', 'parameters': [], 'notation': 'N'}, {'name': 'O', 'parameters': [], 'notation': 'O'}, {'name': 'P', 'parameters': [], 'notation': 'P'}, {'name': 'Q', 'parameters': [], 'notation': 'Q'}, {'name': 'R', 'parameters': [], 'notation': 'R'}, {'name': 'S', 'parameters': [], 'notation': 'S'}, {'name': 'T', 'parameters': [], 'notation': 'T'}, {'name': 'U', 'parameters': [], 'notation': 'U'}, {'name': 'V', 'parameters': [], 'notation': 'V'}, {'name': 'W', 'parameters': [], 'notation': 'W'}, {'name': 'X', 'parameters': [], 'notation': 'X'}, {'name': 'Y', 'parameters': [], 'notation': 'Y'}, {'name': 'Z', 'parameters': [], 'notation': 'Z'}])
    special_variables.extend([{'name': 'a', 'parameters': [], 'notation': 'a'}, {'name': 'b', 'parameters': [], 'notation': 'b'}, {'name': 'c', 'parameters': [], 'notation': 'c'}, {'name': 'd', 'parameters': [], 'notation': 'd'}, {'name': 'e', 'parameters': [], 'notation': 'e'}, {'name': 'f', 'parameters': [], 'notation': 'f'}, {'name': 'g', 'parameters': [], 'notation': 'g'}, {'name': 'h', 'parameters': [], 'notation': 'h'}, {'name': 'i', 'parameters': [], 'notation': 'i'}, {'name': 'j', 'parameters': [], 'notation': 'j'}, {'name': 'k', 'parameters': [], 'notation': 'k'}, {'name': 'l', 'parameters': [], 'notation': 'l'}, {'name': 'm', 'parameters': [], 'notation': 'm'}, {'name': 'n', 'parameters': [], 'notation': 'n'}, {'name': 'o', 'parameters': [], 'notation': 'o'}, {'name': 'p', 'parameters': [], 'notation': 'p'}, {'name': 'q', 'parameters': [], 'notation': 'q'}, {'name': 'r', 'parameters': [], 'notation': 'r'}, {'name': 's', 'parameters': [], 'notation': 's'}, {'name': 't', 'parameters': [], 'notation': 't'}, {'name': 'u', 'parameters': [], 'notation': 'u'}, {'name': 'v', 'parameters': [], 'notation': 'v'}, {'name': 'w', 'parameters': [], 'notation': 'w'}, {'name': 'x', 'parameters': [], 'notation': 'x'}, {'name': 'y', 'parameters': [], 'notation': 'y'}, {'name': 'z', 'parameters': [], 'notation': 'z'}])
    #Add alpha, beta, ...
    special_variables.extend([{'name': 'Alpha', 'parameters': [], 'notation': 'Α'}, {'name': 'Beta', 'parameters': [], 'notation': 'Β'}, {'name': 'Gamma', 'parameters': [], 'notation': 'Γ'}, {'name': 'Delta', 'parameters': [], 'notation': 'Δ'}, {'name': 'Epsilon', 'parameters': [], 'notation': 'Ε'}, {'name': 'Zeta', 'parameters': [], 'notation': 'Ζ'}, {'name': 'Eta', 'parameters': [], 'notation': 'Η'}, {'name': 'Theta', 'parameters': [], 'notation': 'Θ'}, {'name': 'Iota', 'parameters': [], 'notation': 'Ι'}, {'name': 'Kappa', 'parameters': [], 'notation': 'Κ'}, {'name': 'Lambda', 'parameters': [], 'notation': 'Λ'}, {'name': 'Mu', 'parameters': [], 'notation': 'Μ'}, {'name': 'Nu', 'parameters': [], 'notation': 'Ν'}, {'name': 'Xi', 'parameters': [], 'notation': 'Ξ'}, {'name': 'Omicron', 'parameters': [], 'notation': 'Ο'}, {'name': 'Pi', 'parameters': [], 'notation': 'Π'}, {'name': 'Rho', 'parameters': [], 'notation': 'Ρ'}, {'name': 'Sigma', 'parameters': [], 'notation': 'Σ'}, {'name': 'Tau', 'parameters': [], 'notation': 'Τ'}, {'name': 'Upsilon', 'parameters': [], 'notation': 'Υ'}, {'name': 'Phi', 'parameters': [], 'notation': 'Φ'}, {'name': 'Chi', 'parameters': [], 'notation': 'Χ'}, {'name': 'Psi', 'parameters': [], 'notation': 'Ψ'}, {'name': 'Omega', 'parameters': [], 'notation': 'Ω'}])
    special_variables.extend([{'name': 'alpha', 'parameters': [], 'notation': 'α'}, {'name': 'beta', 'parameters': [], 'notation': 'β'}, {'name': 'gamma', 'parameters': [], 'notation': 'γ'}, {'name': 'delta', 'parameters': [], 'notation': 'δ'}, {'name': 'epsilon', 'parameters': [], 'notation': 'ε'}, {'name': 'zeta', 'parameters': [], 'notation': 'ζ'}, {'name': 'eta', 'parameters': [], 'notation': 'η'}, {'name': 'theta', 'parameters': [], 'notation': 'θ'}, {'name': 'iota', 'parameters': [], 'notation': 'ι'}, {'name': 'kappa', 'parameters': [], 'notation': 'κ'}, {'name': 'lambda', 'parameters': [], 'notation': 'λ'}, {'name': 'mu', 'parameters': [], 'notation': 'μ'}, {'name': 'nu', 'parameters': [], 'notation': 'ν'}, {'name': 'xi', 'parameters': [], 'notation': 'ξ'}, {'name': 'omicron', 'parameters': [], 'notation': 'ο'}, {'name': 'pi', 'parameters': [], 'notation': 'π'}, {'name': 'rho', 'parameters': [], 'notation': 'ρ'}, {'name': 'sigma', 'parameters': [], 'notation': 'σ'}, {'name': 'tau', 'parameters': [], 'notation': 'τ'}, {'name': 'upsilon', 'parameters': [], 'notation': 'υ'}, {'name': 'phi', 'parameters': [], 'notation': 'φ'}, {'name': 'chi', 'parameters': [], 'notation': 'χ'}, {'name': 'psi', 'parameters': [], 'notation': 'ψ'}, {'name': 'omega', 'parameters': [], 'notation': 'ω'}])

    grammarGenerator.generateGrammar(all_variables, special_variables, all_commands_structure, all_commands_math, all_commands_text, all_commands_symbolname)
    print("\nGENERATED EXTENDED GRAMMAR.")