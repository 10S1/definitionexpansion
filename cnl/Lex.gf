abstract Lex = open Core in {
    fun
        lex_argmark_by : ArgMarker;
        lex_argmark_of : ArgMarker;

        lex_integer : PreKind;
        lex_path : PreKind;
        lex_sequence : PreKind;
        lex_edge : PreKind;
        lex_node : PreKind;
        lex_state : PreKind;
        lex_pair : PreKind;

        lex_finite : Property;
        lex_positive : Property;
        lex_divisible : Property;
}
