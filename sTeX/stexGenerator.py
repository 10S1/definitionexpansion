import re
import os
from typing import List, Dict

import preprocessingInterface

PATH_dict_mathhub = os.getenv('MATHHUB').strip('"')
if (PATH_dict_mathhub is None) or (not os.path.isdir(PATH_dict_mathhub)):
    print("ERROR: Path to MathHub not found. \nCheck whether the SMGloM is installed and the environment variable is set.")

def read_file_with_fallback(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            return f.read()

def extract_latex_commands(latex_str: str) -> List[str]:
    """Extracts the importmodule, usemodel and symdecl lines out of a sTeX file."""
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

def generate_stexFile(input_stex_definition: str, input_stex_statement: str, replacedSentences: Dict[str, str], newVariables: List[str]) -> str:
    """
    Generates a sTeX file, which is the statement sTeX file, in which the original sentences are replaced by the merged sentences 
    and additonal lines are added for newly introduced variables and the relevant lines from the definition sTeX file are added.
    """
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

def get_stexfile(uri: str) -> str:
    """Fetches the content of the SMGloM file, in which the URI appears."""
    if "defexp/def?" in uri:
        temp_file_path = uri.split("?")[1] 
        file_path = PATH_dict_mathhub + "\smglom\defexp\source\def\\" + temp_file_path + ".en.tex"
    elif "defexp/stm" in uri:
        temp_file_path = uri.split("?")[1] 
        temp_file_path = temp_file_path.replace("-", "_")
        temp_file_path = temp_file_path.replace(".", "-")
        file_path = PATH_dict_mathhub + "\smglom\defexp\source\stm\\" + temp_file_path + ".en.tex"
    else:
        temp_file_path = uri.split("?")[0] 
        file_path = file_path.replace("/", "\\")
        file_path = uri.replace("/mod", "/source/mod")
        file_path = file_path.replace("http://mathhub.info/smglom", PATH_dict_mathhub + "/smglom")
        file_path = file_path + ".en.tex"

    file_path = file_path.replace(".en.en", ".en")
    file_path = file_path.replace("-en.en", ".en")
    file_path = file_path.replace("/", "\\")

    file_content = read_file_with_fallback(file_path)
    return file_content

def main(newVars, og_statement, result_sentence_postprocessed, symname_uri, statement_id_uri):
    newVariables = [item['name'] for item in newVars]
    replacedSentences = {preprocessingInterface.postprocessSentence_onlyremoveSpaces(og_statement): result_sentence_postprocessed}
    input_stex_definition = get_stexfile(symname_uri)
    input_stexStatement = get_stexfile(statement_id_uri)
    result_stex_output = generate_stexFile(input_stex_definition, input_stexStatement, replacedSentences, newVariables)
    name_outputStex = "GEN_mergedOutput.en.tex"
    with open("sTeX\\" + name_outputStex, 'w') as gf_file:
        gf_file.write(result_stex_output)