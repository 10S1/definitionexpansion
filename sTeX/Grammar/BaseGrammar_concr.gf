concrete GEN_grammar_concr of GEN_grammar_abstr = GrammarEng, MathTermsEng, MorphoDictEng ** open ParadigmsEng, SymbolicEng, ResEng, IrregEng, ExtraEng, ExtendEng in {	lincat
        -- Unknown
        U_all = Str;
        -- Symbolic Expressions
        C_symbolicExpression = Str; 
        C_texCommand = Str; 
        C_texArgument = Str; 
        C_texArguments = Str; 
        C_number = Str; 
        C_variable = Str;
        C_multipleSymbolicExpression = Str; 
        C_formula = Str;
        C_strList = Str;

	lin
        -- Unknown ------------------------------------------------------------------------------------------------------------------------------------------------------
        -- Symbolic Expressions
        U_symbolicExpression u = u;
        U_texCommand u = u;       
        U_texArgument u = u;
        U_texArguments u = u;    
        U_number u = u;
        U_variable u = u;
        U_multipleSymbolicExpression u = u;    
        U_formula u = u;
        U_strList u = u;

        -- New ------------------------------------------------------------------------------------------------------------------------------------------------------------
        S_definiendum_WWS_definiendum_WWnonDashempty_S sen = { s = "\\definiens [" ++ "non - empty" ++ "] {" ++ sen.s ++ "}" };
        powerset_N = mkN "powerset";
        nonDashtrivialSpacedivisor_N = mkN "non - trivial divisor";
        nonDashempty_A = mkA "non - empty";
        how_Adv = mkAdv "how";
        represent_V2 = mkV2 "represent";
        include_V2 = mkV2 "include";
        realize_V2 = mkV2 "realize";
        concerned_A = mkA "concerned";
        
        -- C_strList
        R_strList_Str s = s.s;
        R_strList_strList_strList a b = a ++ "," ++ b;

        -- Math specific
        R_formula_symbolicExpression sym = "$" ++ sym ++ "$";
        R_np_formula f = symb f;
        R_s_formula f = {s = f};
        R_utt_formula f = {s = f};

        letUs_Utt ut = { s = "let us" ++ ut.s};

        iff_Conj = mkConj "iff";
        next_Adv = mkAdv "next";
        -- having: "let $ \\fvar $ be a function from $ \\Avar $ to $ \\Yvar $ having a fixed point in $ \\Xvar $"
        have_VV = mkVV IrregEng.have_V;
        -- choose: "thus we can choose an injective function"
        choose_V2 = mkV2 (IrregEng.choose_V);
        -- take: "take a finite basis of the product of $ \\Vvar $ and $ \\Wvar $"
        take_V2 = mkV2 (IrregEng.take_V);

        let_np_be_np_S np1 np2 = {s = "let" ++ np1.s ! (NCase Nom) ++ "be" ++ np2.s ! (NCase Nom)};
        np_is_called_np np1 np2 = {s = np1.s ! (NCase Nom) ++ "is called" ++ np2.s ! (NCase Nom)};
        np_is_called_ap np ap = {s = np.s ! (NCase Nom) ++ "is called" ++ ap.s ! np.a};
        S_assume_S sen = { s = ("assume" | "suppose") ++ ("that" | "") ++ sen.s };
        --S_definiens_N_S n sen = { s = "\\definiens [" ++ n.s ! Sg ! Nom ++ "]{" ++ sen.s ++ "}" };

        --------------------------------------------------------------------------------------------------------------

        -- SMGloM specific

        -- definiendum
        mt_to_np mt = symb mt.s;
        --mt_to_n mt = mkN mt.s;
        VtoV2 v = mkV2 v;
        
        -- definame
        N_definame_N n = { s = table { num => table { c => "\\definame {" ++ n.s ! num ! c ++ "}"} }; g = n.g};
        A_definame_A a = { s = table { af => "\\definame {" ++ a.s ! af ++" }"}; isPre = a.isPre; isMost = a.isMost};
        V_definame_V v = { s = table { vf => "\\definame {" ++ v.s ! vf ++ "}"}; p = v.p; isRefl = v.isRefl};
        CN_definame_CN cn = { s = table { num => table { c => "\\definame {" ++ cn.s ! num ! c ++ "}" } }; g = cn.g};
        NP_definame_NP np = { s = table { npCase => "\\definame {" ++ np.s ! npCase ++ "}" }; a = np.a};

        -- sn
        N_sn_N n = { s = table { num => table { c => "\\sn {" ++ n.s ! num ! c ++ "}"} }; g = n.g};
        A_sn_A a = { s = table { af => "\\sn {" ++ a.s ! af ++" }"}; isPre = a.isPre; isMost = a.isMost};
        V_sn_V v = { s = table { vf => "\\sn {" ++ v.s ! vf ++ "}"}; p = v.p; isRefl = v.isRefl};
        N_sns_N n = { s = table { num => table { c => "\\sns {" ++ n.s ! num ! c ++ "}"} }; g = n.g};
        A_sns_A a = { s = table { af => "\\sns {" ++ a.s ! af ++" }"}; isPre = a.isPre; isMost = a.isMost};
        V_sns_V v = { s = table { vf => "\\sns {" ++ v.s ! vf ++ "}"}; p = v.p; isRefl = v.isRefl};
        N_Sn_N n = { s = table { num => table { c => "\\Sn {" ++ n.s ! num ! c ++ "}"} }; g = n.g};
        A_Sn_A a = { s = table { af => "\\Sn {" ++ a.s ! af ++" }"}; isPre = a.isPre; isMost = a.isMost};
        V_Sn_V v = { s = table { vf => "\\Sn {" ++ v.s ! vf ++ "}"}; p = v.p; isRefl = v.isRefl};
        N_Sns_N n = { s = table { num => table { c => "\\Sns {" ++ n.s ! num ! c ++ "}"} }; g = n.g};
        A_Sns_A a = { s = table { af => "\\Sns {" ++ a.s ! af ++" }"}; isPre = a.isPre; isMost = a.isMost};
        V_Sns_V v = { s = table { vf => "\\Sns {" ++ v.s ! vf ++ "}"}; p = v.p; isRefl = v.isRefl};
        N_Symname_N n = { s = table { num => table { c => "\\Symname {" ++ n.s ! num ! c ++ "}"} }; g = n.g};
        A_Symname_A a = { s = table { af => "\\Symname {" ++ a.s ! af ++" }"}; isPre = a.isPre; isMost = a.isMost};
        V_Symname_V v = { s = table { vf => "\\Symname {" ++ v.s ! vf ++ "}"}; p = v.p; isRefl = v.isRefl};
        N_symname_N n = { s = table { num => table { c => "\\symname {" ++ n.s ! num ! c ++ "}"} }; g = n.g};
        A_symname_A a = { s = table { af => "\\symname {" ++ a.s ! af ++" }"}; isPre = a.isPre; isMost = a.isMost};
        V_symname_V v = { s = table { vf => "\\symname {" ++ v.s ! vf ++ "}"}; p = v.p; isRefl = v.isRefl};
        
        -- definiens          "\\definiens" "[" <identifier> "]" "{" <indefinite article> <notion> "}"
        --S_definiens_N_S n sen = { s = "\\definiens [" ++ n.s ! Sg ! Nom ++ "]{" ++ sen.s ++ "}" };
        --S_definiens_N_S n sen = { s = table { num => table { c => "\\definiens [" ++ n.s ! num ! c ++ "]"} }; g = n.g} ++ "{" ++ sen.s ++ "}";
        --S_definiens_A_S a sen = { s = table { af => "\\definiens [" ++ a.s ! af ++ "]"}; isPre = a.isPre; isMost = a.isMost} ++ "{" ++ sen.s ++ "}";
        --S_definiens_V_S v sen = { s = table { vf => "\\definiens [" ++ v.s ! vf ++ "]"}; p = v.p; isRefl = v.isRefl} ++ "{" ++ sen.s ++ "}";
        --NP_NP_definiens_NP n1 n2 = { s = table { num => table { c => "\\definiens [" ++  n1.s ! num ! c ++ "] {" ++ n2.s ! num ! c ++ "}"} }; g = n2.g};

        -- Multiples ------------------------------------------------------------------------------------------------------------------------------------------------------
        -- multiple symbolic expression
        D_multipleSymbolicExpression_symbolicExpression sy = "," ++ sy;
        D_multipleSymbolicExpression_multipleSymbolicExpression_multipleSymbolicExpression a b = a ++ b;


        -- Symbolic Expressions ------------------------------------------------------------------------------------------------------------------------------------------------------
        -- <symbolic expression> = <tex command>
        R_symbolicExpression_texCommand a = a; 
        -- | <number>
        R_symbolicExpression_number a = a;
        -- | <variable>
        R_symbolicExpression_variable a = a;
        
        -- <tex command> = ("\\union" | "\\setst" | ...) {<tex argument> | <tex arguments>}
        -- AUTOMATICALLY GENERATED
        -- SPLIT1

        -- <tex argument> = "{" <symbolic expression> "}"
        R_texArgument_symbolicExpression n = "{" ++ n ++ "}";

        -- <tex arguments> = "{" <symbolic expression> { "," <symbolic expression> } "}"
        R_texArguments_symbolicExpression n = "{" ++ n ++ "}";
        R_texArguments_symbolicExpression_multipleSymbolicExpression a b = "{" ++ a ++ b ++ "}";

        -- <number> = Int
        R_number_int i = i.s;

        -- <variable> = "\\xvar" | "\\fvarExclamation" | ...
        -- AUTOMATICALLY GENERATED
        -- SPLIT1

        -- Words ------------------------------------------------------------------------------------------------------------------------------------------------------------
        -- AUTOMATICALLY GENERATED
        -- SPLIT1
   
}