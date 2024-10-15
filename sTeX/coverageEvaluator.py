###----- Imports --------------------------------------------------------------------------------------------------------------------------------------------------------------------------###
import regex as re
import os
import sys
import threading
from typing import List, Any, Tuple, Dict
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Resources')))
import gf
import grammarExtender
import preprocessingInterface

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

preprocessingInterface.clear_AfmcList()
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Parameters -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
active_detailedOutput = False
PAR_timeout = 60   #seconds
PAR_grammarname = "GEN_Grammar"   #How the generated grammar file will be named
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
def preprocessSentence(sentence: str) -> str: 
    sentence = sentence.strip()
    sentence = (preprocessingInterface.lowercase_first_letter(sentence).replace("\\", "\\\\"))[:-2]
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
def splitTextIntoSentences(text: str) -> List[str]:
    #SpaCy
    language = detect(text)
    if language == "de":
        text_processed = nlp_de(text)
    else:
        text_processed = nlp_en(text)
    sentences = [sent.text for sent in text_processed.sents]
    return sentences

def make_sentence_GfConform(sentence: str) -> str:
    sentence_pp = sentence.strip()
    sentence_pp = remove_text_in_parentheses(sentence_pp)
    sentence_pp = re.sub(r'(?<!\\)[\n\r]', '', sentence_pp)
    sentence_pp = sentence_pp.replace("Definame", "definame")
    sentence_pp = sentence_pp.replace("\\r\\n", "")
    sentence_pp = sentence_pp.replace("\r\n", "")
    sentence_pp = sentence_pp.strip()
    sentence_pp = preprocessingInterface.preprocessString(sentence_pp)
    if sentence_pp is not None:
        sentence_pp = preprocessingInterface.lowercase_first_letter(sentence_pp).replace("\\", "\\\\")
        sentence_pp = sentence_pp.strip()
        if sentence_pp.endswith(" ."):
            sentence_pp = sentence_pp[:-2]
        if sentence_pp.endswith("."):
            sentence_pp = sentence_pp[:-1]
        sentence_pp = sentence_pp.strip()
    return sentence_pp

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
grammarExtender.generate_grammar(folders)
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