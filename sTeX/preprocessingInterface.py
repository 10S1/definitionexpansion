import shutil
import os
import subprocess
import re

PATH_exe_preprocessor = shutil.which('relocate')
if PATH_exe_preprocessor is None:
    print("ERROR: Path to relocate.exe not found. \nCheck whether the Preprocessor is installed and the environment variable is set.")

PATH_dict_mathhub = os.getenv('MATHHUB').strip('"')
if (PATH_dict_mathhub is None) or (not os.path.isdir(PATH_dict_mathhub)):
    print("ERROR: Path to MathHub not found. \nCheck whether the SMGloM is installed and the environment variable is set.")

PATH_folder_smglom = PATH_dict_mathhub + "\smglom"



###----- Formatting -----------------------------------------------------------------------------------------------------------------------------------------------------------------------###
def lowercase_first_letter(s: str) -> str:
    if s and s[0].isupper():
        return s[0].lower() + s[1:]
    return s
def uppercase_first_letter(s: str) -> str:
    if s and s[0].islower():
        return s[0].upper() + s[1:]
    return s

def makeNameGfConform(name: str) -> str:
    """Replaces symbols, which are not allowed to appear in the names of the GF rules."""
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

def make_sentence_GfConform(sentence: str) -> str:
    """Brings a normal sentence into a format, which is parsable by the generated grammar, which is used in the Grammatical Framework."""
    sentence_pp = preprocessString(sentence)
    sentence_pp = lowercase_first_letter(sentence_pp).replace("\\", "\\\\")
    sentence_pp = sentence_pp.strip()
    if sentence_pp.endswith(" ."):
        sentence_pp = sentence_pp[:-2]
    sentence_pp = sentence_pp.strip()
    sentence_pp = lowercase_first_letter(sentence_pp)
    return sentence_pp
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Using the Preprocessor -----------------------------------------------------------------------------------------------------------------------------------------------------------###
#Path to the afmcList (Used by the Preprocessor)
def clear_AfmcList():
    PATH_json_amfcList = r"sTeX\afmcList.json"
    with open(PATH_json_amfcList, 'w') as file:
        file.write("[]")

def preprocessString(input_string: str) -> str:
    """Uses the Preprocessor to add spaces to a normal sTeX sentence, so it can be parsed by the Grammatical Framework."""
    executable_path = PATH_exe_preprocessor
    command = [executable_path, '--mode=gf', f'--input={input_string}']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def getInformation_defExp(symname_uri: str, statement_id_uri: str) -> str:
    """Uses the Preprocessor to fetch the used variables and commands, which could be used in the SMGloM files, which the URIs refer to."""
    executable_path = PATH_exe_preprocessor
    command = [executable_path, '--mode=def-exp', f'--mathhub={PATH_dict_mathhub}', f'--symname={symname_uri}', f'--statement={statement_id_uri}']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True, encoding='utf-8', errors='replace')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None
    
def getInformation_defExpEval(file_uri: str) -> str:
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
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###



###----- Postprocessing -------------------------------------------------------------------------------------------------------------------------------------------------------------------###
def format_math_expressions(text: str) -> str:
    """Adds spaces for postprocessing the result sentence."""
    return re.sub(r'\$(.*?)\$', lambda m: "$" + m.group(1).replace(" ", "") + "$", text)

def adjust_dollar_sign_spacing(sentence: str) -> str:
    """Adds spaces around dollar signs for postprocessing the result sentence."""
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

def postprocessSentence(sentence: str) -> str:
    """Brings a sentence, which is in a format, which is parsable by the Grammatical Framework, back to a normal format."""
    sentence = (uppercase_first_letter(sentence).replace("\\\\", "\\")) + "."
    sentence = sentence.replace("{ ", "{")
    sentence = sentence.replace(" {", "{")
    sentence = sentence.replace(" }", "}")
    sentence = format_math_expressions(sentence)
    return sentence

def postprocessSentence_onlyremoveSpaces(sentence: str) -> str:
    """
    Brings a sentence, which is in a format, which is parsable by the Grammatical Framework, back to a normal format.
    Special case of postprocessSentence(sentence). 
    Necessary for finding the sentences, which need to be replaced while generating the sTeX file.
    """
    sentence = sentence.replace("{ ", "{")
    sentence = sentence.replace(" {", "{")
    sentence = sentence.replace(" }", "}")
    sentence = format_math_expressions(sentence)
    sentence = sentence.replace("  ", " ")
    sentence = sentence.replace(" .", ".")
    sentence = sentence.strip()
    return sentence
###----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###