abstract GEN_grammar_abstr = Grammar, MathTerms, MorphoDictEngAbs ** {
	cat
        -- Unknown
        U_all;
        -- Symbolic Expressions
        C_symbolicExpression; 
        C_texCommand; 
        C_texArgument; 
        C_texArguments; 
        C_number; 
        C_variable; 
        C_multipleSymbolicExpression;
        C_formula;
        C_strList;

	data
        -- Unknown ------------------------------------------------------------------------------------------------------------------------------------------------------
        -- Symbolic Expressions
        U_symbolicExpression : C_symbolicExpression -> U_all;
        U_texCommand : C_texCommand -> U_all;       
        U_texArgument : C_texArgument -> U_all;
        U_texArguments : C_texArguments -> U_all;       
        U_number : C_number -> U_all;
        U_variable : C_variable -> U_all;
        U_multipleSymbolicExpression : C_multipleSymbolicExpression -> U_all;
        U_formula: C_formula -> U_all;   
        U_strList: C_strList -> U_all;

        -- New ------------------------------------------------------------------------------------------------------------------------------------------------------------
        powerset_N : N;
        nonDashtrivialSpacedivisor_N : N;
        nonDashempty_A : A;
        S_definiendum_WWS_definiendum_WWnonDashempty_S : S -> S;
        how_Adv : Adv;
        representing_V2 : V2;
        include_V2 : V2;
        realizing_V2 : V2;
        concerned_A : A;
        
        -- C_strList
        R_strList_Str : String -> C_strList;
        R_strList_strList_strList : C_strList -> C_strList -> C_strList;
        
        -- Math specific
        R_formula_symbolicExpression : C_symbolicExpression -> C_formula;
        R_np_formula : C_formula -> NP;
        R_s_formula : C_formula -> S;
        R_utt_formula : C_formula -> Utt;

        letUs_Utt : Utt -> S;

        iff_Conj : Conj;
        next_Adv : Adv;
        -- having: "let $ \\fvar $ be a function from $ \\Avar $ to $ \\Yvar $ having a fixed point in $ \\Xvar $"
        have_VV : VV;
        -- choose: "thus we can choose an injective function"
        choose_V2 : V2;
        -- take: "take a finite basis of the product of $ \\Vvar $ and $ \\Wvar $"
        take_V2 : V2;

        let_np_be_np_S : NP -> NP -> S;
        np_is_called_np : NP -> NP -> S;
        np_is_called_ap : NP -> AP -> S;
        S_assume_S : S -> S;

        -- SMGloM specific
        -- definiendum
        mt_to_np : MT -> NP;
        --mt_to_n : MT -> N;
        VtoV2 : V -> V2;

        -- definame
        N_definame_N : N -> N;
        A_definame_A : A -> A;
        V_definame_V : V -> V;
        CN_definame_CN : CN -> CN;
        NP_definame_NP : NP -> NP;


        -- sn
        N_sn_N : N -> N;
        A_sn_A : A -> A;
        V_sn_V : V -> V;
        N_sns_N : N -> N;
        A_sns_A : A -> A;
        V_sns_V : V -> V;
        N_Sn_N : N -> N;
        A_Sn_A : A -> A;
        V_Sn_V : V -> V;
        N_Sns_N : N -> N;
        A_Sns_A : A -> A;
        V_Sns_V : V -> V;
        N_Symname_N : N -> N;
        A_Symname_A : A -> A;
        V_Symname_V : V -> V;
        N_symname_N : N -> N;
        A_symname_A : A -> A;
        V_symname_V : V -> V;

        -- definiens
        NP_NP_definiens_NP : NP -> NP -> NP;
        --S_definiens_A_S : A -> S -> S;
        --S_definiens_V_S : V -> S -> S;
        
        
        -- Multiples ------------------------------------------------------------------------------------------------------------------------------------------------------
        -- SymbolicExpression
        D_multipleSymbolicExpression_symbolicExpression : C_symbolicExpression -> C_multipleSymbolicExpression;
        D_multipleSymbolicExpression_multipleSymbolicExpression_multipleSymbolicExpression : C_multipleSymbolicExpression -> C_multipleSymbolicExpression -> C_multipleSymbolicExpression;
        

        -- Symbolic Expressions ------------------------------------------------------------------------------------------------------------------------------------------------------
        -- <symbolic expression> = <tex command>
        R_symbolicExpression_texCommand : C_texCommand -> C_symbolicExpression;
        -- | <number>
        R_symbolicExpression_number : C_number -> C_symbolicExpression;
        -- | <variable>
        R_symbolicExpression_variable : C_variable -> C_symbolicExpression;
        
        -- <tex command> = ("\\union" | "\\setst" | ...) {<tex argument> | <tex arguments>}
        -- AUTOMATICALLY GENERATED
        -- SPLIT1

        -- <tex argument> = "{" <symbolic expression> "}"
        R_texArgument_symbolicExpression : C_symbolicExpression -> C_texArgument;

        -- <tex arguments> = "{" <symbolic expression> { "," <symbolic expression> } "}"
        R_texArguments_symbolicExpression : C_symbolicExpression -> C_texArguments;
        R_texArguments_symbolicExpression_multipleSymbolicExpression : C_symbolicExpression -> C_multipleSymbolicExpression -> C_texArguments;


        -- <number> = Int
        R_number_int : Int -> C_number;

        -- <str> = Str

        -- <variable> = "\\xvar" | "\\fvarExclamation" | ...
        -- AUTOMATICALLY GENERATED
        -- SPLIT1

        -- Words ------------------------------------------------------------------------------------------------------------------------------------------------------------
        -- AUTOMATICALLY GENERATED
        -- SPLIT1

}