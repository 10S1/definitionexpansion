concrete LexEng of Lex = CoreEng ** open MDictEng, ParadigmsEng, SyntaxEng, GrammarEng in {
    lin
        lex_argmark_by = mkPrep "by";

        lex_integer = mkCN dict_integer_N;

        lex_positive = mkAP dict_positive_A;
        lex_divisible = mkAP dict_divisible_A;
}
