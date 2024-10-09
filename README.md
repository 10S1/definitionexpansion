# Flexiformal Definiton Expansion

This repository contains implementations of flexiformal definition expansion (= replacing a term in a text through its definition).
It contains a sTeX-to-sTeX version and a SHTML-to-SHTML version.



## Usage of sTeX version

The sTeX version works on SMGloM modules. Their content needs to be preprocessed.

1. Download the necessary tools: 

   1.1. Grammatical Framework: 
      * Go to https://www.grammaticalframework.org/download/index-3.11.html and install the Grammatical Framework. 
      * Add the PATH environment variable `GF_LIB_PATH`, which should refer to the installed Grammatical Framework folder.
      * Add the PATH enviroment variable `GF_EXE`, which should refer to the `gf.exe` in the `gf_3.11`-folder in the installed Grammatical Framework folder.
    
   1.2. Preprocessor: 
      * Go to https://gitos.rrze.fau.de/voll-ki/fau/system/relocalization/ and either download or build `relocate.exe`.
      * Add the PATH environment variable `PP_EXE`, which should refer to `relocate.exe`.

   1.3. sTeX:
      * Follow the instructions at https://github.com/slatex/sTeX?tab=readme-ov-file.

   1.4. SMGloM:
      * Create a new folder `MathHub`.
      * Add the PATH environment variable `MATHHUB`, which should refer to the `MathHub` folder.
      * Clone the repositories from https://gl.mathhub.info/smglom. 
         * For example: Install https://github.com/jfschaefer/stextools and execute `python -m pip install .`. (Maybe additonally necessary: `python -m pip install pylatexenc python-gitlab --user`)


2. For definition expansion: In `sTeX\definitionExpander.py` change `symname_uri` to the URI of the definition and `statement_id_uri` to the URI of the statement (= the text, in which you want to replace the definition). The URIs refer to paragraphs in SMGloM modules.



## Usage of SHTML version

1. Download the necessary tools: 

   + The Grammatical Framework executable & grammars: https://www.grammaticalframework.org/download/index-3.11.html

   * ...

2. For definition expansion:

   + ...
