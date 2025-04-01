abstract Core = Xml ** {
    cat
        Stmt;           -- "there is an odd integer"
        StmtFin;        -- "There is an odd integer ."
        -- distinction of Kind and PreKind reduces number of readings (properties can only be applied to PreKind, arguments only to Kind)
        PreKind;        -- "bijective function"
        Kind;           -- "bijective function ... from X to Y"
        NamedKind;      -- "bijective function f from X to Y"
        Term;           -- "every function f from X to Y"
        Ident;          -- "f"
        Property;       -- "divisible by 2"
        ArgMarker;      -- "by", "of degree", ...

    fun
        -- identifiers
        no_ident : Ident;
        math_ident : MathNode -> Ident;

        -- prekinds/kinds/named kinds
        prekind_to_kind : PreKind -> Kind;
        wrapped_prekind : Tag -> PreKind -> PreKind;
        name_kind : Kind -> Ident -> NamedKind;
        such_that_named_kind : NamedKind -> Stmt -> NamedKind;
        such_that_named_kind_v1 : NamedKind -> Stmt -> NamedKind;
        such_that_named_kind_v2 : NamedKind -> Stmt -> NamedKind;
        property_prekind : Property -> PreKind -> PreKind;
        kind_with_arg : Kind -> ArgMarker -> Term -> Kind;
        formula_named_kind : MathNode -> NamedKind;    -- as in "iff there is some n∈N such that ..."

        -- terms
        existential_term : NamedKind -> Term;
        existential_term_v1 : NamedKind -> Term;
        plural_term : NamedKind -> Term;
        math_term : MathNode -> Term;

        -- properties
        wrapped_property : Tag -> Property -> Property;
        property_with_arg : Property -> ArgMarker -> Term -> Property;

        -- statements
        iff_stmt : Stmt -> Stmt -> Stmt;
        formula_stmt : MathNode -> Stmt;
        stmt_for_term : Stmt -> Term -> Stmt;

        let_kind_stmt : Ident -> NamedKind -> Stmt;    -- in practice, NamedKind should be anonymous, but Kind is too restricted (e.g. no "such that")

        fin_stmt : Stmt -> StmtFin;
        wrapped_stmtfin : Tag -> StmtFin -> StmtFin;

        -- definitions
        define_nkind_as_nkind : NamedKind -> NamedKind -> Stmt;
        define_nkind_as_nkind_v1 : NamedKind -> NamedKind -> Stmt;
        define_term_prop : Term -> Property -> Stmt;     -- `t` is called `p`
        define_term_prop_v1 : Term -> Property -> Stmt;   -- `t` is said to be `p`
        define_term_prop_v2 : Term -> Property -> Stmt;   -- `t` is `p`
        exists_nkind : NamedKind -> Stmt;
        exists_nkind_pl : NamedKind -> Stmt;
}

