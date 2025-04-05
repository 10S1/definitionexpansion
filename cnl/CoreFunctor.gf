incomplete concrete CoreFunctor of Core = XmlConcr ** open Syntax, Grammar, Symbolic, AddedTags, Extend in {
    oper
        _Kind = {cn: CN; adv: Adv};   -- inspired by Aarne's new grammar
        _Ident = {s: Str};

        mergeAdv : Adv -> Adv -> Adv = \a,b -> lin Adv {s = a.s ++ b.s};

        empty_Adv : Adv = lin Adv {s = ""};
        mkKind = overload {
            mkKind : CN -> _Kind = \cn -> {cn = cn; adv = empty_Adv};
            mkKind : N -> _Kind = \n -> {cn = mkCN n; adv = empty_Adv};
        };

        kind2CN : _Kind -> CN = \k -> mkCN k.cn k.adv;

    lincat
        Conj = Conj;
        Quantification = Det;
        Stmt = S;
        Polarity = Pol;
        Def = S;
        DefCore = S;
        Sentence = {s: Str};
        PreKind = CN;
        Kind = _Kind;
        NamedKind = CN;
        Term = NP;
        Ident = _Ident;
        Property = AP;
        ArgMarker = Prep;

    lin
        -- polarities
        positive_pol = positivePol;
        negative_pol = negativePol;

        -- conjunctions
        and_conj = and_Conj;
        or_conj = or_Conj;
        if_then_conj = if_then_Conj;

        -- identifiers
        no_ident = {s = ""};
        math_ident m = {s = m.s};

        -- prekinds/kinds/named kinds
        prekind_to_kind pk = mkKind pk;
        wrapped_prekind tag pk = WRAP_CN tag pk;
        name_kind k i = mkCN (mkCN k.cn (symb i.s)) k.adv;
        property_prekind pp pk = mkCN pp pk;
        kind_with_arg k am t = {
            cn = k.cn;
            adv = mergeAdv k.adv (PrepNP am t);
        };
        formula_named_kind m = lin CN {
            s = table { _ => table { _ => m.s } };
            g = Neutr
        };
        nkind_that_is_property nk pol pp = mkCN nk (mkRS pol (mkRCl IdRP pp));

        -- terms
        quantified_nkind q nk = DetCN q nk;
        math_term m = symb m.s;
        plural_term nk = DetCN aPl_Det nk;

        -- quantifications
        existential_quantification = a_Det;

        -- properties
        wrapped_property tag p = WRAP_AP tag p;
        property_with_arg p am t = AdvAP p (PrepNP am t);

        -- definitions
        define_nkind_as_nkind nk1 nk2 = mkS (mkCl (DetCN a_Det nk1) (DetCN a_Det nk2));

        plain_defcore dc = dc;
        defcore_iff_stmt dc s = mkS iff_conj dc s;
        defcore_iff_stmt_v1 dc s = mkS iff_conj_v1 dc s;
        defcore_if_stmt dc s = mkS if_conj dc s;

        -- statements
        wrapped_stmt tag s = lin S {s = wrap tag s.s};
        conj_stmt c s1 s2 = mkS c s1 s2;

        formula_stmt m = lin S {s = m.s};
        exists_nkind nk = mkS (mkCl (DetCN a_Det nk));
        exists_nkind_v1 nk = mkS (ExistsNP (DetCN a_Det nk));
        exists_nkind_pl nk = mkS (mkCl (DetCN aPl_Det nk));

        term_has_nkind_stmt t nk = mkS (mkCl t have_V2 (DetCN a_Det nk));
        term_is_property_stmt t p = mkS (mkCl t p);

        let_kind_stmt i nk = lin S { s = (ImpP3 (symb i.s) (mkVP nk)).s };

        -- sentences
        fin_stmt s = {s = {- CAPIT ++ -} s.s ++ "."};
        def_sentence d = {s = {- CAPIT ++ -} d.s ++ "."};
        wrapped_sentence tag sf = {s = wrap tag sf.s};
}
