###----- Imports --------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
import regex as re
import json
import os
import sys
import subprocess
import threading
from typing import List, Any, Tuple, Dict
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Resources')))
import gf
import grammarGenerator

from langdetect import detect   #pip install langdetect
import spacy   # pip install spacy
nlp_en = spacy.load("en_core_web_sm")   # python -m spacy download en_core_web_sm  # For English
nlp_de = spacy.load("de_core_news_sm")   # python -m spacy download de_core_news_sm # For German
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

PATH_folder_smglom = PATH_dict_mathhub + "\smglom"

#Path to the afmcList (Used by the Preprocessor)
PATH_json_amfcList = r"sTeX\afmcList.json"
with open(PATH_json_amfcList, 'w') as file:
    file.write("[]")
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Parameters -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
active_detailedOutput = False
PAR_timeout = 60   #seconds
PAR_grammarname = "GEN_Grammar"   #How the generated grammar file will be named
PAR_inputformat = "stex"   #Either "stex" (for going through the SMGloM tex folders) or "plain" (for going through a list of plaintext sentences)
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Variables ------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
dictionary_fileSentences = {}
folder_details = ""
name_outputfile = "GEN_OUT_coverageEvaluator"
if active_detailedOutput:
    details = ""
    temp_add_details = ""
shell = None

#Paths where the generated grammars will be placed.
PATH_gf_concrGrammar = 'sTeX\Grammar\GEN_grammar_concr.gf'
PATH_gf_abstrGrammar = 'sTeX\Grammar\GEN_grammar_abstr.gf'
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Irrelevant Functions -------------------------------------------------------------------------------------------------------------------------------------------------------------###
def debug_print(text: str, value: Any):
    print("\n" + str(text) + ": " + str(value))

def lowercase_first_letter(s: str) -> str:
    if s and s[0].isupper():
        return s[0].lower() + s[1:]
    return s

def flatten_list_of_lists(nested_lists: List[List[Any]]) -> List[Any]:
    return [item for sublist in nested_lists for item in sublist]

def preprocessSentence(sentence: str) -> str: 
    sentence = sentence.strip()
    sentence = (lowercase_first_letter(sentence).replace("\\", "\\\\"))[:-2]
    return sentence

def remove_text_in_parentheses(text: str) -> str:
    result = []
    skip = 0
    for char in text:
        if char == '(':
            skip += 1
        elif char == ')' and skip > 0:
            skip -= 1
        elif skip == 0:
            result.append(char)
    return ''.join(result)

class TimeoutError(Exception):
    pass

def create_output(all_parsed_sentences, all_not_parsed_sentences, all_timeout_sentences, all_parsed_files, all_not_parsed_files, all_timeout_files):
    total_sentences = str(len(all_parsed_sentences) + len(all_not_parsed_sentences) + len(all_timeout_sentences))
    total_files = str(len(all_parsed_files) + len(all_not_parsed_files) + len(all_timeout_files))
    output = "\n\nAmount of total sentences: " + str(total_sentences) + "\n   Amount of parsed sentences: " + str(len(all_parsed_sentences)) + "\n   Amount of not parsed sentences: " + str(len(all_not_parsed_sentences)) + "\n   Amount of timeout sentences: " + str(len(all_timeout_sentences))
    output = str(output) + "\n\nAmount of total files: " + str(total_files) + "\n   Amount of parsed files: " + str(len(all_parsed_files)) + "\n   Amount of not parsed files: " + str(len(all_not_parsed_files)) + "\n   Amount of timeout files: " + str(len(all_timeout_files))
    output = str(output) + "\n\n" + str(folder_details)
    output = str(output) + "\n\nParsed sentences: " + str(all_parsed_sentences) + "\n\nNot parsed sentences: " + str(all_not_parsed_sentences) + "\n\nTimeout sentences: " + str(all_timeout_sentences)
    if active_detailedOutput:
        output = str(output) + "\n\n--------------------------------------------------------------------------\n\n" + str(details)
    with open("sTeX\\" + name_outputfile + ".txt", 'w') as file:
        file.write(output)

def read_file_with_fallback(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            return f.read()

def get_mod_files_paths(base_dir: str) -> List[Dict]:
    all_files_paths = []
    
    # Go through all folders in the smglom directory
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        
        if os.path.isdir(folder_path):
            # Look for the "source" folder inside the current folder
            source_path = os.path.join(folder_path, 'source')
            if os.path.isdir(source_path):
                # Look for the "mod" folder inside the "source" folder
                mod_path = os.path.join(source_path, 'mod')
                if os.path.isdir(mod_path):
                    # Collect all files in the "mod" folder
                    mod_files = []
                    for file in os.listdir(mod_path):
                        if file.endswith('.en.tex'):   #TODO: Remove if you want to consider all languages
                            file_path = os.path.join(mod_path, file)
                            if os.path.isfile(file_path):
                                mod_files.append(file_path)
                    
                    # Add the folder name and its corresponding mod file contents as an entry in the array
                    all_files_paths.append({
                        "foldername": folder,
                        "filepaths": mod_files
                    })
    return all_files_paths
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Functions ------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
def PREPROCESSOR_preprocessString(input_string: str) -> str:
    executable_path = PATH_exe_preprocessor
    command = [executable_path, '--mode=gf', f'--input={input_string}']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def PREPROCESSOR_getInformation(file_uri: str) -> str:
    executable_path = PATH_exe_preprocessor
    command = [executable_path, '--mode=def-exp-eval', f'--mathhub={PATH_dict_mathhub}', f'--file={file_uri}', f'--amfc={PATH_json_amfcList}']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        ret = result.stdout
        if ret != None:
            ret = ret.strip()
        return ret
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def splitTextIntoSentences(text: str) -> List[str]:
    #SpaCy
    language = detect(text)
    if language == "de":
        text_processed = nlp_de(text)
    else:
        text_processed = nlp_en(text)
    sentences = [sent.text for sent in text_processed.sents]
    return sentences

    # Alternatives:
    #     #NLTK
    #     import nltk
    #     nltk.download('punkt')
    #     from nltk.tokenize import sent_tokenize
    #     sentences = sent_tokenize(text)
    #     return sentences

    #     #Stanza
    #     import stanza
    #     stanza.download('en')
    #     nlp_en = stanza.Pipeline('en')
    #     doc = nlp_en(text)
    #     sentences = [sentence.text for sentence in doc.sentences]
    #     return sentences

    #     #Hugging Face Transformers
    #     from transformers import AutoTokenizer, AutoModelForTokenClassification
    #     import torch
    #     from transformers import pipeline
    #     # Load a pre-trained model and tokenizer from Hugging Face
    #     tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    #     model = AutoModelForTokenClassification.from_pretrained("bert-base-cased")
    #     # Use the pipeline for sentence segmentation
    #     nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    #     sentences = tokenizer.tokenize(text)
    #     return sentences

def make_sentence_GfConform(sentence: str) -> str:
    sentence_pp = sentence.strip()
    sentence_pp = remove_text_in_parentheses(sentence_pp)
    sentence_pp = re.sub(r'(?<!\\)[\n\r]', '', sentence_pp)
    sentence_pp = sentence_pp.replace("Definame", "definame")
    sentence_pp = sentence_pp.replace("\\r\\n", "")
    sentence_pp = sentence_pp.replace("\r\n", "")
    sentence_pp = sentence_pp.strip()
    sentence_pp = PREPROCESSOR_preprocessString(sentence_pp)
    if sentence_pp is not None:
        sentence_pp = lowercase_first_letter(sentence_pp).replace("\\", "\\\\")
        sentence_pp = sentence_pp.strip()
        if sentence_pp.endswith(" ."):
            sentence_pp = sentence_pp[:-2]
        if sentence_pp.endswith("."):
            sentence_pp = sentence_pp[:-1]
        sentence_pp = sentence_pp.strip()
    return sentence_pp

def generate_grammar(folders: List[Any]):
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
            text_information_str = PREPROCESSOR_getInformation(file_uri)
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
    print("\nGENERATED.")

def try_parsing(sentence: str) -> str:
    cmd = 'parse "' + sentence + '"'
    tree = shell.handle_command(cmd)
    #Multiple statement trees 
    #trees_all = shell.handle_command(cmd)
    #trees = trees_all.split('\n')
    if active_detailedOutput:
        global temp_add_details
        temp_add_details = "\n\ncmd: " + str(cmd) + "\nTree: " + str(tree)
    return tree

def sentence_is_parsable(sentence: str) -> str:
    global shell
    # Preprocess sentence
    sentence_pp = make_sentence_GfConform(sentence)
    if sentence_pp is None:
        return "FALSE"

    # Define a thread to handle the parsing
    result = [None]
    timeout = PAR_timeout  # seconds

    def worker():
        result[0] = try_parsing(sentence_pp)

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join(timeout)  # Wait for the specified timeout period

    if thread.is_alive():
        thread.join(0)  # Terminate the thread if it’s still alive
        shell.gf_shell.kill()
        print("Timeout occurred")
        shell = gf.GFShellRaw(PATH_exe_gf)
        shell.handle_command(f"import {PATH_gf_concrGrammar}")
        return "TIMEOUT"
    #print("\n" + str(result))
    sentence_tree = result[0]

    if ("parser failed" in sentence_tree) or (sentence_tree == ""): 
        if active_detailedOutput:
            global temp_add_details
            global details
            details = str(details) + str(temp_add_details)
        return "FALSE" 
    return "TRUE"
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Main -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
#Input
base_dir = PATH_folder_smglom
folders = get_mod_files_paths(base_dir)

#Generate grammar and initialize GF
generate_grammar(folders)
shell = gf.GFShellRaw(PATH_exe_gf)
shell.handle_command(f"import {PATH_gf_concrGrammar}")

#For each folder: Get the amount of parsed sentences and the amount of parsed files
all_parsed_files = []
all_not_parsed_files = []
all_timeout_files = []
all_parsed_sentences = []
all_not_parsed_sentences = []
all_timeout_sentences = []

for folder in folders:
    parsed_files = []
    not_parsed_files = []
    timeout_files = []
    parsed_sentences = []
    not_parsed_sentences = []
    timeout_sentences = []

    for file in folder["filepaths"]:
        file_parseable = True
        if file not in dictionary_fileSentences:
            not_parsed_files.append(file)
        else:
            texts = dictionary_fileSentences[file]
            sentences = []
            for text in texts:
                sentences.extend(splitTextIntoSentences(text))

            for sentence in sentences:
                if (sentence != "") and (sentence != " ") and (sentence != "%") and (not "TODO" in sentence):   #Removes incomplete sentences
                    parsable = sentence_is_parsable(sentence)
                    if parsable == "TRUE":
                        parsed_sentences.append(sentence)
                    elif parsable == "TIMEOUT":
                        timeout_sentences.append(sentence)
                        if file_parseable:
                            file_parseable = "TIMEOUT"
                    else:
                        not_parsed_sentences.append(sentence)
                        file_parseable = False

            if file_parseable:
                parsed_files.append(file)
            elif file_parseable == "TIMEOUT":
                timeout_files.append(file)
            else:
                not_parsed_files.append(file)

    folder_details = str(folder_details) + "\n\nFoldername: " + str(folder["foldername"]) + "\n     Parsed sentences: " + str(len(parsed_sentences)) + "   Not parsed sentences: " + str(len(not_parsed_sentences)) + "   Timeout sentences: " + str(len(timeout_sentences)) + "\n     Parsed files: " + str(len(parsed_files)) + "   Not parsed files: " + str(len(not_parsed_files)) + "   Timeout files: " + str(len(timeout_files))
    print("DONE: " + str(folder["foldername"]))
    
    all_parsed_files.extend(parsed_files)
    all_not_parsed_files.extend(not_parsed_files)
    all_timeout_files.extend(timeout_files)
    all_parsed_sentences.extend(parsed_sentences)
    all_not_parsed_sentences.extend(not_parsed_sentences)
    all_timeout_sentences.extend(timeout_sentences)
    create_output(all_parsed_sentences, all_not_parsed_sentences, all_timeout_sentences, all_parsed_files, all_not_parsed_files, all_timeout_files)

shell.gf_shell.kill()
print("\nDONE.")
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###