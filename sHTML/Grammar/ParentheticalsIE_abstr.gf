abstract ParentheticalsIE_abstr = Grammar ** {

    fun

        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html

        IE_A : Utt -> A -> A;
        IE_A2 : Utt -> A2 -> A2;
        IE_ACard : Utt -> ACard -> ACard;

        IE_AP : Utt -> AP -> AP;
        IE_AdA : Utt -> AdA -> AdA;
        IE_AdN : Utt -> AdN -> AdN;
        IE_AdV : Utt -> AdV -> AdV;
        IE_Adv : Utt -> Adv -> Adv;

        IE_Ant : Utt -> Ant -> Ant;
        IE_CAdv : Utt -> CAdv -> CAdv;
        IE_CN : Utt -> CN -> CN;
        IE_Card : Utt -> Card -> Card;
        IE_Cl : Utt -> Cl -> Cl;
                
        IE_ClSlash : Utt -> ClSlash -> ClSlash;
        IE_Comp : Utt -> Comp -> Comp;
        IE_Conj : Utt -> Conj -> Conj;
        IE_DAP : Utt -> DAP -> DAP;
        IE_Det : Utt -> Det -> Det;
                        
        IE_Dig : Utt -> Dig -> Dig;
        IE_Digits : Utt -> Digits -> Digits;
        IE_IAdv : Utt -> IAdv -> IAdv;
        IE_IComp : Utt -> IComp -> IComp;
        IE_IDet : Utt -> IDet -> IDet;
                        
        IE_IP : Utt -> IP -> IP;
        IE_IQuant : Utt -> IQuant -> IQuant;
        IE_Imp : Utt -> Imp -> Imp;
        -- IE_ImpForm : Utt -> ImpForm -> ImpForm;
        IE_Interj : Utt -> Interj -> Interj;

        IE_ListAP : Utt -> ListAP -> ListAP;
        IE_ListAdv : Utt -> ListAdv -> ListAdv;
        IE_ListNP : Utt -> ListNP -> ListNP;
        IE_ListRS : Utt -> ListRS -> ListRS;
        IE_ListS : Utt -> ListS -> ListS;

        IE_N : Utt -> N -> N;
        IE_N2 : Utt -> N2 -> N2;
        IE_N3 : Utt -> N3 -> N3;
        IE_NP : Utt -> NP -> NP;
        IE_Num : Utt -> Num -> Num;

        IE_Numeral : Utt -> Numeral -> Numeral;
        IE_Ord : Utt -> Ord -> Ord;
        IE_PConj : Utt -> PConj -> PConj;
        IE_PN : Utt -> PN -> PN;
        IE_Phr : Utt -> Phr -> Phr;

        IE_Pol : Utt -> Pol -> Pol;
        IE_Predet : Utt -> Predet -> Predet;
        IE_Prep : Utt -> Prep -> Prep;
        IE_Pron : Utt -> Pron -> Pron;
        -- IE_Punct : Utt -> Punct -> Punct;

        IE_QCl : Utt -> QCl -> QCl;
        IE_QS : Utt -> QS -> QS;
        IE_RCl : Utt -> RCl -> RCl;
        IE_RP : Utt -> RP -> RP;
        IE_RS : Utt -> RS -> RS;

        IE_S : Utt -> S -> S;
        IE_SC : Utt -> SC -> SC;
        IE_SSlash : Utt -> SSlash -> SSlash;
        IE_Sub100 : Utt -> Sub100 -> Sub100;
        IE_Sub1000 : Utt -> Sub1000 -> Sub1000;

        IE_Subj : Utt -> Subj -> Subj;
        IE_Temp : Utt -> Temp -> Temp;
        IE_Tense : Utt -> Tense -> Tense;
        IE_Text : Utt -> Text -> Text;
        -- IE_Unit : Utt -> Unit -> Unit;

        IE_Utt : Utt -> Utt -> Utt;
        IE_V : Utt -> V -> V;
        IE_V2 : Utt -> V2 -> V2;
        IE_V2A : Utt -> V2A -> V2A;
        IE_V2Q : Utt -> V2Q -> V2Q;

        IE_V2S : Utt -> V2S -> V2S;
        IE_V2V : Utt -> V2V -> V2V;
        IE_V3 : Utt -> V3 -> V3;
        IE_VA : Utt -> VA -> VA;
        IE_VP : Utt -> VP -> VP;

        IE_VPSlash : Utt -> VPSlash -> VPSlash;
        IE_VQ : Utt -> VQ -> VQ;
        IE_VS : Utt -> VS -> VS;
        IE_VV : Utt -> VV -> VV;
        IE_Voc : Utt -> Voc -> Voc;

}