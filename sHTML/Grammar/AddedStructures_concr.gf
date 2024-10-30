concrete AddedStructures_concr of AddedStructures_abstr = GrammarEng, ** open ParadigmsEng, SymbolicEng, ResEng, IrregEng in {	
    
    lincat
        
	lin
        
        letUs_Utt ut = { s = "let us" ++ ut.s};

        let_np_be_np_S np1 np2 = {s = "let" ++ np1.s ! (NCase Nom) ++ "be" ++ np2.s ! (NCase Nom)};

        np_is_called_np np1 np2 = {s = np1.s ! (NCase Nom) ++ "is called" ++ np2.s ! (NCase Nom)};

        np_is_called_ap np ap = {s = np.s ! (NCase Nom) ++ "is called" ++ ap.s ! np.a};

        S_assume_S sen = { s = ("assume" | "suppose") ++ ("that" | "") ++ sen.s };
        

        -- definiendum
        mt_to_np mt = symb mt.s;
        VtoV2 v = mkV2 v;
        
}