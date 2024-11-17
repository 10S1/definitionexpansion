concrete ParentheticalsIE_concr of ParentheticalsIE_abstr = GrammarEng ** open ParadigmsEng, SymbolicEng, ResEng, IrregEng, ExtraEng, ExtendEng in {	

    lin

        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html
        
        IE_A utter x = { 
            s = table { af => WRAP_IE utter (x.s ! af) }; 
            isPre = x.isPre; 
            isMost = x.isMost
        };

        IE_A2 utter x = { 
            s = table { af => WRAP_IE utter (x.s ! af) }; 
            isPre = x.isPre; 
            isMost = x.isMost; 
            c2 = x.c2
        };

        IE_ACard utter x = { 
            s = table { c => WRAP_IE utter (x.s ! c) }; 
            n = x.n 
        };

        IE_AP utter x = { 
            s = table { agr => WRAP_IE utter (x.s ! agr) }; 
            isPre = x.isPre 
        };

--        IE_AdA utter x = ;

--        IE_AdN utter x = ;

--        IE_AdV utter x = ;

        IE_Adv utter x = {
            s = WRAP_IE utter x.s
        };

--        IE_Ant utter x = ;

        IE_CAdv utter x = { 
            s = table { pol => WRAP_IE utter (x.s ! pol) }; 
            p = x.p 
        };

        IE_CN utter x = { 
            s = table { 
                num => table { 
                    c => WRAP_IE utter (x.s ! num ! c) 
                } 
            }; 
            g = x.g 
        };

        IE_Card utter x = { 
            s = table { b => table { c => WRAP_IE utter (x.s ! b ! c) } };
            sp = table { b => table { c => WRAP_IE utter (x.sp ! b ! c) } };
            n = x.n 
        };

        IE_Cl utter x = { 
            s = table { t => table { a => table { cp => table { o => WRAP_IE utter (x.s ! t ! a ! cp ! o) } } } } 
        };
                        
        IE_ClSlash utter x = { 
            s = table { t => table { a => table { cp => table { o => WRAP_IE utter (x.s ! t ! a ! cp ! o) } } } };
            c2 = x.c2 
        };

        IE_Comp utter x = { 
            s = table { agr => WRAP_IE utter (x.s ! agr) }
        };

        IE_Conj utter x = { 
            s1 = WRAP_IE utter x.s1;
            s2 = WRAP_IE utter x.s2;
            n = x.n 
        };

        IE_DAP utter x = { 
            s = WRAP_IE utter x.s;
            sp = table { g => table { b => table { c => WRAP_IE utter (x.sp ! g ! b ! c) } } };
            n = x.n;
            hasNum = x.hasNum
        };

        IE_Det utter x = { 
            s = WRAP_IE utter x.s;
            sp = table { g => table { b => table { c => WRAP_IE utter (x.sp ! g ! b ! c) } } };
            n = x.n;
            hasNum = x.hasNum
        };
                                
--        IE_Dig utter x = ;

        IE_Digits utter x = { 
            s = table { co => table { c => WRAP_IE utter (x.s ! co ! c) } };
            n = x.n;
            tail = x.tail
        };

--        IE_IAdv utter x = ;

        IE_IComp utter x = { 
            s = WRAP_IE utter x.s 
        };

        IE_IDet utter x = { 
            s = WRAP_IE utter x.s;
            n = x.n 
        };
                             
        IE_IP utter x = { 
            s = table { c => WRAP_IE utter (x.s ! c) };
            n = x.n 
        };

        IE_IQuant utter x = { 
            s = table { n => WRAP_IE utter (x.s ! n) }
        };

        IE_Imp utter x = { 
            s = table { cp => table { f => WRAP_IE utter (x.s ! cp ! f) } }
        };

--        -- IE_ImpForm utter x = ;
--        IE_Interj utter x = ;

--        IE_ListAP utter x = ;

--        IE_ListAdv utter x = ;

--        IE_ListNP utter x = ;

--        IE_ListRS utter x = ;

--        IE_ListS utter x = ;

        IE_N utter x = { 
            s = table { num => table { c => WRAP_IE utter (x.s ! num ! c) } }; 
            g = x.g 
        };

        IE_N2 utter x = { 
            s = table { n => table { c => WRAP_IE utter (x.s ! n ! c) } };
            g = x.g;
            c2 = x.c2
        };

        IE_N3 utter x = { 
            s = table { n => table { c => WRAP_IE utter (x.s ! n ! c) } };
            g = x.g;
            c2 = x.c2;
            c3 = x.c3
        };

        IE_NP utter x = { 
            s = table { c => WRAP_IE utter (x.s ! c) };
            a = x.a 
        };

        IE_Num utter x = { 
            s = table { b => table { c => WRAP_IE utter (x.s ! b ! c) } };
            sp = table { b => table { c => WRAP_IE utter (x.sp ! b ! c) } };
            n = x.n;
            hasCard = x.hasCard
        };

        IE_Numeral utter x = { 
            s = table { b => table { co => table { c => WRAP_IE utter (x.s ! b ! co ! c) } } };
            n = x.n 
        };

        IE_Ord utter x = { 
            s = table { c => WRAP_IE utter (x.s ! c) }
        };

--        IE_PConj utter x = ;

        IE_PN utter x = { 
            s = table { c => WRAP_IE utter (x.s ! c) };
            g = x.g 
        };

--        IE_Phr utter x = ;

        IE_Pol utter x = { 
            s = WRAP_IE utter x.s;
            p = x.p 
        };

        IE_Predet utter x = { 
            s = WRAP_IE utter x.s 
        };

        IE_Prep utter x = { 
            s = WRAP_IE utter x.s;
            isPre = x.isPre 
        };

        IE_Pron utter x = { 
            s = table { c => WRAP_IE utter (x.s ! c) };
            sp = table { c => WRAP_IE utter (x.sp ! c) };
            a = x.a 
        };

--        -- IE_Punct utter x = ;

        IE_QCl utter x = { 
            s = table { t => table { a => table { cp => table { qf => WRAP_IE utter (x.s ! t ! a ! cp ! qf) } } } }
        };

        IE_QS utter x = { 
            s = table { qf => WRAP_IE utter (x.s ! qf) }
        };

        IE_RCl utter x = { 
            s = table { t => table { a => table { cp => table { agr => WRAP_IE utter (x.s ! t ! a ! cp ! agr) } } } };
            c = x.c 
        };

        IE_RP utter x = { 
            s = table { rc => WRAP_IE utter (x.s ! rc) };
            a = x.a 
        };


        IE_RS utter x = { 
            s = table { agr => WRAP_IE utter (x.s ! agr) };
            c = x.c 
        };

        IE_S utter x = { 
            s = WRAP_IE utter x.s 
        };

--        IE_SC utter x = ;

        IE_SSlash utter x = { 
            s = WRAP_IE utter x.s;
            c2 = WRAP_IE utter x.c2
        };

--        IE_Sub100 utter x = ;

--        IE_Sub1000 utter x = ;

        IE_Subj utter x = { 
            s = WRAP_IE utter x.s 
        };

--        IE_Temp utter x = ;

--        IE_Tense utter x = ;

--        IE_Text utter x = ;

--        -- IE_Unit utter x = ;

        IE_Utt utter x = {
            s = WRAP_IE utter x.s
        };

        IE_V utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        IE_V2 utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        IE_V2A utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3 
        };

        IE_V2Q utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        IE_V2S utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        IE_V2V utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3; 
            typ = x.typ
        };

        IE_V3 utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3 
        };

        IE_VA utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

--        IE_VP utter x = lin VP { 
--            p = WRAP_IE utter x.p;
--            ad = table { agr => WRAP_IE utter (x.ad ! agr) };
--            s2 = table { agr => WRAP_IE utter (x.s2 ! agr) };
--            ext = WRAP_IE utter x.ext;
--            prp = WRAP_IE utter x.prp;
--            ptp = WRAP_IE utter x.ptp;
--            inf = WRAP_IE utter x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => WRAP_IE utter (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => WRAP_IE utter (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => WRAP_IE utter (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => WRAP_IE utter (x.nonAuxForms.pres ! agr) };
--                past = WRAP_IE utter x.nonAuxForms.past
--            }
--        };

--        IE_VPSlash utter x = lin VPSlash { 
--            p = WRAP_IE utter x.p;
--            ad = table { agr => WRAP_IE utter (x.ad ! agr) };
--            s2 = table { agr => WRAP_IE utter (x.s2 ! agr) };
--            ext = WRAP_IE utter x.ext;
--            prp = WRAP_IE utter x.prp;
--            ptp = WRAP_IE utter x.ptp;
--            inf = WRAP_IE utter x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => WRAP_IE utter (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => WRAP_IE utter (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => WRAP_IE utter (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => WRAP_IE utter (x.nonAuxForms.pres ! agr) };
--                past = WRAP_IE utter x.nonAuxForms.past
--            };
--            c2 = WRAP_IE utter x.c2;
--            gapInMiddle = x.gapInMiddle;
--            missingAdv = x.missingAdv
--        };

        IE_VQ utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        IE_VS utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        IE_VV utter x = { 
            s = table { vf => WRAP_IE utter (x.s ! vf) };
            p = WRAP_IE utter x.p;
            typ = x.typ 
        };

--        IE_Voc utter x = ;



    oper
        WRAP_IE : Utt -> Str -> Str = \u,s -> s ++ "(i.e." ++ u.s ++ ")";
   
}