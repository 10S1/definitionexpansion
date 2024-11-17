concrete ParentheticalsParentheses_concr of ParentheticalsParentheses_abstr = GrammarEng ** open ParadigmsEng, SymbolicEng, ResEng, IrregEng, ExtraEng, ExtendEng in {	

    lin

        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html
        
        PARENTHESES_A utter x = { 
            s = table { af => WRAP_PARENTHESES utter (x.s ! af) }; 
            isPre = x.isPre; 
            isMost = x.isMost
        };

        PARENTHESES_A2 utter x = { 
            s = table { af => WRAP_PARENTHESES utter (x.s ! af) }; 
            isPre = x.isPre; 
            isMost = x.isMost; 
            c2 = x.c2
        };

        PARENTHESES_ACard utter x = { 
            s = table { c => WRAP_PARENTHESES utter (x.s ! c) }; 
            n = x.n 
        };

        PARENTHESES_AP utter x = { 
            s = table { agr => WRAP_PARENTHESES utter (x.s ! agr) }; 
            isPre = x.isPre 
        };

--        PARENTHESES_AdA utter x = ;

--        PARENTHESES_AdN utter x = ;

--        PARENTHESES_AdV utter x = ;

        PARENTHESES_Adv utter x = {
            s = WRAP_PARENTHESES utter x.s
        };

--        PARENTHESES_Ant utter x = ;

        PARENTHESES_CAdv utter x = { 
            s = table { pol => WRAP_PARENTHESES utter (x.s ! pol) }; 
            p = x.p 
        };

        PARENTHESES_CN utter x = { 
            s = table { 
                num => table { 
                    c => WRAP_PARENTHESES utter (x.s ! num ! c) 
                } 
            }; 
            g = x.g 
        };

        PARENTHESES_Card utter x = { 
            s = table { b => table { c => WRAP_PARENTHESES utter (x.s ! b ! c) } };
            sp = table { b => table { c => WRAP_PARENTHESES utter (x.sp ! b ! c) } };
            n = x.n 
        };

        PARENTHESES_Cl utter x = { 
            s = table { t => table { a => table { cp => table { o => WRAP_PARENTHESES utter (x.s ! t ! a ! cp ! o) } } } } 
        };
                        
        PARENTHESES_ClSlash utter x = { 
            s = table { t => table { a => table { cp => table { o => WRAP_PARENTHESES utter (x.s ! t ! a ! cp ! o) } } } };
            c2 = x.c2 
        };

        PARENTHESES_Comp utter x = { 
            s = table { agr => WRAP_PARENTHESES utter (x.s ! agr) }
        };

        PARENTHESES_Conj utter x = { 
            s1 = WRAP_PARENTHESES utter x.s1;
            s2 = WRAP_PARENTHESES utter x.s2;
            n = x.n 
        };

        PARENTHESES_DAP utter x = { 
            s = WRAP_PARENTHESES utter x.s;
            sp = table { g => table { b => table { c => WRAP_PARENTHESES utter (x.sp ! g ! b ! c) } } };
            n = x.n;
            hasNum = x.hasNum
        };

        PARENTHESES_Det utter x = { 
            s = WRAP_PARENTHESES utter x.s;
            sp = table { g => table { b => table { c => WRAP_PARENTHESES utter (x.sp ! g ! b ! c) } } };
            n = x.n;
            hasNum = x.hasNum
        };
                                
--        PARENTHESES_Dig utter x = ;

        PARENTHESES_Digits utter x = { 
            s = table { co => table { c => WRAP_PARENTHESES utter (x.s ! co ! c) } };
            n = x.n;
            tail = x.tail
        };

--        PARENTHESES_IAdv utter x = ;

        PARENTHESES_IComp utter x = { 
            s = WRAP_PARENTHESES utter x.s 
        };

        PARENTHESES_IDet utter x = { 
            s = WRAP_PARENTHESES utter x.s;
            n = x.n 
        };
                             
        PARENTHESES_IP utter x = { 
            s = table { c => WRAP_PARENTHESES utter (x.s ! c) };
            n = x.n 
        };

        PARENTHESES_IQuant utter x = { 
            s = table { n => WRAP_PARENTHESES utter (x.s ! n) }
        };

        PARENTHESES_Imp utter x = { 
            s = table { cp => table { f => WRAP_PARENTHESES utter (x.s ! cp ! f) } }
        };

--        -- PARENTHESES_ImpForm utter x = ;
--        PARENTHESES_Interj utter x = ;

--        PARENTHESES_ListAP utter x = ;

--        PARENTHESES_ListAdv utter x = ;

--        PARENTHESES_ListNP utter x = ;

--        PARENTHESES_ListRS utter x = ;

--        PARENTHESES_ListS utter x = ;

        PARENTHESES_N utter x = { 
            s = table { num => table { c => WRAP_PARENTHESES utter (x.s ! num ! c) } }; 
            g = x.g 
        };

        PARENTHESES_N2 utter x = { 
            s = table { n => table { c => WRAP_PARENTHESES utter (x.s ! n ! c) } };
            g = x.g;
            c2 = x.c2
        };

        PARENTHESES_N3 utter x = { 
            s = table { n => table { c => WRAP_PARENTHESES utter (x.s ! n ! c) } };
            g = x.g;
            c2 = x.c2;
            c3 = x.c3
        };

        PARENTHESES_NP utter x = { 
            s = table { c => WRAP_PARENTHESES utter (x.s ! c) };
            a = x.a 
        };

        PARENTHESES_Num utter x = { 
            s = table { b => table { c => WRAP_PARENTHESES utter (x.s ! b ! c) } };
            sp = table { b => table { c => WRAP_PARENTHESES utter (x.sp ! b ! c) } };
            n = x.n;
            hasCard = x.hasCard
        };

        PARENTHESES_Numeral utter x = { 
            s = table { b => table { co => table { c => WRAP_PARENTHESES utter (x.s ! b ! co ! c) } } };
            n = x.n 
        };

        PARENTHESES_Ord utter x = { 
            s = table { c => WRAP_PARENTHESES utter (x.s ! c) }
        };

--        PARENTHESES_PConj utter x = ;

        PARENTHESES_PN utter x = { 
            s = table { c => WRAP_PARENTHESES utter (x.s ! c) };
            g = x.g 
        };

--        PARENTHESES_Phr utter x = ;

        PARENTHESES_Pol utter x = { 
            s = WRAP_PARENTHESES utter x.s;
            p = x.p 
        };

        PARENTHESES_Predet utter x = { 
            s = WRAP_PARENTHESES utter x.s 
        };

        PARENTHESES_Prep utter x = { 
            s = WRAP_PARENTHESES utter x.s;
            isPre = x.isPre 
        };

        PARENTHESES_Pron utter x = { 
            s = table { c => WRAP_PARENTHESES utter (x.s ! c) };
            sp = table { c => WRAP_PARENTHESES utter (x.sp ! c) };
            a = x.a 
        };

--        -- PARENTHESES_Punct utter x = ;

        PARENTHESES_QCl utter x = { 
            s = table { t => table { a => table { cp => table { qf => WRAP_PARENTHESES utter (x.s ! t ! a ! cp ! qf) } } } }
        };

        PARENTHESES_QS utter x = { 
            s = table { qf => WRAP_PARENTHESES utter (x.s ! qf) }
        };

        PARENTHESES_RCl utter x = { 
            s = table { t => table { a => table { cp => table { agr => WRAP_PARENTHESES utter (x.s ! t ! a ! cp ! agr) } } } };
            c = x.c 
        };

        PARENTHESES_RP utter x = { 
            s = table { rc => WRAP_PARENTHESES utter (x.s ! rc) };
            a = x.a 
        };


        PARENTHESES_RS utter x = { 
            s = table { agr => WRAP_PARENTHESES utter (x.s ! agr) };
            c = x.c 
        };

        PARENTHESES_S utter x = { 
            s = WRAP_PARENTHESES utter x.s 
        };

--        PARENTHESES_SC utter x = ;

        PARENTHESES_SSlash utter x = { 
            s = WRAP_PARENTHESES utter x.s;
            c2 = WRAP_PARENTHESES utter x.c2
        };

--        PARENTHESES_Sub100 utter x = ;

--        PARENTHESES_Sub1000 utter x = ;

        PARENTHESES_Subj utter x = { 
            s = WRAP_PARENTHESES utter x.s 
        };

--        PARENTHESES_Temp utter x = ;

--        PARENTHESES_Tense utter x = ;

--        PARENTHESES_Text utter x = ;

--        -- PARENTHESES_Unit utter x = ;

        PARENTHESES_Utt utter x = {
            s = WRAP_PARENTHESES utter x.s
        };

        PARENTHESES_V utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        PARENTHESES_V2 utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        PARENTHESES_V2A utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3 
        };

        PARENTHESES_V2Q utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        PARENTHESES_V2S utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        PARENTHESES_V2V utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3; 
            typ = x.typ
        };

        PARENTHESES_V3 utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3 
        };

        PARENTHESES_VA utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

--        PARENTHESES_VP utter x = lin VP { 
--            p = WRAP_PARENTHESES utter x.p;
--            ad = table { agr => WRAP_PARENTHESES utter (x.ad ! agr) };
--            s2 = table { agr => WRAP_PARENTHESES utter (x.s2 ! agr) };
--            ext = WRAP_PARENTHESES utter x.ext;
--            prp = WRAP_PARENTHESES utter x.prp;
--            ptp = WRAP_PARENTHESES utter x.ptp;
--            inf = WRAP_PARENTHESES utter x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => WRAP_PARENTHESES utter (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => WRAP_PARENTHESES utter (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => WRAP_PARENTHESES utter (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => WRAP_PARENTHESES utter (x.nonAuxForms.pres ! agr) };
--                past = WRAP_PARENTHESES utter x.nonAuxForms.past
--            }
--        };

--        PARENTHESES_VPSlash utter x = lin VPSlash { 
--            p = WRAP_PARENTHESES utter x.p;
--            ad = table { agr => WRAP_PARENTHESES utter (x.ad ! agr) };
--            s2 = table { agr => WRAP_PARENTHESES utter (x.s2 ! agr) };
--            ext = WRAP_PARENTHESES utter x.ext;
--            prp = WRAP_PARENTHESES utter x.prp;
--            ptp = WRAP_PARENTHESES utter x.ptp;
--            inf = WRAP_PARENTHESES utter x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => WRAP_PARENTHESES utter (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => WRAP_PARENTHESES utter (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => WRAP_PARENTHESES utter (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => WRAP_PARENTHESES utter (x.nonAuxForms.pres ! agr) };
--                past = WRAP_PARENTHESES utter x.nonAuxForms.past
--            };
--            c2 = WRAP_PARENTHESES utter x.c2;
--            gapInMiddle = x.gapInMiddle;
--            missingAdv = x.missingAdv
--        };

        PARENTHESES_VQ utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        PARENTHESES_VS utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        PARENTHESES_VV utter x = { 
            s = table { vf => WRAP_PARENTHESES utter (x.s ! vf) };
            p = WRAP_PARENTHESES utter x.p;
            typ = x.typ 
        };

--        PARENTHESES_Voc utter x = ;



    oper
        WRAP_PARENTHESES : Utt -> Str -> Str = \u,s -> s ++ "(" ++ u.s ++ ")";
   
}