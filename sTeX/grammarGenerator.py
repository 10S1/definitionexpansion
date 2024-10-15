import regex as re
import json
import preprocessingInterface

def escapeCmds(text: str) -> str:
    text = text.replace("\\omega", "\\\\omega")
    text = text.replace("\\natminus", "\\\\natminus")
    text = text.replace("\\infty", "\\\\infty")
    text = text.replace("\\ell", "\\\\ell")
    text = text.replace("\\pnormOp", "\\\\pnormOp")
    text = text.replace("\\pair", "\\\\pair")
    text = text.replace("\\sigma", "\\\\sigma")
    text = text.replace("\u00e4", "\\\\u00e4")  # 'ä'
    text = text.replace("\u00fc", "\\\\u00fc")  # 'ü'
    text = text.replace("\u00f6", "\\\\u00f6")  # 'ö'
    text = text.replace("\u2013", "\\\\u2013")   # '–' (en dash)
    text = text.replace("\\&", "and")
    text = text.replace("\\ALeAname", "\\\\ALeAname")
    text = text.replace("\\LaTeX", "\\\\LaTeX")
    text = text.replace("\\MMTformat", "\\\\MMTformat")
    text = text.replace("\\TeX", "\\\\TeX")
    text = text.replace("\\MMTsystem", "\\\\MMTsystem")
    text = text.replace("\\python", "\\\\python")
    text = text.replace("\\underline", "\\\\underline")
    text = text.replace("\\ndim", "\\\\ndim")
    text = text.replace("\\RealNumbers", "\\\\RealNumbers")
    text = text.replace("\\phi", "\\\\phi")
    text = text.replace("\\sn{table", "\\\\sn{table")
    text = re.sub(r'(?<!\\)(\\)([a-zA-Z])', r'\\\1\2', text)

    #text = re.sub(r'(\\)([a-zA-Z])', r'\\\1\2', text)
    #text = text.replace("\\", "\\\\")
    return text

def get_usedDefiniendums() -> list[str]:
    with open('Resources\definiendums.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract words out of the "en"-lists
    words = []
    for value in data.values():
        if "en" in value:
            words.extend(value["en"])

    # Remove duplicates and sort list
    words_unique = sorted(set(words))

    return words_unique

def generateGrammar(variables, special_variables, commands_structure, commands_math, commands_text, commands_symbolname):
    with open("sTeX\Grammar\BaseGrammar_abstr.gf", 'r', encoding='utf-8') as file:
        abstrSyntaxBase = file.read()
    with open("sTeX\Grammar\BaseGrammar_concr.gf", 'r', encoding='utf-8') as file:
        concrSyntaxBase = file.read()

    #DEFINIENDUMS
    abs_defis = ""
    con_defis = ""
    usedDefiniendums = get_usedDefiniendums()
    for defi in usedDefiniendums:
        new_abs_defis = ""
        new_con_defis = ""
        ruleName = "S_definiendum_WW" + preprocessingInterface.makeNameGfConform(defi) + "_S"
        defi2 = defi.replace("-", " - ")
        if (str(ruleName) + " :") in abstrSyntaxBase:
            ruleName = str(ruleName) + "2"

        new_abs_defis = new_abs_defis + "\n" + "        " + "S_definiendum_WW" + ruleName + " : S -> S;"   
        new_con_defis = new_con_defis + "\n" + "        " + "S_definiendum_WW" + ruleName + " sen = { s = \"\\\\definiens [\" ++ \"" + defi2 + "\" ++ \"] {\" ++ sen.s ++ \"}\" };"
        
        if (new_abs_defis not in abs_defis) and (new_con_defis not in con_defis):
            abs_defis = abs_defis + new_abs_defis
            con_defis = con_defis + new_con_defis


    #VARIABLES  
    abs_var = ""      
    con_var = "" 
    for variable in variables:
        new_abs_var = "" 
        new_con_var = ""
        temp_Var = (variable["name"]).replace("\\", "")
        var = preprocessingInterface.makeNameGfConform(temp_Var)
        varName = variable["name"].replace("\n", "")
        if variable["parameters"] == []:
            #Abstract rules  
            new_abs_var = new_abs_var + "\n" + "        " + "G_variable_VAR" + var + " : C_variable;"
            #Concrete rules          
            new_con_var = new_con_var + "\n" + "        " + "G_variable_VAR" + var + " = \"\\" + varName + "\";"
        elif variable["parameters"] == ["RETURN"]:
            #Abstract rules    
            new_abs_var = new_abs_var + "\n" + "        " + "G_variable_VAR_ret" + var + "_exclamation : C_variable;"     
            new_abs_var = new_abs_var + "\n" + "        " + "G_variable_VAR_ret" + var + "_brackets : C_variable;"   
            #Concrete rules     
            new_con_var = new_con_var + "\n" + "        " + "G_variable_VAR_ret" + var +  "_exclamation = \"\\" + varName + " !\";"
            new_con_var = new_con_var + "\n" + "        " + "G_variable_VAR_ret" + var +  "_brackets = \"\\" + varName + "\"++ \"{ }\";"
        else:
            #Concrete rules     
            new_con_var = new_con_var + "\n" + "        " + "G_Variable_VAR" + var +  "_exclamation = \"\\" + varName + " !\";"
            arguments = ""
            text = ""
            counter_i = 1
            counter_a = 1
            for par in variable["parameters"]:
                if par == "i" or par == "b": 
                    arguments = arguments + " i" + str(counter_i)
                    text = text + " ++ i" + str(counter_i)
                    counter_i += 1
                elif par == "a" or par == "B": 
                    arguments = arguments + " a" + str(counter_a)
                    text = text + " ++ a" + str(counter_a)
                    counter_a += 1
            new_con_var = new_con_var + "\n" + "        " + "G_Variable_VAR_" + var + "_" + arguments[1:].replace(" ", "_") + arguments + " = \"\\" + varName + "\"" + text + ";"

            #Abstract rules    
            new_abs_var = new_abs_var + "\n" + "        " + "G_variable_VAR" + var + "_exclamation : C_variable;"     
            new_abs_var = new_abs_var + "\n" + "        " + "G_variable_VAR" + var + "_" + arguments[1:].replace(" ", "_") + " : "
            for par in variable["parameters"]:
                if par == "i" or par == "b": 
                    new_abs_var = new_abs_var + "C_variable -> "
                elif par == "a" or par == "B": 
                    new_abs_var = new_abs_var + "C_variable -> "
            new_abs_var = new_abs_var + "C_texCommand;"
            
        if (new_abs_var not in abs_var) and (new_con_var not in con_var):
            abs_var = abs_var + new_abs_var
            con_var = con_var + new_con_var
    
    #Special Variables
    for variable in special_variables:
        new_abs_var = "" 
        new_con_var = ""
        temp_Var = (variable["name"]).replace("\\", "")
        var = preprocessingInterface.makeNameGfConform(temp_Var)
        varName = variable["name"].replace("\n", "")
        if variable["parameters"] == []:
            new_abs_var = new_abs_var + "\n" + "        " + "G_undeclearedVariable_VAR" + var + " : C_variable;"      
            new_con_var = new_con_var + "\n" + "        " + "G_undeclearedVariable_VAR" + var + " = \"" + varName + "\";"

        if (new_abs_var not in abs_var) and (new_con_var not in con_var):
            abs_var = abs_var + new_abs_var
            con_var = con_var + new_con_var


    #COMMANDS
    abs_cmnd = ""    
    con_cmnd = ""

    #Structure commands
    for command in commands_structure:
        new_abs_cmnd = "" 
        new_con_cmnd = ""
        cmnd = command["command"]
        if (preprocessingInterface.makeNameGfConform(cmnd) == "leftOtherSymbolSpaceSpacedistributivityPointcond") or (preprocessingInterface.makeNameGfConform(cmnd) == "rightOtherSymbolSpaceSpacedistributivityPointcond") or (preprocessingInterface.makeNameGfConform(cmnd) == "noSpaceconfusionSpacebetweenOtherSymbolSpaceSpaceSpaceSpaceconstructors"):
            continue
        temp_name = "G_texCommand_TEX" + preprocessingInterface.makeNameGfConform(cmnd)
        #Abstract rules    
        new_abs_cmnd = new_abs_cmnd + "\n" + "        " + temp_name + "_brackets : " + "C_texCommand;"
        new_abs_cmnd = new_abs_cmnd + "\n" + "        " + temp_name + "_brackets_stringList : " + "C_strList -> C_texCommand;"
        new_abs_cmnd = new_abs_cmnd + "\n" + "        " + temp_name + "_exclamation : " + "C_texCommand;"
        #Concrete rules
        new_con_cmnd = new_con_cmnd + "\n" + "        " + temp_name + "_brackets = \"\\" + cmnd + "\" ++ \"{ } { }\";"
        new_con_cmnd = new_con_cmnd + "\n" + "        " + temp_name + "_brackets_stringList fields = \"\\" + cmnd + "\" ++ \"{ } { } [\" ++ fields ++ \"]\";"
        new_con_cmnd = new_con_cmnd + "\n" + "        " + temp_name + "_exclamation = \"\\" + cmnd + "\" ++ \"!\";"
        if (new_abs_cmnd not in abs_cmnd) and (new_con_cmnd not in con_cmnd):
            abs_cmnd = abs_cmnd + new_abs_cmnd
            con_cmnd = con_cmnd + new_con_cmnd

    #Math commands
    for command in commands_math:
        new_abs_cmnd = "" 
        new_con_cmnd = ""
        cmnd = command["command"]
        #Abstract rules         
        new_abs_cmnd = new_abs_cmnd + "\n" + "        " + "G_texCommand_TEX" + preprocessingInterface.makeNameGfConform(cmnd) + "_" + ''.join(command["parameters"]) + " : "
        for par in command["parameters"]:
            if par == "i" or par == "b": 
                new_abs_cmnd = new_abs_cmnd + "C_texArgument -> "
            elif par == "a" or par == "B": 
                new_abs_cmnd = new_abs_cmnd + "C_texArguments -> "
        new_abs_cmnd = new_abs_cmnd + "C_texCommand;"
        #Concrete rules     
        arguments = ""
        text = ""
        counter_i = 1
        counter_a = 1
        for par in command["parameters"]:
            if par == "i" or par == "b": 
                arguments = arguments + " i" + str(counter_i)
                text = text + " ++ i" + str(counter_i)
                counter_i += 1
            elif par == "a" or par == "B": 
                arguments = arguments + " a" + str(counter_a)
                text = text + " ++ a" + str(counter_a)
                counter_a += 1
        new_con_cmnd = new_con_cmnd + "\n" + "        " + "G_texCommand_TEX" + preprocessingInterface.makeNameGfConform(cmnd) + "_" + ''.join(command["parameters"]) + arguments + " = \"\\" + cmnd + "\"" + text + ";"
        if (new_abs_cmnd not in abs_cmnd) and (new_con_cmnd not in con_cmnd):
            abs_cmnd = abs_cmnd + new_abs_cmnd
            con_cmnd = con_cmnd + new_con_cmnd

    #Text commands
    for command in commands_text:
        new_abs_cmnd = "" 
        new_con_cmnd = ""
        if "parameters" in command["command"]:
            cmnd = command["command"]
            #Abstract rules       
            new_abs_cmnd = new_abs_cmnd + "\n" + "        " + "G_texCommand_TEX_PN" + preprocessingInterface.makeNameGfConform(cmnd) + "_" + ''.join(command["parameters"]) + " : " + "PN;"
            #Concrete rules
            new_con_cmnd = new_con_cmnd + "\n" + "        " + "G_texCommand_TEX_PN" + preprocessingInterface.makeNameGfConform(cmnd) + "_" + ''.join(command["parameters"]) + " = \"\\" + cmnd + "\";"
            if (new_abs_cmnd not in abs_cmnd) and (new_con_cmnd not in con_cmnd):
                abs_cmnd = abs_cmnd + new_abs_cmnd
                con_cmnd = con_cmnd + new_con_cmnd
        else:
            print("\nERROR: Grammar Generation: KeyError: 'parameters' for: " + str(command))
    
    con_cmnd = con_cmnd.replace("G_texCommand_TEX_brackets = \"\\\" ++ \"{ } { }\";", "")
    con_cmnd = con_cmnd.replace("G_texCommand_TEX_brackets_stringList fields = \"\\\" ++ \"{ } { } [\" ++ fields ++ \"]\";", "")
    con_cmnd = con_cmnd.replace("G_texCommand_TEX_exclamation = \"\\\" ++ \"!\";", "")

    #Concatinate base and generated grammar rules
    splittedAbstr = abstrSyntaxBase.split("-- SPLIT1")
    splittedConcr = concrSyntaxBase.split("-- SPLIT1")
    abstractSyntax = splittedAbstr[0] + "\n        -- SPLIT1" + abs_cmnd + splittedAbstr[1] + "\n        -- SPLIT1" + abs_var + splittedAbstr[2] + "\n        -- SPLIT1" + abs_defis + "" + splittedAbstr[3]
    concreteSyntax = splittedConcr[0] + "\n        -- SPLIT1" + con_cmnd + splittedConcr[1] + "\n        -- SPLIT1" + con_var + splittedConcr[2] + "\n        -- SPLIT1" + con_defis + "" + splittedConcr[3]
    concreteSyntax = escapeCmds(concreteSyntax)
    with open("sTeX\Grammar\GEN_grammar_abstr.gf", 'w') as gf_file:
        gf_file.write(abstractSyntax)
    with open("sTeX\Grammar\GEN_grammar_concr.gf", 'w') as gf_file:
        gf_file.write(concreteSyntax)