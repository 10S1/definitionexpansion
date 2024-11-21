concrete TestEng of Test = XmlConcr ** {
    lincat
        S = Str;
        NP = Str;
        VP = Str;

    lin
        john = "John";
        mary = "Mary";
        run = "runs";
        formula_NP m = m.s;
        mkS np vp = np ++ vp;

        wrap_NP t np = wrap t np;
}
