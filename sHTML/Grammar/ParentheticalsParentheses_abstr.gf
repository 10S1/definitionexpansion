abstract ParentheticalsParentheses_abstr = Grammar ** {

    fun

        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html

        PARENTHESES_A : Utt -> A -> A;
        PARENTHESES_A2 : Utt -> A2 -> A2;
        PARENTHESES_ACard : Utt -> ACard -> ACard;

        PARENTHESES_AP : Utt -> AP -> AP;
        PARENTHESES_AdA : Utt -> AdA -> AdA;
        PARENTHESES_AdN : Utt -> AdN -> AdN;
        PARENTHESES_AdV : Utt -> AdV -> AdV;
        PARENTHESES_Adv : Utt -> Adv -> Adv;

        PARENTHESES_Ant : Utt -> Ant -> Ant;
        PARENTHESES_CAdv : Utt -> CAdv -> CAdv;
        PARENTHESES_CN : Utt -> CN -> CN;
        PARENTHESES_Card : Utt -> Card -> Card;
        PARENTHESES_Cl : Utt -> Cl -> Cl;
                
        PARENTHESES_ClSlash : Utt -> ClSlash -> ClSlash;
        PARENTHESES_Comp : Utt -> Comp -> Comp;
        PARENTHESES_Conj : Utt -> Conj -> Conj;
        PARENTHESES_DAP : Utt -> DAP -> DAP;
        PARENTHESES_Det : Utt -> Det -> Det;
                        
        PARENTHESES_Dig : Utt -> Dig -> Dig;
        PARENTHESES_Digits : Utt -> Digits -> Digits;
        PARENTHESES_IAdv : Utt -> IAdv -> IAdv;
        PARENTHESES_IComp : Utt -> IComp -> IComp;
        PARENTHESES_IDet : Utt -> IDet -> IDet;
                        
        PARENTHESES_IP : Utt -> IP -> IP;
        PARENTHESES_IQuant : Utt -> IQuant -> IQuant;
        PARENTHESES_Imp : Utt -> Imp -> Imp;
        -- PARENTHESES_ImpForm : Utt -> ImpForm -> ImpForm;
        PARENTHESES_Interj : Utt -> Interj -> Interj;

        PARENTHESES_ListAP : Utt -> ListAP -> ListAP;
        PARENTHESES_ListAdv : Utt -> ListAdv -> ListAdv;
        PARENTHESES_ListNP : Utt -> ListNP -> ListNP;
        PARENTHESES_ListRS : Utt -> ListRS -> ListRS;
        PARENTHESES_ListS : Utt -> ListS -> ListS;

        PARENTHESES_N : Utt -> N -> N;
        PARENTHESES_N2 : Utt -> N2 -> N2;
        PARENTHESES_N3 : Utt -> N3 -> N3;
        PARENTHESES_NP : Utt -> NP -> NP;
        PARENTHESES_Num : Utt -> Num -> Num;

        PARENTHESES_Numeral : Utt -> Numeral -> Numeral;
        PARENTHESES_Ord : Utt -> Ord -> Ord;
        PARENTHESES_PConj : Utt -> PConj -> PConj;
        PARENTHESES_PN : Utt -> PN -> PN;
        PARENTHESES_Phr : Utt -> Phr -> Phr;

        PARENTHESES_Pol : Utt -> Pol -> Pol;
        PARENTHESES_Predet : Utt -> Predet -> Predet;
        PARENTHESES_Prep : Utt -> Prep -> Prep;
        PARENTHESES_Pron : Utt -> Pron -> Pron;
        -- PARENTHESES_Punct : Utt -> Punct -> Punct;

        PARENTHESES_QCl : Utt -> QCl -> QCl;
        PARENTHESES_QS : Utt -> QS -> QS;
        PARENTHESES_RCl : Utt -> RCl -> RCl;
        PARENTHESES_RP : Utt -> RP -> RP;
        PARENTHESES_RS : Utt -> RS -> RS;

        PARENTHESES_S : Utt -> S -> S;
        PARENTHESES_SC : Utt -> SC -> SC;
        PARENTHESES_SSlash : Utt -> SSlash -> SSlash;
        PARENTHESES_Sub100 : Utt -> Sub100 -> Sub100;
        PARENTHESES_Sub1000 : Utt -> Sub1000 -> Sub1000;

        PARENTHESES_Subj : Utt -> Subj -> Subj;
        PARENTHESES_Temp : Utt -> Temp -> Temp;
        PARENTHESES_Tense : Utt -> Tense -> Tense;
        PARENTHESES_Text : Utt -> Text -> Text;
        -- PARENTHESES_Unit : Utt -> Unit -> Unit;

        PARENTHESES_Utt : Utt -> Utt -> Utt;
        PARENTHESES_V : Utt -> V -> V;
        PARENTHESES_V2 : Utt -> V2 -> V2;
        PARENTHESES_V2A : Utt -> V2A -> V2A;
        PARENTHESES_V2Q : Utt -> V2Q -> V2Q;

        PARENTHESES_V2S : Utt -> V2S -> V2S;
        PARENTHESES_V2V : Utt -> V2V -> V2V;
        PARENTHESES_V3 : Utt -> V3 -> V3;
        PARENTHESES_VA : Utt -> VA -> VA;
        PARENTHESES_VP : Utt -> VP -> VP;

        PARENTHESES_VPSlash : Utt -> VPSlash -> VPSlash;
        PARENTHESES_VQ : Utt -> VQ -> VQ;
        PARENTHESES_VS : Utt -> VS -> VS;
        PARENTHESES_VV : Utt -> VV -> VV;
        PARENTHESES_Voc : Utt -> Voc -> Voc;

}