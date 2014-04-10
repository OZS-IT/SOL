"""Navodila:
  -  Izberi primerno vhodno in izhodno datoteko in pot do njiju vpiši spodaj.
  -  Italiansko datoteko v .xls shrani v vhodno datoteko kot .csv
  -  Spremeni kodiranje vhodne datoteke na utf-8.
  -  Med kategorijami zbriši vse (seveda ne tekmovalcev), vmes pusti le prazno vrstico.
  -  V kategorije po vrsti vpiši skupinam tekmovalcev pripadajoče skupine.
  -  Poženi datoteko (python 3).
  -  Program predpostavi, da ima vsak samo en priimek. Če to ni res je treba
  popraviti na roko (sicer bi bilo potrebno popravljati ljudi, z več imeni)."""
vhodna_datoteka = 'sol2a.csv'
izhodna_datoteka = 'sol2.csv'
kategorije = ["Začetniki","M10","M12","M14","M16","M18","M20","M35",
                      "M45","M55","M65","M21E","M21B","W10","W12",
                      "W14","W16","W18","W35","W45","W55","W21A","W21B"]

def pretvori(niz):
    niz1=niz.split(' ')
    b=''
    for niz in niz1:
        b+=niz[0]+niz[1:].lower()+' '
    return b[:-1]
with open(vhodna_datoteka,'r',encoding='utf-8') as f:
    with open(izhodna_datoteka,'w',encoding='utf-8')as g:
        g.write('@SI\n')
        g.write('Pl;First name;Surname;Time;Short;City;Classifier;\n')
        z = 0
        kat = kategorije[z]
        for i in f:
            a=i.split(';')
            if i!='\n':
                ime=''
                for k in a[3].split(' ')[1:]:
                    ime+=k+' '
                ime=pretvori(ime[:-1])
                priimek=pretvori(a[3].split(' ')[0])
                if a[2][0]=='=':
                    cas='mp'
                    clas='3'
                else:
                    cas=a[2]
                    clas='0'
                klub=a[8]
                mesto=a[0]
                if mesto:
                    mesto+='.'
                if mesto and mesto[0]=='\ufeff':
                    mesto=mesto[1:]
                g.write(mesto+';'+ime+';'+priimek+';'+cas+';'+kat+';'+klub+';'+clas+';\n')
            elif z < len(kategorije)-1:
                z+=1
                kat = kategorije[z]
                
            
