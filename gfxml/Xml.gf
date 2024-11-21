abstract Xml = {
    cat
        Tag;
        MathNode;
        Epsilon;  -- empty string

    fun
        epsilon : Epsilon;  -- empty string
        tag : Int -> Tag;
        wrap_math : Tag -> Epsilon -> MathNode;   -- signature is hard-coded in gfxml.py!
}
