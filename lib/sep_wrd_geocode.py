## TODO: unit test

import re

def sep_wrd(word, seq):
    if seq==-1:
        return word
    else:
        p = re.compile(" *?[,|] *")
        ln = p.split(word)
        if len(ln)> seq:
            return ln[seq]
        else:
            return ""
