incomplete concrete CoreFunctor of Core = XmlConcr ** open Syntax, Grammar, Symbolic, AddedTags in {
    oper
        _Kind = {cn: CN; adv: Adv};   -- inspired by Aarne's new grammar
        _Ident = {s: Str};

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

        -- terms
        existential_term nk = DetCN a_Det nk;
        math_term m = symb m.s;

        -- properties
        plain_preproperty pp = pp;
        wrapped_preproperty tag pp = WRAP_AP tag pp;
        property_with_arg p am t = AdvAP p (PrepNP am t);

        -- statements
        formula_stmt m = lin S {s = m.s};
}
