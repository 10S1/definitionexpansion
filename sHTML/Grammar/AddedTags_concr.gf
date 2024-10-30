concrete AddedTags_concr of AddedTags_abstr = {	

    lincat
        Tag = {s: Str};
        

    lin
        tag i = {s = i.s};
        
        wrap_NP t np = wrap t np;
                
        wrap_A tag x = wrap tag x;
        
        wrap_A tag x = { s = table { af => "<" ++ t.s ++ ">" ++ x.s ! af ++ "</" ++ t.s ++ ">"}; isPre = x.isPre; isMost = x.isMost};

        N_sn_N n = { s = table { num => table { c => "\\sn {" ++ n.s ! num ! c ++ "}"} }; g = n.g};
        V_sn_V v = { s = table { vf => "\\sn {" ++ v.s ! vf ++ "}"}; p = v.p; isRefl = v.isRefl};


    oper
        wrap : Tag -> Str -> Str = \t,s -> "<" ++ t.s ++ ">" ++ s ++ "</" ++ t.s ++ ">";
   
}