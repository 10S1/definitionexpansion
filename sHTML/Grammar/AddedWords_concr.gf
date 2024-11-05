concrete AddedWords_concr of AddedWords_abstr = GrammarEng, MathTermsEng, MorphoDictEng ** open ParadigmsEng, SymbolicEng, ResEng, IrregEng, ExtraEng, ExtendEng in {	  
        
	lin
        
        powerset_N = mkN "powerset";
        nonDashtrivialSpacedivisor_N = mkN "non - trivial divisor";
        nonDashempty_A = mkA "non - empty";
        how_Adv = mkAdv "how";
        represent_V2 = mkV2 "represent";
        include_V2 = mkV2 "include";
        realize_V2 = mkV2 "realize";
        concerned_A = mkA "concerned";
        iff_Conj = mkConj "iff";
        next_Adv = mkAdv "next";
        have_VV = mkVV IrregEng.have_V;
        choose_V2 = mkV2 (IrregEng.choose_V);
        take_V2 = mkV2 (IrregEng.take_V);
        
}