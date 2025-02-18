concrete LexEng of Lex = CoreEng ** open MDictEng, ParadigmsEng, SyntaxEng, GrammarEng in {
    lin
        lex_argmark_by = mkPrep "by";
        lex_argmark_of = mkPrep "of";

        lex_integer = mkCN dict_integer_N;
        lex_path = mkCN dict_path_N;
        lex_sequence = mkCN dict_sequence_N;
        lex_edge = mkCN dict_edge_N;
        lex_node = mkCN dict_node_N;
        lex_state = mkCN dict_state_N;
        lex_pair = mkCN dict_pair_N;

        lex_finite = mkAP dict_finite_A;
        lex_positive = mkAP dict_positive_A;
        lex_divisible = mkAP dict_divisible_A;
}
