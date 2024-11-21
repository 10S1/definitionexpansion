abstract AddedTags_abstr = Grammar, MathTags_abstr ** {

    fun
--         tag : Int -> Tag;



        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html

        WRAP_A : Tag -> A -> A;
        WRAP_A2 : Tag -> A2 -> A2;
        WRAP_ACard : Tag -> ACard -> ACard;

        WRAP_AP : Tag -> AP -> AP;
        WRAP_AdA : Tag -> AdA -> AdA;
        WRAP_AdN : Tag -> AdN -> AdN;
        WRAP_AdV : Tag -> AdV -> AdV;
        WRAP_Adv : Tag -> Adv -> Adv;

        WRAP_Ant : Tag -> Ant -> Ant;
        WRAP_CAdv : Tag -> CAdv -> CAdv;
        WRAP_CN : Tag -> CN -> CN;
        WRAP_Card : Tag -> Card -> Card;
        WRAP_Cl : Tag -> Cl -> Cl;
                
        WRAP_ClSlash : Tag -> ClSlash -> ClSlash;
        WRAP_Comp : Tag -> Comp -> Comp;
        WRAP_Conj : Tag -> Conj -> Conj;
        WRAP_DAP : Tag -> DAP -> DAP;
        WRAP_Det : Tag -> Det -> Det;
                        
        WRAP_Dig : Tag -> Dig -> Dig;
        WRAP_Digits : Tag -> Digits -> Digits;
        WRAP_IAdv : Tag -> IAdv -> IAdv;
        WRAP_IComp : Tag -> IComp -> IComp;
        WRAP_IDet : Tag -> IDet -> IDet;
                        
        WRAP_IP : Tag -> IP -> IP;
        WRAP_IQuant : Tag -> IQuant -> IQuant;
        WRAP_Imp : Tag -> Imp -> Imp;
        -- WRAP_ImpForm : Tag -> ImpForm -> ImpForm;
        WRAP_Interj : Tag -> Interj -> Interj;

        WRAP_ListAP : Tag -> ListAP -> ListAP;
        WRAP_ListAdv : Tag -> ListAdv -> ListAdv;
        WRAP_ListNP : Tag -> ListNP -> ListNP;
        WRAP_ListRS : Tag -> ListRS -> ListRS;
        WRAP_ListS : Tag -> ListS -> ListS;

        WRAP_N : Tag -> N -> N;
        WRAP_N2 : Tag -> N2 -> N2;
        WRAP_N3 : Tag -> N3 -> N3;
        WRAP_NP : Tag -> NP -> NP;
        -- WRAP_Num : Tag -> Num -> Num;

        WRAP_Numeral : Tag -> Numeral -> Numeral;
        WRAP_Ord : Tag -> Ord -> Ord;
        WRAP_PConj : Tag -> PConj -> PConj;
        WRAP_PN : Tag -> PN -> PN;
        WRAP_Phr : Tag -> Phr -> Phr;

        WRAP_Pol : Tag -> Pol -> Pol;
        WRAP_Predet : Tag -> Predet -> Predet;
        WRAP_Prep : Tag -> Prep -> Prep;
        WRAP_Pron : Tag -> Pron -> Pron;
        -- WRAP_Punct : Tag -> Punct -> Punct;

        WRAP_QCl : Tag -> QCl -> QCl;
        WRAP_QS : Tag -> QS -> QS;
        WRAP_RCl : Tag -> RCl -> RCl;
        WRAP_RP : Tag -> RP -> RP;
        WRAP_RS : Tag -> RS -> RS;

        WRAP_S : Tag -> S -> S;
        WRAP_SC : Tag -> SC -> SC;
        WRAP_SSlash : Tag -> SSlash -> SSlash;
        WRAP_Sub100 : Tag -> Sub100 -> Sub100;
        WRAP_Sub1000 : Tag -> Sub1000 -> Sub1000;

        WRAP_Subj : Tag -> Subj -> Subj;
        WRAP_Temp : Tag -> Temp -> Temp;
        WRAP_Tense : Tag -> Tense -> Tense;
        WRAP_Text : Tag -> Text -> Text;
        -- WRAP_Unit : Tag -> Unit -> Unit;

        WRAP_Utt : Tag -> Utt -> Utt;
        WRAP_V : Tag -> V -> V;
        WRAP_V2 : Tag -> V2 -> V2;
        WRAP_V2A : Tag -> V2A -> V2A;
        WRAP_V2Q : Tag -> V2Q -> V2Q;

        WRAP_V2S : Tag -> V2S -> V2S;
        WRAP_V2V : Tag -> V2V -> V2V;
        WRAP_V3 : Tag -> V3 -> V3;
        WRAP_VA : Tag -> VA -> VA;
        WRAP_VP : Tag -> VP -> VP;

        WRAP_VPSlash : Tag -> VPSlash -> VPSlash;
        WRAP_VQ : Tag -> VQ -> VQ;
        WRAP_VS : Tag -> VS -> VS;
        WRAP_VV : Tag -> VV -> VV;
        WRAP_Voc : Tag -> Voc -> Voc;

}