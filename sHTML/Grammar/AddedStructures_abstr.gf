abstract AddedStructures_abstr = Grammar ** {
	
    cat

	data
        
        letUs_Utt : Utt -> S;

        let_np_be_np_S : NP -> NP -> S;

        np_is_called_np : NP -> NP -> S;

        np_is_called_ap : NP -> AP -> S;

        S_assume_S : S -> S;

        -- definiendum
        mt_to_np : MT -> NP;
        VtoV2 : V -> V2;
}