# Flexiformal Definiton Expansion

This repository contains implementations of flexiformal definition expansion (= replacing a term in a text through its definition).
It contains a sTeX-to-sTeX version and a SHTML-to-SHTML version.



## Usage of sTeX version

The sTeX version works on SMGloM modules. Their content needs to be preprocessed.

1. Download the necessary tools: 

   + The Grammatical Framework executable & grammars: https://www.grammaticalframework.org/download/index-3.11.html
    
   * The Preprocessor executable: https://gitos.rrze.fau.de/voll-ki/fau/system/relocalization/
    
   * The SMGloM folder: https://gl.mathhub.info/smglom


2. In `sTeX\definitionExpander.py`:

   + Change the paths to the paths of your installations.
   
   * Change `symname_uri` to the URI of the definition and `statement_id_uri` to the URI of the statement (= the text, in which you want to replace the definition). The URIs refer to paragraphs in SMGloM modules.
  

## Usage of SHTML version

1. Download the necessary tools: 

   + The Grammatical Framework executable & grammars: https://www.grammaticalframework.org/download/index-3.11.html

2. In `SHTML\definitionExpander.py`:

   + Change the paths to the paths of your installations.
