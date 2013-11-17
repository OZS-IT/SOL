def sumniki(niz):
    #Vrne enak niz, brez sumnikov.
    sumniki=['š','č','ž','Š','Č','Ž','ć','Ć']
    nesumniki=['s','c','z','S','C','Z','c','C']
    a=''
    for i in niz:
        if i in sumniki:
            a+=nesumniki[sumniki.index(i)]
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
                if  tek.get(naziv,[0])[0]==kat and tek.get(naziv,[0])[3]<=st_tekme and rezultatiTekme[kat][naziv] not in ["dns","dnf","mp","DISQ"]:
                    seznamCasov.append((rezultatiTekme[kat][naziv][0])*3600+(rezultatiTekme[kat][naziv][1])*60+rezultatiTekme[kat][naziv][2])
                    
            seznamCasov.sort()
            for naziv in rezultatiTekme[kat].keys():
                if  tek.get(naziv,[0])[0]==kat and tek.get(naziv,[0])[3]<=st_tekme and rezultatiTekme[kat][naziv] not in ["dns","dnf","mp","DISQ"]:
                    RT=(rezultatiTekme[kat][naziv][0])*3600+(rezultatiTekme[kat][naziv][1])*60+rezultatiTekme[kat][naziv][2]
                    for i in range(len(seznamCasov)):
                        if seznamCasov[i]==RT:
                            mesto=i+1
                            break
                    stanjeLige[kat][naziv][st_tekme]=[rezultatiTekme[kat][naziv],tocke(mesto-1),mesto]

                elif tek.get(naziv,[0])[0]==kat  and tek.get(naziv,[0])[3]<=st_tekme:
                    if rezultatiTekme[kat][naziv]!="dns":
                        stanjeLige[kat][naziv][st_tekme]=[rezultatiTekme[kat][naziv],'-']
                vsota_=0
                k=0
                if rezultatiTekme[kat][naziv]not in ["dns","dnf","mp","DISQ"] and tek.get(naziv,[0])[0]==kat and tek.get(naziv,[0])[3]<=st_tekme:
                    for i,j in stanjeLige[kat][naziv].items():
                        if i not in ['sestevek','tekmaRegistracije','povprecje','klub','ime','priimek',0] and j[1]!='-' and j[1]>0:
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
                    if i in [k for k in range(1,12)] and j[1]!='-' and j[1]>0:#največ 11 lig je lahko
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
            elif rownum==0:
                pass
            else:
                colnum=0
                a=True
                for col in str(row[0]).split(';'):
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
                    elif header[colnum]=='Cl.name':
                        klub=col
                    elif header[colnum]=='Classifier':
                        ok=col
                    else:
                        pass            
                    colnum+=1
                ok=int(ok)
                classs={3:"mp",2:"dns",1:"dnf",4:"DISQ",0:True}
                
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
                a={'scommendrisio':'SCOM Mendriso','rodjezerskizmaj':'RJZ Velenje','ind':'ind.','ssdgaja':'SSD Gaja','okkomenda':'OK Komenda','pdajdovscina':'PD Ajdovščina','okazimut':'OK Azimut', 'okbrezice':'OK Brežice','okperkmandeljc':'OK Perkmandeljc','okpolaris':'OK Polaris','okslovenjgradec':'OK Slovenj Gradec','okslovenskekonjice':'OK Slovenske Konjice','oktivoli':'OK Tivoli','oktrzin':'OK Trzin','rjzvelenje':'RJZ Velenje','sok':'ŠOK'}
                if presledki(sumniki(klub1).lower()) in a.keys():
                    klub1=a[presledki(sumniki(klub1).lower())]
                else:
                    a[presledki(sumniki(klub1).lower())]=klub1

                ime1=presledki(ime1)
                priimek1=presledki(priimek1)
                naziv=ime1.lower()+priimek1.lower()
##                if naziv == "natasaaljancic":
##                    print(naziv,cas)
                #print(kategorija)
                if not kategorija:
                    pass
                elif kategorija[0]=="W":
                    kategorija="Ž"+kategorija[1:]
                elif kategorija[0]=="H":
                    kategorija="M"+kategorija[1:]
                elif kategorija[0]=="D":
                    kategorija="Ž"+kategorija[1:]
                if kategorija in kat:
                    if naziv not in stanjeLige[kategorija].keys():
                        if tek.get(naziv,[0])[0]!=0  and tek.get(naziv,[0])[3]<=st_lige:
                            rezultat[tek[naziv][0]][naziv]="mp"
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
                        rezultat[tek[naziv][0]][naziv]="mp"

            rownum+=1
    return rezultat


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
            h.sort()
            h=h[::-1]
            for t,z,naziv in h:
                if stanjeLige[k][naziv].get('klub',None)!=None:
                    if stanjeLige[k][naziv].get('sestevek',None)==None:
                            pass
                    elif stanjeLige[k][naziv].get(st_tekem,None)==None:
                        f.write(stanjeLige[k][naziv]['priimek']+';'+stanjeLige[k][naziv]['ime']+';'+str(stanjeLige[k][naziv]['klub'])+';'+k+';'+''+';'+''+';'+'')
                    elif stanjeLige[k][naziv][st_tekem][0] not in ["dns","dnf","mp","DISQ"]:
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
                    elif stanjeLige[k][naziv][st_tekem][0] not in ["dns","dnf","mp","DISQ"]:
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

