def uniasc(x, form='NFKD', action='replace', debug=False):
    # unicode to ascii format
    if debug:
        print x
    return unicodedata.normalize(form, x).encode('ascii', action)


