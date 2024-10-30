abstract AddedTags_abstr = {

    cat
        Tag;


    fun
        tag : Int -> Tag;
        
    

        wrap_A : Tag -> A -> A;
        wrap_A2 : Tag -> A2 -> A2;
        wrap_ACard : Tag -> ACard -> ACard;

        wrap_AP : Tag -> AP -> AP;
        wrap_AdA : Tag -> AdA -> AdA;
        wrap_AdN : Tag -> AdN -> AdN;
        wrap_AdV : Tag -> AdV -> AdV;
        wrap_Adv : Tag -> Adv -> Adv;

        wrap_Ant : Tag -> Ant -> Ant;
        wrap_CAdv : Tag -> CAdv -> CAdv;
        wrap_CN : Tag -> CN -> CN;
        wrap_Card : Tag -> Card -> Card;
        wrap_Cl : Tag -> Cl -> Cl;
                
        wrap_ClSlash : Tag -> ClSlash -> ClSlash;
        wrap_Comp : Tag -> Comp -> Comp;
        wrap_Conj : Tag -> Conj -> Conj;
        wrap_DAP : Tag -> DAP -> DAP;
        wrap_Det : Tag -> Det -> Det;
                        
        wrap_Dig : Tag -> Dig -> Dig;
        wrap_Digits : Tag -> Digits -> Digits;
        wrap_IAdv : Tag -> IAdv -> IAdv;
        wrap_IComp : Tag -> IComp -> IComp;
        wrap_IDet : Tag -> IDet -> IDet;
                        
        wrap_IP : Tag -> IP -> IP;
        wrap_IQuant : Tag -> IQuant -> IQuant;
        wrap_Imp : Tag -> Imp -> Imp;
        wrap_ImpForm : Tag -> ImpForm -> ImpForm;
        wrap_Interj : Tag -> Interj -> Interj;

        wrap_ListAP : Tag -> ListAP -> ListAP;
        wrap_ListAdv : Tag -> ListAdv -> ListAdv;
        wrap_ListNP : Tag -> ListNP -> ListNP;
        wrap_ListRS : Tag -> ListRS -> ListRS;
        wrap_ListS : Tag -> ListS -> ListS;

        wrap_N : Tag -> N -> N;
        wrap_N2 : Tag -> N2 -> N2;
        wrap_N3 : Tag -> N3 -> N3;
        wrap_NP : Tag -> NP -> NP;
        wrap_Num : Tag -> Num -> Num;

        wrap_Numeral : Tag -> Numeral -> Numeral;
        wrap_Ord : Tag -> Ord -> Ord;
        wrap_PConj : Tag -> PConj -> PConj;
        wrap_PN : Tag -> PN -> PN;
        wrap_Phr : Tag -> Phr -> Phr;

        wrap_Pol : Tag -> Pol -> Pol;
        wrap_Predet : Tag -> Predet -> Predet;
        wrap_Prep : Tag -> Prep -> Prep;
        wrap_Pron : Tag -> Pron -> Pron;
        wrap_Punct : Tag -> Punct -> Punct;

        wrap_QCl : Tag -> QCl -> QCl;
        wrap_QS : Tag -> QS -> QS;
        wrap_RCl : Tag -> RCl -> RCl;
        wrap_RP : Tag -> RP -> RP;
        wrap_RS : Tag -> RS -> RS;

        wrap_S : Tag -> S -> S;
        wrap_SC : Tag -> SC -> SC;
        wrap_SSlash : Tag -> SSlash -> SSlash;
        wrap_Sub100 : Tag -> Sub100 -> Sub100;
        wrap_Sub1000 : Tag -> Sub1000 -> Sub1000;

        wrap_Subj : Tag -> Subj -> Subj;
        wrap_Temp : Tag -> Temp -> Temp;
        wrap_Tense : Tag -> Tense -> Tense;
        wrap_Text : Tag -> Text -> Text;
        wrap_Unit : Tag -> Unit -> Unit;

        wrap_Utt : Tag -> Utt -> Utt;
        wrap_V : Tag -> V -> V;
        wrap_V2 : Tag -> V2 -> V2;
        wrap_V2A : Tag -> V2A -> V2A;
        wrap_V2Q : Tag -> V2Q -> V2Q;

        wrap_V2S : Tag -> V2S -> V2S;
        wrap_V2V : Tag -> V2V -> V2V;
        wrap_V3 : Tag -> V3 -> V3;
        wrap_VA : Tag -> VA -> VA;
        wrap_VP : Tag -> VP -> VP;

        wrap_VPSlash : Tag -> VPSlash -> VPSlash;
        wrap_VQ : Tag -> VQ -> VQ;
        wrap_VS : Tag -> VS -> VS;
        wrap_VV : Tag -> VV -> VV;
        wrap_Voc : Tag -> Voc -> Voc;

}