concrete XmlConcr of Xml = {
    lincat
        Tag = {s: Str};
        MathNode = {s: Str};
        Epsilon = Str;

    lin
        epsilon = "";
        tag i = {s = i.s};
        wrap_math t e = {s = "<m" ++ t.s ++ ">" ++ e ++ "</m" ++ t.s ++ ">"};

    oper
        wrap : Tag -> Str -> Str = \t,s -> "<" ++ t.s ++ ">" ++ s ++ "</" ++ t.s ++ ">";
}
