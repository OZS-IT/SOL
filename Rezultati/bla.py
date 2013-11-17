with open("SOL3a.csv",'r+',encoding="utf-8") as f:
    with open("SOL3.csv",'r+',encoding="utf-8") as g:
        for i in f:
            for j in i:
                if j!="\"":
                    g.write(j)
        
