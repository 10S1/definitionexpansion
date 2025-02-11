abstract Lex = open Core in {
    fun
        lex_argmark_by : ArgMarker;

        lex_integer : PreKind;

        lex_positive : Property;
        lex_divisible : Property;
}
