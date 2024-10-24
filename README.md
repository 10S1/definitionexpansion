# Flexiformal Definiton Expansion

This repository contains implementations [definitionExpander.py] of flexiformal definition expansion (= replacing a term in a text through its definition).
It contains a sTeX-to-sTeX version and a SHTML-to-SHTML version.

## sTeX version
### A. Setup

The sTeX version works on SMGloM modules. Their content needs to be preprocessed by the Preprocessor to enable parsing through the Grammatical Framework.

   1. Grammatical Framework: 
      * Go to https://www.grammaticalframework.org/download/index-3.11.html and install the Grammatical Framework. 
      * Add the PATH environment variable `GF_LIB_PATH`, which should refer to the installed Grammatical Framework folder.
      * Add the path of `gf.exe` in the `gf_3.11`-folder in the installed Grammatical Framework folder to the `PATH`.
    
   2. Preprocessor: 
      * Go to https://gitos.rrze.fau.de/voll-ki/fau/system/relocalization/ and build `relocate`.
      * Add the path of the executable `relocate` to the `PATH`.

   3. SMGloM:
      * Create a new folder `MathHub`.
      * Add the environment variable `MATHHUB`, which should refer to the `MathHub` folder.
      * Clone the repositories from https://gl.mathhub.info/smglom. 
         * For example: Install https://github.com/jfschaefer/stextools and execute `python -m pip install .`. (Maybe additonally necessary: `python -m pip install pylatexenc python-gitlab --user`)

   4. For definition expansion: 
      * Copy the folder `sTeX\SMGloM\defexp` into the `smglom` folder in the `MathHub` folder, which you created in step `3.`.
   
   5. For coverage evaluation: If not installed yet:
      * `python -m pip install spacy`
      * `python -m spacy download en_core_web_sm`
      * `python -m spacy download de_core_news_sm`
      * `python -m pip install langdetect`


### B. Usage
* Definition Expansion: To apply definition expansion, use the function `def main(symname_uri: str, statement_id_uri: str, definiendum: str, stexOutput: bool) -> str`.
   * Inputs:
      * `symname_uri`: URI refering to a paragraph in a SMGloM module, which defines the definiendum.
      * `statement_id_uri`: URI refering to a paragraph in a SMGloM module, in which the definiendum appears.
      * `definiendum`: A mathematical term.
      * `stexOutput`: Determines whether a merged sTeX file should be generated. 
   * Output: The merged sentence. (The paragraph refered by `statement_id_uri`, in which the `definiendum` is replaced by its definition according to `symname_uri`.)
   * Example: 
      * `import definitionExpander`
      * `definitionExpander.main("http://mathhub.info/smglom/defexp/def?consistent?consistent", "http://mathhub.info/smglom/defexp/stm/stm_2-5.en?stm-2.5", "consistent", True)`
      * Further example tuples can be found in `sTeX\FDE_examples.json`.

* Parsing Coverage Evaluation: To evaluate the coverage of the grammar while parsing the sentences, which appear in SMGloM modules, run `sTeX\coverageEvaluator.py`.


## SHTML version
### A. Setup
   1. Grammatical Framework: 
      * Go to https://www.grammaticalframework.org/download/index-3.11.html and install the Grammatical Framework. 
      * Add the PATH environment variable `GF_LIB_PATH`, which should refer to the installed Grammatical Framework folder.
      * Add the path of `gf.exe` in the `gf_3.11`-folder in the installed Grammatical Framework folder to the `PATH`.
   
2. ...

### B. Usage
...
