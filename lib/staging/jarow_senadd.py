def jarow(s1,s2):
    try:
        s1 = s1.upper()
        s2 = s2.upper()
        if s1==s2:
            return 1.0
        if s1=="" or s2=="":
            return 0.0
        short, long = len(s1)>len(s2) and [s2, s1] or [s1, s2]
        for l in range(0, min(5, len(short))):
          if short[l] != long[l]:
            break
        mtch = ""
        mtch2=[]
        dist = len(long)/2-1
        m = 0.0
        for i, x in enumerate(long):
          jx, jy = (lambda x,y: x==y and (x,y+1) or (x,y))(max(0, i-dist), min(len(short), i+dist))
          for j in range(jx, jy):
            if j<len(short) and x == short[j]:
              m+=1
              mtch+=x
              mtch2.extend([[j,x]])
              short=short[:j]+"*"+short[min(len(short), j+1):]
              break
        mtch2 = "".join(x[1] for x in sorted(mtch2))
        t = 0.0
        for i in range(0, len(mtch)):      
          if mtch[i]!=mtch2[i]:
            t += 0.5

        d = 0.1 
        # this is the jaro-distance 
        if m==0:
          d_j = 0
        else:
          d_j = 1/3.0 * ((m/len(short)) + (m/len(long)) + ((m - t)/m))
        return d_j + (l * d * (1 - d_j))
    except:
        print "Jaro-Winkler exception thrown on comparison between " + s1 + " and " + s2
        return 0
