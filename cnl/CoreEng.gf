concrete CoreEng of Core =
    CoreFunctor with 
        (Syntax=SyntaxEng), (Grammar=GrammarEng), (Symbolic=SymbolicEng),
        (AddedTags=AddedTagsEng)
** open ParadigmsEng, ResEng, Prelude, StructuralEng in {
    oper
        _call_V2 : V2 = mkV2 (mkV "call");
        _say_V2 : V2 = mkV2 (mkV "say" "said" "said");
        _iff: Conj = mkConj "iff";

        -- mergeAdv a b = lin Adv {s = a.s ++ b.s};

        term_to_adv : NP -> Adv = PrepNP (mkPrep "");
        str_adv : Str -> Adv = \s -> lin Adv {s = s};
        property_to_adv : AP -> Adv = \p -> lin Adv {s = p.s ! AgP3Sg Neutr};

    lin
        iff_stmt s1 s2 = mkS _iff s1 s2;

        such_that_named_kind nk s = mkCN nk (lin Adv {s = "such that" ++ s.s});
        such_that_named_kind_v1 nk s = mkCN nk (lin Adv {s = "where" ++ s.s});
        such_that_named_kind_v2 nk s = mkCN nk (lin Adv {s = "with" ++ s.s});

        existential_term_v1 nk = DetCN someSg_Det nk;

        stmt_for_term stmt term = lin S {s = stmt.s ++ (PrepNP (mkPrep "for") term).s};

        define_nkind_as_nkind_v1 nk1 nk2 = mkS (mkCl (DetCN a_Det nk2) (mkVP (passiveVP _call_V2) (term_to_adv (DetCN a_Det nk2))));

        define_term_prop t p = mkS (mkCl t (mkVP (passiveVP _call_V2) (property_to_adv p)));
        define_term_prop_v1 t p = mkS (mkCl t (mkVP (passiveVP _say_V2) (str_adv (infVP VVInf (mkVP p) False Simul CPos (agrP3 Sg)))));
        define_term_prop_v2 t p = mkS (mkCl t p);
}
