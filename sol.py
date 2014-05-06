from sol_fun import *
from os import path
from re import sub
import csv
tek={}
stanjeLige={}
kat=set()
with open("Rezultati/solsko1.csv","r",encoding="utf-8") as f:
    with open("tekmovalci.csv","w",encoding="utf-8") as g:
        a = str(f.read())
        a=a.split("\n")
        header = a[1].split(";")
        pointer={}
        polja=["First name","Surname","City","Short"]
        for i in polja:
            pointer[i]=header.index(i)
        for i in range(2,len(a)):
            vrstica = a[i].split(";")
            ime = sub(r"\"",r"",vrstica[pointer["First name"]])
            priimek = sub(r"\"",r"",vrstica[pointer["Surname"]])
            klub = sub(r"\"",r"",vrstica[pointer["City"]])
            kate = sub(r"\"",r"",vrstica[pointer["Short"]])
            g.write("0;{0};{1};{2};{3}\n".format(ime,priimek,klub,kate))

with open("tekmovalci.csv",'r',encoding="utf-8") as f:
    for i in f:
        a=i.split(";")
        st=a[0]
        ime=a[1]
        priimek=a[2]
        klub=a[3]
        kate=a[4]
        s=presledki(sumniki(a[1]+a[2]))
        s=s.lower()
        if kate[-1] == "\n":
            kate = kate[:-1]
        kat.add(kate)
        if ime=="Žiga" and priimek=="Groff":
            st="483"
        elif ime == "Cesare" and priimek == "Tarrabocchia":
            klub = "OK Azimut"
        elif ime == "Andraž" and priimek == "De Luisa":
            klub = "OK Azimut"
        if s not in tek.keys():
            tek[s]=[kate,ime,priimek,0,klub,st]
for i in kat:
    stanjeLige[i]={}
for i in tek.keys():
    b=tek[i]
    stanjeLige[b[0]][i]={"ime":b[1],"priimek":b[2],"klub":b[4],0:0,"tekmaRegistracije":b[3]}

st_tekem=0
IP=1
zadnja=16
for st_lige in range(1,12):
    if st_lige==zadnja:#Nočemo, da se zgodi v sol, je pa na voljo.
        IP=1.15
    if path.isfile('./Rezultati/solsko'+str(st_lige)+'.csv'):
        c=rezultati(st_lige,stanjeLige,kat,tek)
        stanjeLige=izracunLige(c,st_lige,stanjeLige,IP,kat,tek)
        #print(stanjeLige["M55"])
        #print(stanjeLige["M21E"]["jurezmrzlikar"])
        st_tekem+=1
        vCsv(stanjeLige,st_tekem,kat,tek)
klubsko(stanjeLige,list(kat),st_tekem)
