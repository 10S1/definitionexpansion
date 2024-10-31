concrete AddedTags_concr of AddedTags_abstr = {	

    lincat
        Tag = {s: Str};
        

    lin
        tag i = {s = i.s};
        

        
        wrap_A tag x = { s = table { af => wrap tag (x.s ! af) }; isPre = x.isPre; isMost = x.isMost};
        wrap_A2 tag x = { s = table { af => wrap tag (x.s ! af) }; isPre = x.isPre; isMost = x.isMost; c2 = x.c2};
        wrap_ACard tag x = ;

        wrap_AP tag x = ;
        wrap_AdA tag x = ;
        wrap_AdN tag x = ;
        wrap_AdV tag x = ;
        wrap_Adv tag x = ;

        wrap_Ant tag x = ;
        wrap_CAdv tag x = ;
        wrap_CN tag x = ;
        wrap_Card tag x = ;
        wrap_Cl tag x = ;
                        
        wrap_ClSlash tag x = ;
        wrap_Comp tag x = ;
        wrap_Conj tag x = ;
        wrap_DAP tag x = ;
        wrap_Det tag x = ;
                                
        wrap_Dig tag x = ;
        wrap_Digits tag x = ;
        wrap_IAdv tag x = ;
        wrap_IComp tag x = ;
        wrap_IDet tag x = ;
                                
        wrap_IP tag x = ;
        wrap_IQuant tag x = ;
        wrap_Imp tag x = ;
        wrap_ImpForm tag x = ;
        wrap_Interj tag x = ;

        wrap_ListAP tag x = ;
        wrap_ListAdv tag x = ;
        wrap_ListNP tag x = ;
        wrap_ListRS tag x = ;
        wrap_ListS tag x = ;

        wrap_N tag x = { s = table { num => table { c => wrap tag (x.s ! num ! c) } }; g = x.g };
        wrap_N2 tag x = ;
        wrap_N3 tag x = ;
        wrap_NP tag x = ;
        wrap_Num tag x = ;

        wrap_Numeral tag x = ;
        wrap_Ord tag x = ;
        wrap_PConj tag x = ;
        wrap_PN tag x = ;
        wrap_Phr tag x = ;

        wrap_Pol tag x = ;
        wrap_Predet tag x = ;
        wrap_Prep tag x = ;
        wrap_Pron tag x = ;
        wrap_Punct tag x = ;

        wrap_QCl tag x = ;
        wrap_QS tag x = ;
        wrap_RCl tag x = ;
        wrap_RP tag x = ;
        wrap_RS tag x = ;

        wrap_S tag x = ;
        wrap_SC tag x = ;
        wrap_SSlash tag x = ;
        wrap_Sub100 tag x = ;
        wrap_Sub1000 tag x = ;

        wrap_Subj tag x = ;
        wrap_Temp tag x = ;
        wrap_Tense tag x = ;
        wrap_Text tag x = ;
        wrap_Unit tag x = ;

        wrap_Utt tag x = ;
        wrap_V tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl };
        wrap_V2 tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl; c2 = x.c2 };
        wrap_V2A tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl; c2 = x.c2; c3 = x.c3 };
        wrap_V2Q tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl; c2 = x.c2 };

        wrap_V2S tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl; c2 = x.c2 };
        wrap_V2V tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl; c2 = x.c2; c3 = x.c3 typ = x.typ};
        wrap_V3 tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl; c2 = x.c2; c3 = x.c3 };
        wrap_VA tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl };
        wrap_VP tag x = ;

        wrap_VPSlash tag x = ;
        wrap_VQ tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl };
        wrap_VS tag x = { s = table { vf => wrap tag (x.s ! vf) }; p = x.p; isRefl = x.isRefl };
        wrap_VV tag x = ;
        wrap_Voc tag x = ;



    oper
        wrap : Tag -> Str -> Str = \t,s -> "<" ++ t.s ++ ">" ++ s ++ "</" ++ t.s ++ ">";
   
}