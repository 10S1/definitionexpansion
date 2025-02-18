abstract Core = Xml ** {
    cat
        Stmt;           -- "there is an odd integer"
        PreKind;        -- "function"
        Kind;           -- "function ... from X to Y"
        NamedKind;      -- "function f from X to Y"
        Term;           -- "every function f from X to Y"
        Ident;          -- "f"
        PreProperty;    -- "divisible"
        Property;       -- "divisible by 2"
        ArgMarker;      -- "by", "of degree", ...

    fun
        -- identifiers
        no_ident : Ident;
        math_ident : MathNode -> Ident;

        -- prekinds/kinds/named kinds
        plain_prekind : PreKind -> Kind;
        wrapped_prekind : Tag -> PreKind -> Kind;
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
        plain_preproperty : PreProperty -> Property;
        wrapped_preproperty : Tag -> PreProperty -> Property;
        property_with_arg : Property -> ArgMarker -> Term -> Property;

        -- statements
        iff_stmt : Stmt -> Stmt -> Stmt;
        formula_stmt : MathNode -> Stmt;
        stmt_for_term : Stmt -> Term -> Stmt;

        -- definitions
        define_nkind_as_nkind : NamedKind -> NamedKind -> Stmt;
        define_nkind_as_nkind_v1 : NamedKind -> NamedKind -> Stmt;
        define_term_prop : Term -> Property -> Stmt;     -- `t` is called `p`
        define_term_prop_v1 : Term -> Property -> Stmt;   -- `t` is said to be `p`
        define_term_prop_v2 : Term -> Property -> Stmt;   -- `t` is `p`
        exists_nkind : NamedKind -> Stmt;
        exists_nkind_pl : NamedKind -> Stmt;
}

