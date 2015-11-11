def sumniki(niz):
    #Vrne enak niz, brez sumnikov.
    sumniki={'š':'s','č':'c','ž':'z','Š':'S','Č':'C','Ž':'Z','ć':'c','Ć':'C','ö':'o','ä':'a','Ä':'A','Ö':'O'}
    a=''
    for i in niz:
        if sumniki.get(i):
            a+=sumniki.get(i)
        else:
            a+=i
    return a
def presledki(niz):
    a=''
    for i in niz:
        if i!=' ':
            a+=i
    return a
def tocke(i):
    #i je mesto
    t=[25,20,15,12,10,8,7,6,5,4,3,2,1]
    if i>len(t)-1:
        return 1
    return t[i]
def izracunLige(rezultatiTekme,st_tekme,stanjeLige,IP,kategorija,tek):
    #'st_tekme' je št SOL(npr. pri SOL2, je to 2).
    #IP je vrednost tekme(1.2 pomeni, da je tekmo vredna 20 % več).
    #stanjeLige mora biti enako stanjeLige[kategorija]
    for kat in kategorija:
        if rezultatiTekme[kat]:
            #Sestavljamo seznam z časi in točkami.
            seznamCasov=[]
            for naziv in rezultatiTekme[kat].keys():
                if  tek.get(naziv,[0])[0]==kat and tek.get(naziv)[3]<=st_tekme and rezultatiTekme[kat][naziv] not in ["dns","dnf","mp","DISQ","wrongKat"]:
                    seznamCasov.append((rezultatiTekme[kat][naziv][0])*3600+(rezultatiTekme[kat][naziv][1])*60+rezultatiTekme[kat][naziv][2])
                    
            seznamCasov.sort()
            for naziv in rezultatiTekme[kat].keys():
                if  tek.get(naziv,[0])[0]==kat and tek.get(naziv,[0])[3]<=st_tekme and rezultatiTekme[kat][naziv] not in ["dns","dnf","mp","DISQ","wrongKat"]:
                    RT=(rezultatiTekme[kat][naziv][0])*3600+(rezultatiTekme[kat][naziv][1])*60+rezultatiTekme[kat][naziv][2]
                    for i in range(len(seznamCasov)):
                        if seznamCasov[i]==RT:
                            mesto=i+1
                            break
                    stanjeLige[kat][naziv][st_tekme]=[rezultatiTekme[kat][naziv],tocke(mesto-1),mesto]

                elif tek.get(naziv,[0])[0]==kat  and tek.get(naziv,[0])[3]<=st_tekme:
                    if rezultatiTekme[kat][naziv] == "wrongKat":
                        stanjeLige[kat][naziv][st_tekme]=[rezultatiTekme[kat][naziv],'*', float("inf")]
                    elif rezultatiTekme[kat][naziv]!="dns":
                        stanjeLige[kat][naziv][st_tekme]=[rezultatiTekme[kat][naziv],'-', float("inf")] #dodal sem float(inf), da lahko primerjam kdo je večkrat premagal druge z <
                vsota_=0
                k=0
                if rezultatiTekme[kat][naziv]not in ["dns","dnf","mp","DISQ","wrongKat"] and tek.get(naziv,[0])[0]==kat and tek.get(naziv,[0])[3]<=st_tekme:
                    for i,j in stanjeLige[kat][naziv].items():
                        if i not in ['sestevek','tekmaRegistracije','povprecje','klub','ime','priimek',0] and j[1]!='-' and j[1]!='*' and j[1]>0:
                            vsota_+=round(j[1])
                            k+=1
                        else:
                            pass
                if k!=0:
                    stanjeLige[kat][naziv][0]=[0,round(vsota_/k)]

            #Računamo skupni seštevek lige.
            for naziv in stanjeLige[kat].keys():
                seznam=[]
                for i,j in stanjeLige[kat][naziv].items():
                    if i in [k for k in range(1,12)] and j[1]!='-' and j[1]!='*' and j[1]>0:#največ 11 lig je lahko
                        seznam.append(j[1])
                seznam.sort()
                seznam=seznam[::-1]
                if len(seznam)==0:
                    stanjeLige[kat][naziv]['sestevek']=0
                    stanjeLige[kat][naziv]['povprecje']=0
                elif len(seznam)>=5:
                    stanjeLige[kat][naziv]['sestevek']=sum(seznam[0:5])
                    stanjeLige[kat][naziv]['povprecje']=round(sum(seznam[0:5])/5)
                else:
                    stanjeLige[kat][naziv]['sestevek']=sum(seznam[0:len(seznam)])
                    stanjeLige[kat][naziv]['povprecje']=round(sum(seznam[0:len(seznam)])/len(seznam))
    return stanjeLige




def rezultati(st_lige,stanjeLige,kat,tek):
    #Vrne rezultate tekme v slovarju oblike {kategorija:rezultatiKategorija,...}.
    rezultat={}
    for i in kat:
        rezultat[i]={}
    import csv
    kodiranje='utf-8'
    with open('./Rezultati/SOL'+str(st_lige)+'.csv',encoding=kodiranje) as f:
        reader=csv.reader(f)
        rownum=0
        for row in reader:
            #print(row)
            if rownum==1:
                header=str(row[0]).split(';')
                #print('\n\n')
            elif rownum==0:
                pass
            else:
                colnum=0
                a=True
                #print(row)
                for col in row[0].split(';'):
                    if colnum>=len(header):
                        break
                    if header[colnum]=='First name':
                        ime=col
                    elif header[colnum]=='Surname':
                        priimek=col
                    elif header[colnum]=='Short':
                        kategorija=col
                    elif header[colnum]=='Time':
                        if col==''or col =='\"\"' or col in ["dns","dnf","mp","DISQ"]:
                            cas1=False
                        else:
                            cas1=col
                            if len(cas1.split(':')[0])< 3:
                                if cas1[1]!=':':
                                    if int(cas1[:2])>5 and len(cas1)>5:
                                        cas1='00:'+cas1[:-2]
                                else:
                                    if int(cas1[0])>5 and len(cas1)>5:
                                        cas1='00:'+cas1[:-2]
                            else:
                                ggz=cas1.split(':')
                                cas1=str(int(ggz[0])//60)+':'+str(int(ggz[0])%60)+':'+ggz[1]
                    elif header[colnum]=="City":
                        klub=col
                    elif header[colnum]=='Classifier':
                        ok=col
                    else:
                        pass            
                    colnum+=1
                #print(row[0].split(';'))
                ok=int(ok)
                classs={3:"mp",1:"dns",2:"dnf",4:"DISQ",0:True}
                
                if cas1==False and ok not in [1,2,3,4]:
                    cas="mp"
                elif ok in [1,2,3,4]:
                    cas1=classs[ok]
                    if cas1!=True:
                        cas=cas1
                else:
                    cas=['','','']
                    st_dvopicij=0
                    for y in cas1:
                        if y!=':'and y!='"':
                            cas[st_dvopicij]+=str(y)
                        elif y=='"':
                            pass
                        else:
                            st_dvopicij+=1
                    if cas[2]=='':
                        cas[2]=cas[1]
                        cas[1]=cas[0]
                        cas[0]=str(0)
                    cas=[int(cas[0]),int(cas[1]),int(cas[2])]
                if not ok and cas not in["dns","dnf","mp","DISQ"]:
                    for i in range(2,0,-1):
                        if cas[i]>=60:
                            cas[i-1]=cas[i-1]+cas[i]//60
                            cas[i]=cas[i]%60                       
                a=''
                for i in klub:
                    if i.isalpha() or i==' ':
                        a+=i
                klub=a
                
                a=''
                b=0
                for i in ime:
                    if i.isalpha():
                        if b==0:
                            i=i.upper()
                        a+=i
                    b+=1
                ime=a
                a=''
                b=0
                for i in ime:
                    if i.isupper()and b!=0:
                        a+=' '
                        a+=i
                    else:
                        a+=i
                    b+=1
                ime=a
                a=''
                b=0
                for i in priimek:
                    if i.isalpha():
                        if b==0:
                            i=i.upper()
                        a+=i
                    b+=1
                priimek=a
                a=''
                b=0
                for i in priimek:
                    if i.isupper() and b!=0:
                        a+=' '
                        a+=i
                    else:
                        a+=i
                    b+=1
                priimek=a
                a=''
                for i in kategorija:
                    if i!='"':
                        a+=i
                kategorija=a
                ime1=sumniki(ime)
                priimek1=sumniki(priimek)
                klub1=klub
                if ime1=='Nejc'and priimek1=='Zorman':
                    ime1='Jernej'
                elif ime1=='Ivo'and priimek1=='Kette':
                    priimek1='Kete'
                a={'mokmariborskiok':'Mariborski OK','kamniskiokkok': 'Kamniški OK','scommendrisio':'SCOM Mendriso','rodjezerskizmaj':'RJZ Velenje','ind':'ind.','ssdgaja':'SSD Gaja','okkomenda':'OK Komenda','pdajdovscina':'PD Ajdovščina','orientacijskiklubazimutokazimut':'OK Azimut', 'okbrezice':'OK Brežice','okperkmandeljc':'OK Perkmandeljc','okpolaris':'OK Polaris','okslovenjgradec':'OK Slovenj Gradec','okslovenskekonjice':'OK Slovenske Konjice','oktivoli':'OK Tivoli','oktrzin':'OK Trzin','rjzvelenje':'RJZ Velenje','sok':'ŠOK'}
                if presledki(sumniki(klub1).lower()) in a.keys():
                    klub1=a[presledki(sumniki(klub1).lower())]
                else:
                    a[presledki(sumniki(klub1).lower())]=klub1

                ime1=presledki(ime1)
                priimek1=presledki(priimek1)
                naziv=ime1.lower()+priimek1.lower()
                if naziv == "ivanboyadzhievml":
                    naziv+="."
                    #print(naziv,cas)
                #print(kategorija)
                if not kategorija:
                    pass
                elif kategorija[0]=="W":
                    kategorija="Ž"+kategorija[1:]
                elif kategorija[0]=="H":
                    kategorija="M"+kategorija[1:]
                elif kategorija[0]=="D":
                    kategorija="Ž"+kategorija[1:]
                elif kategorija[:2]=="MW":
                    kategorija="MŽ"+kategorija[2:]
                elif kategorija[:2]=="MD":
                    kategorija="MŽ"+kategorija[2:]
                elif kategorija[:2]=="HW":
                    kategorija="MŽ"+kategorija[2:]
                elif kategorija[:2]=="HD":
                    kategorija="MŽ"+kategorija[2:]
                if kategorija in kat:
                    if naziv not in stanjeLige[kategorija].keys():
                        if tek.get(naziv,[0])[0]!=0  and tek.get(naziv)[3]<=st_lige:
                            rezultat[tek[naziv][0]][naziv]="wrongKat"
                        #stanjeLige[kategorija][naziv]={0:0,'ime':ime,'priimek':priimek,'klub':klub1}
                    elif stanjeLige[kategorija][naziv].get('klub',1)==(1 or '' or 'ind.' or ' '):
                        if klub1==(' 'or''or'ind'):
                            klub1=='ind.'
                        stanjeLige[kategorija][naziv]['klub']=klub1                     
                        rezultat[kategorija][naziv]=cas
                    else:
                        rezultat[kategorija][naziv]=cas
                else:
                    if naziv in tek.keys():
                        rezultat[tek[naziv][0]][naziv]="wrongKat"

            rownum+=1
    return rezultat

def popraviEnakoTock(h, stanjeLigeKat, stTekem):
    #Če ima več ljudi enako točk jih razvrsti, kot je v pravilniku
    print("Tekma: ",stTekem,"\n\n\n\n\n")

    #najdemo vse ljudi z enako točkami
    def najdiEnake(h):
        d = {}
        k = 0
        for sestevek,povprecje,naziv in h:
            d[sestevek] = d.get(sestevek,[])+[(naziv,k)]
            k += 1
        return [j for i,j in d.items() if len(j) > 1 and i > 0]
    enaki = najdiEnake(h) # seznam seznamov ljudi z enakimi točkami
    #print(enaki)
    for i in enaki:
        #računamo število zmag nad vsemi ostalimi
        zmage = [0] * len(i)
        for st in range(1, stTekem+1):
            mesto = [0] * len(i)
            for j in range(len(i)):
                try: #niso vsi na vseh tekmah
                    if stanjeLigeKat[i[j][0]][st][1] != "*":
                        mesto[j] = stanjeLigeKat[i[j][0]][st][2]
                except:
                    pass
            for j in range(len(i)):
                zmage[j] += len([mest for mest in mesto if (mest > mesto[j] and not mest == 0 and not mesto[j] == 0)]) 
                #print(zmage)
            #print("------")
        zmage = [(zmage[j],i[j][1],i[j][0]) for j in range(len(zmage))]
        zmage.sort(key = lambda x: -x[0])
        #print(zmage)
        indeksi = [k[1] for k in zmage]
        if len(set([zmaga[0] for zmaga in zmage])) == len(zmage):
            #Če imajo tudi po tem kriteriju tekmovalci enak izkupiček, gledamo mesta po vrsti
            noviEnaki = najdiEnake(zmage)
            for skupina in noviEnaki:
                mesta = [([stanjeLigeKat[k[0]][st][2] if not (stanjeLigeKat[k[0]].get(st) == None) else float("inf") for st in range(1, stTekem+1)],k[1]) for k in skupina]
                for bla in range(len(mesta)):
                    seznamcek = mesta[bla][0]
                    seznamcek.sort()
                    mesta[bla] = (seznamcek,mesta[bla][1])
                mesta.sort(key = lambda x: x[0] if x[0] else float("inf")) #če ni tekmoval dobi inf
                indeksi1 = [k[1] for k in mesta]
                #zmanjkalo kriterijev, kakor je, je mesta popravi ročno (v html-ju, jaz jih itak ne pišem)
                zmage[min(indeksi1):max(indeksi1)+1] = [zmage[bla] for bla in indeksi1]
                if not len(set([tuple(mesto[0]) for mesto in mesta])) == len(mesta):
                    print("Tekmovalc(a)i " + ", ".join([zmage[bla][2] for bla in indeksi1]) + " se ujemajo v vseh kriterijih.")
        #kar se je dalo popraviti smo
        h[min(indeksi):max(indeksi)+1] = [h[k[1]] for k in zmage]
        #print(h)
    return h
                

def vCsv(stanjeLige,st_tekem,kat,tek):
    with open('./Stanja racunana/SOL'+str(st_tekem)+'.csv','w+',encoding='utf-8') as f:
        #st_tekem-=1
        f.write('Surname;First name;Cl.name;Class;Time;Pl;Points')
        for i in range(1,st_tekem +1):
            f.write(';'+'SOL'+str(i))
        f.write(';Sum;Average;ID\n')
        kat1=list(kat)
        kat1.sort()
        for k in kat1:
            h=[]
            for naziv in stanjeLige[k].keys():
                if stanjeLige[k][naziv].get('sestevek',None)!=None:
                    h.append((stanjeLige[k][naziv]['sestevek'],stanjeLige[k][naziv]['povprecje'],naziv))
            h.sort(key = lambda x:  1/x[0] if x[0] else float("inf"))
            h = popraviEnakoTock(h, stanjeLige[k], st_tekem)
            for t,z,naziv in h:
                if stanjeLige[k][naziv].get('klub',None)!=None:
                    if stanjeLige[k][naziv].get('sestevek',None)==None:
                            pass
                    elif stanjeLige[k][naziv].get(st_tekem,None)==None:
                        f.write(stanjeLige[k][naziv]['priimek']+';'+stanjeLige[k][naziv]['ime']+';'+str(stanjeLige[k][naziv]['klub'])+';'+k+';'+''+';'+''+';'+'')
                    elif stanjeLige[k][naziv][st_tekem][0] not in ["dns","dnf","mp","DISQ","wrongKat"]:
                        cas=''
                        podpicja=0
                        for j in range(3):
                            for i in str(stanjeLige[k][naziv][st_tekem][0][j]):
                                if len(str(stanjeLige[k][naziv][st_tekem][0][j]))<2 and j!=0:
                                    cas+='0'
                                cas+=i
                            podpicja+=1
                            if podpicja!=3:
                                    cas+=':'
                        f.write(stanjeLige[k][naziv]['priimek']+';'+stanjeLige[k][naziv]['ime']+';'+str(stanjeLige[k][naziv]['klub'])+';'+k+';'+cas+';'+str(stanjeLige[k][naziv][st_tekem][2])+';'+str(stanjeLige[k][naziv][st_tekem][1]))
                    else:
                        #print("1")
                        f.write(stanjeLige[k][naziv]['priimek']+';'+stanjeLige[k][naziv]['ime']+';'+str(stanjeLige[k][naziv]['klub'])+';'+k+';'+stanjeLige[k][naziv][st_tekem][0]+';'+''+';'+'')
                    if stanjeLige[k][naziv].get('sestevek',None)!=None:
                        for i in range(1,st_tekem +1):
                            if stanjeLige[k][naziv].get(i,None)!=None:
                                f.write(';'+str(stanjeLige[k][naziv][i][1]))
                            else:
                                f.write(';'+'')
                        f.write(';'+str(stanjeLige[k][naziv]['sestevek'])+';'+str(stanjeLige[k][naziv]['povprecje'])+';'+tek[naziv][5]+'\n')

                else:
                    if stanjeLige[k][naziv].get('sestevek',None)==None:
                            pass
                    elif stanjeLige[k][naziv].get(st_tekem,None)==None:
                        f.write(stanjeLige[k][naziv]['priimek']+';'+stanjeLige[k][naziv]['ime']+';'+''+';'+k+';'+''+';'+''+';'+'')
                    elif stanjeLige[k][naziv][st_tekem][0] not in ["dns","dnf","mp","DISQ","wrongKat"]:
                        cas=''
                        podpicja=0
                        for j in range(3):
                            for i in str(stanjeLige[k][naziv][st_tekem][0][j]):
                                cas+=i
                            podpicja+=1
                            if podpicja!=3:
                                cas+=':'
                        f.write(stanjeLige[k][naziv]['priimek']+';'+stanjeLige[k][naziv]['ime']+';'+''+';'+k+';'+str(cas)+';'+str(stanjeLige[k][naziv][st_tekem][2])+';'+str(stanjeLige[k][naziv][st_tekem][1]))
                    else:
                        f.write(stanjeLige[k][naziv]['priimek']+';'+stanjeLige[k][naziv]['ime']+';'+''+';'+k+';'+stanjeLige[k][naziv][st_tekem][0]+';'+''+';'+'')
                    if stanjeLige[k][naziv].get('sestevek',None)!=None:
                        for i in range(1,st_tekem +1):
                            if stanjeLige[k][naziv].get(i,None)!=None:
                                f.write(';'+str(stanjeLige[k][naziv][i][1]))
                            else:
                                f.write(';'+'')
                        f.write(';'+str(stanjeLige[k][naziv]['sestevek'])+';'+str(stanjeLige[k][naziv]['povprecje'])+';'+tek[naziv][5]+'\n')

