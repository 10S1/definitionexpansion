abstract Test = Xml ** {
    cat
        S;
        NP;
        VP;

    fun
        john : NP;
        mary : NP;
        formula_NP : MathNode -> NP;
        run : VP;
        mkS : NP -> VP -> S;

        wrap_NP : Tag -> NP -> NP;
}
