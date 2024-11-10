abstract PlaceholderCat_abstr = Grammar, MathTerms, MorphoDictEngAbs, AddedTags_abstr, AddedStructures_abstr, AddedWords_abstr ** {
	cat
        PlaceholderCat;

	data
        -- Own categories

        PlaceholderCat_Tag : Tag -> PlaceholderCat;



        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html

        PlaceholderCat_A : A -> PlaceholderCat;
        PlaceholderCat_A2 : A2 -> PlaceholderCat;
        PlaceholderCat_ACard : ACard -> PlaceholderCat;

        PlaceholderCat_AP : AP -> PlaceholderCat;
        PlaceholderCat_AdA : AdA -> PlaceholderCat;
        PlaceholderCat_AdN : AdN -> PlaceholderCat;
        PlaceholderCat_AdV : AdV -> PlaceholderCat;
        PlaceholderCat_Adv : Adv -> PlaceholderCat;

        PlaceholderCat_Ant : Ant -> PlaceholderCat;
        PlaceholderCat_CAdv : CAdv -> PlaceholderCat;
        PlaceholderCat_CN : CN -> PlaceholderCat;
        PlaceholderCat_Card : Card -> PlaceholderCat;
        PlaceholderCat_Cl : Cl -> PlaceholderCat;
                
        PlaceholderCat_ClSlash : ClSlash -> PlaceholderCat;
        PlaceholderCat_Comp : Comp -> PlaceholderCat;
        PlaceholderCat_Conj : Conj -> PlaceholderCat;
        PlaceholderCat_DAP : DAP -> PlaceholderCat;
        PlaceholderCat_Det : Det -> PlaceholderCat;
                        
        PlaceholderCat_Dig : Dig -> PlaceholderCat;
        PlaceholderCat_Digits : Digits -> PlaceholderCat;
        PlaceholderCat_IAdv : IAdv -> PlaceholderCat;
        PlaceholderCat_IComp : IComp -> PlaceholderCat;
        PlaceholderCat_IDet : IDet -> PlaceholderCat;
                        
        PlaceholderCat_IP : IP -> PlaceholderCat;
        PlaceholderCat_IQuant : IQuant -> PlaceholderCat;
        PlaceholderCat_Imp : Imp -> PlaceholderCat;
        -- PlaceholderCat_ImpForm : ImpForm -> PlaceholderCat;
        PlaceholderCat_Interj : Interj -> PlaceholderCat;

        PlaceholderCat_ListAP : ListAP -> PlaceholderCat;
        PlaceholderCat_ListAdv : ListAdv -> PlaceholderCat;
        PlaceholderCat_ListNP : ListNP -> PlaceholderCat;
        PlaceholderCat_ListRS : ListRS -> PlaceholderCat;
        PlaceholderCat_ListS : ListS -> PlaceholderCat;

        PlaceholderCat_N : N -> PlaceholderCat;
        PlaceholderCat_N2 : N2 -> PlaceholderCat;
        PlaceholderCat_N3 : N3 -> PlaceholderCat;
        PlaceholderCat_NP : NP -> PlaceholderCat;
        PlaceholderCat_Num : Num -> PlaceholderCat;

        PlaceholderCat_Numeral : Numeral -> PlaceholderCat;
        PlaceholderCat_Ord : Ord -> PlaceholderCat;
        PlaceholderCat_PConj : PConj -> PlaceholderCat;
        PlaceholderCat_PN : PN -> PlaceholderCat;
        PlaceholderCat_Phr : Phr -> PlaceholderCat;

        PlaceholderCat_Pol : Pol -> PlaceholderCat;
        PlaceholderCat_Predet : Predet -> PlaceholderCat;
        PlaceholderCat_Prep : Prep -> PlaceholderCat;
        PlaceholderCat_Pron : Pron -> PlaceholderCat;
        -- PlaceholderCat_Punct : Punct -> PlaceholderCat;

        PlaceholderCat_QCl : QCl -> PlaceholderCat;
        PlaceholderCat_QS : QS -> PlaceholderCat;
        PlaceholderCat_RCl : RCl -> PlaceholderCat;
        PlaceholderCat_RP : RP -> PlaceholderCat;
        PlaceholderCat_RS : RS -> PlaceholderCat;

        PlaceholderCat_S : S -> PlaceholderCat;
        PlaceholderCat_SC : SC -> PlaceholderCat;
        PlaceholderCat_SSlash : SSlash -> PlaceholderCat;
        PlaceholderCat_Sub100 : Sub100 -> PlaceholderCat;
        PlaceholderCat_Sub1000 : Sub1000 -> PlaceholderCat;

        PlaceholderCat_Subj : Subj -> PlaceholderCat;
        PlaceholderCat_Temp : Temp -> PlaceholderCat;
        PlaceholderCat_Tense : Tense -> PlaceholderCat;
        PlaceholderCat_Text : Text -> PlaceholderCat;
        -- PlaceholderCat_Unit : Unit -> PlaceholderCat;

        PlaceholderCat_Utt : Utt -> PlaceholderCat;
        PlaceholderCat_V : V -> PlaceholderCat;
        PlaceholderCat_V2 : V2 -> PlaceholderCat;
        PlaceholderCat_V2A : V2A -> PlaceholderCat;
        PlaceholderCat_V2Q : V2Q -> PlaceholderCat;

        PlaceholderCat_V2S : V2S -> PlaceholderCat;
        PlaceholderCat_V2V : V2V -> PlaceholderCat;
        PlaceholderCat_V3 : V3 -> PlaceholderCat;
        PlaceholderCat_VA : VA -> PlaceholderCat;
        PlaceholderCat_VP : VP -> PlaceholderCat;

        PlaceholderCat_VPSlash : VPSlash -> PlaceholderCat;
        PlaceholderCat_VQ : VQ -> PlaceholderCat;
        PlaceholderCat_VS : VS -> PlaceholderCat;
        PlaceholderCat_VV : VV -> PlaceholderCat;
        PlaceholderCat_Voc : Voc -> PlaceholderCat;
}