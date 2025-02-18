incomplete concrete CoreFunctor of Core = XmlConcr ** open Syntax, Grammar, Symbolic, AddedTags in {
    oper
        _Kind = {cn: CN; adv: Adv};   -- inspired by Aarne's new grammar
        _Ident = {s: Str};

        mergeAdv : Adv -> Adv -> Adv = \a,b -> lin Adv {s = a.s ++ b.s};

        empty_Adv : Adv = lin Adv {s = ""};
        mkKind = overload {
            mkKind : CN -> _Kind = \cn -> {cn = cn; adv = empty_Adv};
            mkKind : N -> _Kind = \n -> {cn = mkCN n; adv = empty_Adv};
        };

    lincat
        Stmt = S;
        PreKind = CN;
        Kind = _Kind;
        NamedKind = CN;
        Term = NP;
        Ident = _Ident;
        PreProperty = AP;
        Property = AP;
        ArgMarker = Prep;

    lin
        -- identifiers
        no_ident = {s = ""};
        math_ident m = {s = m.s};

        -- prekinds/kinds/named kinds
        plain_prekind pk = mkKind pk;
        wrapped_prekind tag pk = mkKind (WRAP_CN tag pk);
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

        -- terms
        existential_term nk = DetCN a_Det nk;
        math_term m = symb m.s;
        plural_term nk = DetCN aPl_Det nk;

        -- properties
        plain_preproperty pp = pp;
        wrapped_preproperty tag pp = WRAP_AP tag pp;
        property_with_arg p am t = AdvAP p (PrepNP am t);

        -- definitions
        define_nkind_as_nkind nk1 nk2 = mkS (mkCl (DetCN a_Det nk1) (DetCN a_Det nk2));

        -- statements
        formula_stmt m = lin S {s = m.s};
        exists_nkind nk = mkS (mkCl (DetCN a_Det nk));
        exists_nkind_pl nk = mkS (mkCl (DetCN aPl_Det nk));
}
