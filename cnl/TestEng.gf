concrete TestEng of Test = open SyntaxEng, ParadigmsEng in {
    lincat
        MyCat = A;
        MyOtherCat = {s: Str};

    lin
        mycat = mkA "mycat";
        myFun mycat = {s = "mycat"};
}
