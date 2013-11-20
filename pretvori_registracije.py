import re
with open("Registracije/registracije1a.csv","r",encoding="utf-8") as f:
    with open("Registracije/registracije1.csv","w",encoding="utf-8") as g:
        a = f.read()
        b = a.split("\n")
        s = ""
        for i in b:
            stri=""
            c = i.split(";")
            print(c)
            k = 0
            if len(c)>0:
                while k < 4:
                    stri += c[k]+";"
                    k += 1
                stri = stri[:-1] + "\n"
                s += stri
        g.write(s)
