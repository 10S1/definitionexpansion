concrete AddedTags_concr of AddedTags_abstr = {	

    lincat
        Tag = {s: Str};
        

    lin
        tag i = {s = i.s};
        
        wrap_NP t np = wrap t np;
        

    oper
        wrap : Tag -> Str -> Str = \t,s -> "<" ++ t.s ++ ">" ++ s ++ "</" ++ t.s ++ ">";
   
}