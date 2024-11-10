concrete PlaceholderCat_concr of PlaceholderCat_abstr = GrammarEng, MathTermsEng, MorphoDictEng, AddedTags_concr, AddedStructures_concr, AddedWords_concr ** open ParadigmsEng, SymbolicEng, ResEng, IrregEng, ExtraEng, ExtendEng in {
    lincat
        PlaceholderCat = Str;

	lin
        -- Own categories

        PlaceholderCat_Tag x = x.s;



        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html
        
        PlaceholderCat_A x = table { af => (x.s ! af) };

        PlaceholderCat_A2 x = table { af => (x.s ! af) }; 

        PlaceholderCat_ACard x = table { c => (x.s ! c) }; 

        PlaceholderCat_AP x = table { agr => (x.s ! agr) }; 

--        PlaceholderCat_AdA x = ;

--        PlaceholderCat_AdN x = ;

--        PlaceholderCat_AdV x = ;

        PlaceholderCat_Adv x = x.s;

--        PlaceholderCat_Ant x = ;

        PlaceholderCat_CAdv x = table { pol => (x.s ! pol) }; 

        PlaceholderCat_CN x = table { num => table { c => (x.s ! num ! c) } }; 

        PlaceholderCat_Card x = table { b => table { c => (x.s ! b ! c) } };

        PlaceholderCat_Cl x = table { t => table { a => table { cp => table { o => (x.s ! t ! a ! cp ! o) } } } };
                        
        PlaceholderCat_ClSlash x = table { t => table { a => table { cp => table { o => (x.s ! t ! a ! cp ! o) } } } };

        PlaceholderCat_Comp x = table { agr => (x.s ! agr) };

--        PlaceholderCat_Conj x = { 
--            s1 = x.s1;
--            s2 = x.s2;
--            n = x.n 
--        };

        PlaceholderCat_DAP x = x.s;

        PlaceholderCat_Det x = x.s;
                                
--        PlaceholderCat_Dig x = ;

        PlaceholderCat_Digits x = table { co => table { c => (x.s ! co ! c) } };

--        PlaceholderCat_IAdv x = ;

        PlaceholderCat_IComp x = x.s;

        PlaceholderCat_IDet x = x.s;
                             
        PlaceholderCat_IP x = table { c => (x.s ! c) };

        PlaceholderCat_IQuant x = table { n => (x.s ! n) };

        PlaceholderCat_Imp x = table { cp => table { f => (x.s ! cp ! f) } };

--        -- PlaceholderCat_ImpForm x = ;

--        PlaceholderCat_Interj x = ;

--        PlaceholderCat_ListAP x = ;

--        PlaceholderCat_ListAdv x = ;

--        PlaceholderCat_ListNP x = ;

--        PlaceholderCat_ListRS x = ;

--        PlaceholderCat_ListS x = ;

        PlaceholderCat_N x = table { num => table { c => (x.s ! num ! c) } }; 

        PlaceholderCat_N2 x = table { n => table { c => (x.s ! n ! c) } };

        PlaceholderCat_N3 x = table { n => table { c => (x.s ! n ! c) } };

        PlaceholderCat_NP x = table { c => (x.s ! c) };

        PlaceholderCat_Num x = table { b => table { c => (x.s ! b ! c) } };

        PlaceholderCat_Numeral x = table { b => table { co => table { c => (x.s ! b ! co ! c) } } };

        PlaceholderCat_Ord x = table { c => (x.s ! c) };

--        PlaceholderCat_PConj x = ;

        PlaceholderCat_PN x = table { c => (x.s ! c) };

--        PlaceholderCat_Phr x = ;

        PlaceholderCat_Pol x = x.s;

        PlaceholderCat_Predet x = x.s;

        PlaceholderCat_Prep x = x.s;

        PlaceholderCat_Pron x = table { c => (x.s ! c) };

--        -- PlaceholderCat_Punct x = ;

        PlaceholderCat_QCl x = table { t => table { a => table { cp => table { qf => (x.s ! t ! a ! cp ! qf) } } } };

        PlaceholderCat_QS x = table { qf => (x.s ! qf) };

        PlaceholderCat_RCl x = table { t => table { a => table { cp => table { agr => (x.s ! t ! a ! cp ! agr) } } } };

        PlaceholderCat_RP x = table { rc => (x.s ! rc) };

        PlaceholderCat_RS x = table { agr => (x.s ! agr) };

        PlaceholderCat_S x = x.s;

--        PlaceholderCat_SC x = ;

        PlaceholderCat_SSlash x = x.s;

--        PlaceholderCat_Sub100 x = ;

--        PlaceholderCat_Sub1000 x = ;

        PlaceholderCat_Subj x = x.s;

--        PlaceholderCat_Temp x = ;

--        PlaceholderCat_Tense x = ;

--        PlaceholderCat_Text x = ;

--        -- PlaceholderCat_Unit x = ;

        PlaceholderCat_Utt x = x.s;

        PlaceholderCat_V x = table { vf => (x.s ! vf) }; 

        PlaceholderCat_V2 x = table { vf => (x.s ! vf) };

        PlaceholderCat_V2A x = table { vf => (x.s ! vf) };

        PlaceholderCat_V2Q x = table { vf => (x.s ! vf) }; 

        PlaceholderCat_V2S x = table { vf => (x.s ! vf) };

        PlaceholderCat_V2V x = table { vf => (x.s ! vf) }; 

        PlaceholderCat_V3 x = table { vf => (x.s ! vf) }; 

        PlaceholderCat_VA x = table { vf => (x.s ! vf) }; 

--        PlaceholderCat_VP x = lin VP { 
--            p = x.p;
--            ad = table { agr => (x.ad ! agr) };
--            s2 = table { agr => (x.s2 ! agr) };
--            ext = x.ext;
--            prp = x.prp;
--            ptp = x.ptp;
--            inf = x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => (x.nonAuxForms.pres ! agr) };
--                past = x.nonAuxForms.past
--            }
--        };

--        PlaceholderCat_VPSlash x = lin VPSlash { 
--            p = x.p;
--            ad = table { agr => (x.ad ! agr) };
--            s2 = table { agr => (x.s2 ! agr) };
--            ext = x.ext;
--            prp = x.prp;
--            ptp = x.ptp;
--            inf = x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => (x.nonAuxForms.pres ! agr) };
--                past = x.nonAuxForms.past
--            };
--            c2 = x.c2;
--            gapInMiddle = x.gapInMiddle;
--            missingAdv = x.missingAdv
--        };

        PlaceholderCat_VQ x = table { vf => (x.s ! vf) };

        PlaceholderCat_VS x = table { vf => (x.s ! vf) };

        PlaceholderCat_VV x = table { vf => (x.s ! vf) };

--        PlaceholderCat_Voc x = ;
}