concrete ParentheticalsEmDashes_concr of ParentheticalsEmDashes_abstr = GrammarEng ** open ParadigmsEng, SymbolicEng, ResEng, IrregEng, ExtraEng, ExtendEng in {	

    lin

        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html
        
        EMDASHES_A utter x = { 
            s = table { af => WRAP_EMDASHES utter (x.s ! af) }; 
            isPre = x.isPre; 
            isMost = x.isMost
        };

        EMDASHES_A2 utter x = { 
            s = table { af => WRAP_EMDASHES utter (x.s ! af) }; 
            isPre = x.isPre; 
            isMost = x.isMost; 
            c2 = x.c2
        };

        EMDASHES_ACard utter x = { 
            s = table { c => WRAP_EMDASHES utter (x.s ! c) }; 
            n = x.n 
        };

        EMDASHES_AP utter x = { 
            s = table { agr => WRAP_EMDASHES utter (x.s ! agr) }; 
            isPre = x.isPre 
        };

--        EMDASHES_AdA utter x = ;

--        EMDASHES_AdN utter x = ;

--        EMDASHES_AdV utter x = ;

        EMDASHES_Adv utter x = {
            s = WRAP_EMDASHES utter x.s
        };

--        EMDASHES_Ant utter x = ;

        EMDASHES_CAdv utter x = { 
            s = table { pol => WRAP_EMDASHES utter (x.s ! pol) }; 
            p = x.p 
        };

        EMDASHES_CN utter x = { 
            s = table { 
                num => table { 
                    c => WRAP_EMDASHES utter (x.s ! num ! c) 
                } 
            }; 
            g = x.g 
        };

        EMDASHES_Card utter x = { 
            s = table { b => table { c => WRAP_EMDASHES utter (x.s ! b ! c) } };
            sp = table { b => table { c => WRAP_EMDASHES utter (x.sp ! b ! c) } };
            n = x.n 
        };

        EMDASHES_Cl utter x = { 
            s = table { t => table { a => table { cp => table { o => WRAP_EMDASHES utter (x.s ! t ! a ! cp ! o) } } } } 
        };
                        
        EMDASHES_ClSlash utter x = { 
            s = table { t => table { a => table { cp => table { o => WRAP_EMDASHES utter (x.s ! t ! a ! cp ! o) } } } };
            c2 = x.c2 
        };

        EMDASHES_Comp utter x = { 
            s = table { agr => WRAP_EMDASHES utter (x.s ! agr) }
        };

        EMDASHES_Conj utter x = { 
            s1 = WRAP_EMDASHES utter x.s1;
            s2 = WRAP_EMDASHES utter x.s2;
            n = x.n 
        };

        EMDASHES_DAP utter x = { 
            s = WRAP_EMDASHES utter x.s;
            sp = table { g => table { b => table { c => WRAP_EMDASHES utter (x.sp ! g ! b ! c) } } };
            n = x.n;
            hasNum = x.hasNum
        };

        EMDASHES_Det utter x = { 
            s = WRAP_EMDASHES utter x.s;
            sp = table { g => table { b => table { c => WRAP_EMDASHES utter (x.sp ! g ! b ! c) } } };
            n = x.n;
            hasNum = x.hasNum
        };
                                
--        EMDASHES_Dig utter x = ;

        EMDASHES_Digits utter x = { 
            s = table { co => table { c => WRAP_EMDASHES utter (x.s ! co ! c) } };
            n = x.n;
            tail = x.tail
        };

--        EMDASHES_IAdv utter x = ;

        EMDASHES_IComp utter x = { 
            s = WRAP_EMDASHES utter x.s 
        };

        EMDASHES_IDet utter x = { 
            s = WRAP_EMDASHES utter x.s;
            n = x.n 
        };
                             
        EMDASHES_IP utter x = { 
            s = table { c => WRAP_EMDASHES utter (x.s ! c) };
            n = x.n 
        };

        EMDASHES_IQuant utter x = { 
            s = table { n => WRAP_EMDASHES utter (x.s ! n) }
        };

        EMDASHES_Imp utter x = { 
            s = table { cp => table { f => WRAP_EMDASHES utter (x.s ! cp ! f) } }
        };

--        -- EMDASHES_ImpForm utter x = ;
--        EMDASHES_Interj utter x = ;

--        EMDASHES_ListAP utter x = ;

--        EMDASHES_ListAdv utter x = ;

--        EMDASHES_ListNP utter x = ;

--        EMDASHES_ListRS utter x = ;

--        EMDASHES_ListS utter x = ;

        EMDASHES_N utter x = { 
            s = table { num => table { c => WRAP_EMDASHES utter (x.s ! num ! c) } }; 
            g = x.g 
        };

        EMDASHES_N2 utter x = { 
            s = table { n => table { c => WRAP_EMDASHES utter (x.s ! n ! c) } };
            g = x.g;
            c2 = x.c2
        };

        EMDASHES_N3 utter x = { 
            s = table { n => table { c => WRAP_EMDASHES utter (x.s ! n ! c) } };
            g = x.g;
            c2 = x.c2;
            c3 = x.c3
        };

        EMDASHES_NP utter x = { 
            s = table { c => WRAP_EMDASHES utter (x.s ! c) };
            a = x.a 
        };

        EMDASHES_Num utter x = { 
            s = table { b => table { c => WRAP_EMDASHES utter (x.s ! b ! c) } };
            sp = table { b => table { c => WRAP_EMDASHES utter (x.sp ! b ! c) } };
            n = x.n;
            hasCard = x.hasCard
        };

        EMDASHES_Numeral utter x = { 
            s = table { b => table { co => table { c => WRAP_EMDASHES utter (x.s ! b ! co ! c) } } };
            n = x.n 
        };

        EMDASHES_Ord utter x = { 
            s = table { c => WRAP_EMDASHES utter (x.s ! c) }
        };

--        EMDASHES_PConj utter x = ;

        EMDASHES_PN utter x = { 
            s = table { c => WRAP_EMDASHES utter (x.s ! c) };
            g = x.g 
        };

--        EMDASHES_Phr utter x = ;

        EMDASHES_Pol utter x = { 
            s = WRAP_EMDASHES utter x.s;
            p = x.p 
        };

        EMDASHES_Predet utter x = { 
            s = WRAP_EMDASHES utter x.s 
        };

        EMDASHES_Prep utter x = { 
            s = WRAP_EMDASHES utter x.s;
            isPre = x.isPre 
        };

        EMDASHES_Pron utter x = { 
            s = table { c => WRAP_EMDASHES utter (x.s ! c) };
            sp = table { c => WRAP_EMDASHES utter (x.sp ! c) };
            a = x.a 
        };

--        -- EMDASHES_Punct utter x = ;

        EMDASHES_QCl utter x = { 
            s = table { t => table { a => table { cp => table { qf => WRAP_EMDASHES utter (x.s ! t ! a ! cp ! qf) } } } }
        };

        EMDASHES_QS utter x = { 
            s = table { qf => WRAP_EMDASHES utter (x.s ! qf) }
        };

        EMDASHES_RCl utter x = { 
            s = table { t => table { a => table { cp => table { agr => WRAP_EMDASHES utter (x.s ! t ! a ! cp ! agr) } } } };
            c = x.c 
        };

        EMDASHES_RP utter x = { 
            s = table { rc => WRAP_EMDASHES utter (x.s ! rc) };
            a = x.a 
        };


        EMDASHES_RS utter x = { 
            s = table { agr => WRAP_EMDASHES utter (x.s ! agr) };
            c = x.c 
        };

        EMDASHES_S utter x = { 
            s = WRAP_EMDASHES utter x.s 
        };

--        EMDASHES_SC utter x = ;

        EMDASHES_SSlash utter x = { 
            s = WRAP_EMDASHES utter x.s;
            c2 = WRAP_EMDASHES utter x.c2
        };

--        EMDASHES_Sub100 utter x = ;

--        EMDASHES_Sub1000 utter x = ;

        EMDASHES_Subj utter x = { 
            s = WRAP_EMDASHES utter x.s 
        };

--        EMDASHES_Temp utter x = ;

--        EMDASHES_Tense utter x = ;

--        EMDASHES_Text utter x = ;

--        -- EMDASHES_Unit utter x = ;

        EMDASHES_Utt utter x = {
            s = WRAP_EMDASHES utter x.s
        };

        EMDASHES_V utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        EMDASHES_V2 utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        EMDASHES_V2A utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3 
        };

        EMDASHES_V2Q utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        EMDASHES_V2S utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        EMDASHES_V2V utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3; 
            typ = x.typ
        };

        EMDASHES_V3 utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3 
        };

        EMDASHES_VA utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

--        EMDASHES_VP utter x = lin VP { 
--            p = WRAP_EMDASHES utter x.p;
--            ad = table { agr => WRAP_EMDASHES utter (x.ad ! agr) };
--            s2 = table { agr => WRAP_EMDASHES utter (x.s2 ! agr) };
--            ext = WRAP_EMDASHES utter x.ext;
--            prp = WRAP_EMDASHES utter x.prp;
--            ptp = WRAP_EMDASHES utter x.ptp;
--            inf = WRAP_EMDASHES utter x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => WRAP_EMDASHES utter (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => WRAP_EMDASHES utter (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => WRAP_EMDASHES utter (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => WRAP_EMDASHES utter (x.nonAuxForms.pres ! agr) };
--                past = WRAP_EMDASHES utter x.nonAuxForms.past
--            }
--        };

--        EMDASHES_VPSlash utter x = lin VPSlash { 
--            p = WRAP_EMDASHES utter x.p;
--            ad = table { agr => WRAP_EMDASHES utter (x.ad ! agr) };
--            s2 = table { agr => WRAP_EMDASHES utter (x.s2 ! agr) };
--            ext = WRAP_EMDASHES utter x.ext;
--            prp = WRAP_EMDASHES utter x.prp;
--            ptp = WRAP_EMDASHES utter x.ptp;
--            inf = WRAP_EMDASHES utter x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => WRAP_EMDASHES utter (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => WRAP_EMDASHES utter (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => WRAP_EMDASHES utter (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => WRAP_EMDASHES utter (x.nonAuxForms.pres ! agr) };
--                past = WRAP_EMDASHES utter x.nonAuxForms.past
--            };
--            c2 = WRAP_EMDASHES utter x.c2;
--            gapInMiddle = x.gapInMiddle;
--            missingAdv = x.missingAdv
--        };

        EMDASHES_VQ utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        EMDASHES_VS utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        EMDASHES_VV utter x = { 
            s = table { vf => WRAP_EMDASHES utter (x.s ! vf) };
            p = WRAP_EMDASHES utter x.p;
            typ = x.typ 
        };

--        EMDASHES_Voc utter x = ;



    oper
        WRAP_EMDASHES : Utt -> Str -> Str = \u,s -> s ++ "—" ++ u.s ++ "—";
   
}