def uniasc(x):
    if type(x)==types.IntType or type(x)==types.FloatType:
        return x
    else:
        x = x.upper()
        #Solves that {UMLAUT OVER (A)}
        x = re.sub(r"[{].*?[(].*?[)].*?[}]", lambda(x):re.findall("[(](.*?)[)]", x.group())[0], x)
        #remove international zips (eg. A-12358, A12358, 12358A)
        x = re.sub(r"\b[A-Z]{1,5}[-]{0,2}[0-9]+\b|\b[0-9]+?[-]{0,2}[A-Z]{1,5}\b", "", x)
        x = re.sub(r"\b[A-Z]{1,5} ?[-]{1,2} ?[0-9]+\b|\b[0-9]+? ?[-]{1,2} ?[A-Z]{1,5}\b", "", x)
        #remove all numbers
        x = re.sub(r"[0-9]", "", x)
        #remove TOWN OF, ALL OF, etc
        x = re.sub(r"\b[A-Z]+?[,]? +?[I]?OF ", "", x)
        #remove stuff in parathesis
        x = re.sub(r"[(].*?[)]", "", x)
        #remove basic period punctuation, replace with nothing
        x = re.sub(r"[.()`'#\"&]|[-]{2,}|[/][-]", "", x)
        #remove space(s) + punctuation
        x = re.sub(r" *?[,|-] *?", lambda(x):re.findall(r"[,|-]", x.group())[0], x)
        #remove duplicates
        x = re.sub(r"[ ,|-]{2,}", lambda(x):re.findall(r"[ ,|-]", x.group())[0], x)
        #remove leading [,|-]
        x = re.sub(r"^[,|-]", "", x)
        #remove trailing [,|-]
        x = (lambda(x):len(x)>len(re.sub(r"[,|-]", " ", x).strip()))(x) and x[:-1] or x
        #remove all unicode
        x = unicodedata.normalize('NFKD', unicode(x)).encode('ascii', 'ignore')
        return x
