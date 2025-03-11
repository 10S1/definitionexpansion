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

def initializeGfShell():
    shell = gf.GFShellRaw(PATH_exe_gf)
    print(shell.handle_command(f"import {PATH_gf_concrGrammar}"))
    return shell

def parse(input_path):
    shell = initializeGfShell()
    #print(
    parseHtmltoTrees(shell, input_path)[0]

parse("sHTML/Examples/Statements/E001_reduced.en.xhtml")