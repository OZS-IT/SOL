from urllib.request import urlopen

with open("Registracije/registracije9a.csv","r",encoding="utf-8") as f:
    with open("Registracije/registracije9a.csv","w",encoding="utf-8") as g:
        a = f.read()
        b = a.split("\n")
        ozs = urlopen("http://www.orientacijska-zveza.si/index.php?id=56")
        stran=str(ozs.read(),encoding="utf-8")
        s = ""
        tujci = ["Herwig Allwinger jr.", "Andraž De Luisa", "Vedran Bijelič",
                 "Manuel Jurado", "Marko Dudić", "Mariya Perepelytsya", "Matjaž Štanfel"]
        for i in b:
            stri=""
            c = i.split(";")
            k = 0
            if len(c)>1:
                naziv = " ".join(c[1:3])
                if not (naziv+"<sup>" in stran) or naziv in tujci:
                    while k < 5:
                        stri += c[k]+";"
                        k += 1
                    stri = stri[:-1] + "\n"
                    s += stri
        g.write(s[:-1])
