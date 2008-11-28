import common,re,wikimapia

def cleanHtml(url,striptags=0):
    #trage sursa html a paginii si opreste doar ce e folositor
    #care urmeaza sa treaca in viitor prin expresii regulate
    try:
        ky,c = common.request(url)
    except:
        print "Connection error to "+str(url)
        return ''
    html = c[(c.find("<div id=\"site_content\">")+23):c.find("<div id=\"site_statusbar\">")]
    if(striptags==1):
        html = common.strip_tags(html)
    return html    


def getStringLocation(html):
    #input: clean html cu strip tags
    #intoarce locatia asa cum e definita de user pe site
    html = html.replace("\n","").replace("\r","").replace("\t\t\t","^")
    try:
        return re.compile("Localizare:[\t\^]*([^\^]*)\^").findall(html)[0]
    except:
        return ''
    
def getCoordinatesLocation(location):
    #input: string location forma "cautcoleg.ro": particular (orasul town)
    #dandu-se locatia in string, se vor gasi coordonatele
    town=location[(location.rfind("(")+1):location.rfind(")")]
    town=town[6:]
    if(town[:6]=="Bucure"):
        town="Bucharest"
    #return
    town_country= town+ ", Romania"
    R=[]
    particular=(location[:location.rfind("(")]).strip()
    query=particular+' '+town+' '
    #in cazul in care nu gasim match pe localitate
    #returnam primul rezultat
    firstshot=1;
    Rbest=()
    while(query.rfind(" ")>-1):
        query=query[:query.rfind(" ")]
        
        #print "Looking for"+query
        R = wikimapia.search(query)
        #print R
        if(firstshot==1):
            firstshot=0
            try:
                Rbest=R[1][0]
            except:
                Rbest=()
        if(len(R[0])):
            #print 'here1'
            for i in range(len(R[0])):
                #print R[2][i]
                if(R[2][i].find(town_country)>-1) and (R[0][i].find(particular)>-1):
                    #se potrivesc si localitatea si titlul, intoarcem sigur
                    #print R[0][i]
                    #print "sure return"
                    return [R[1][i][1], R[1][i][0]]
                if(R[2][i].find(town_country)>-1):
                    #se potriveste orasul, salvam
                    Rbest = R[1][i]
                if(Rbest==() and (R[0][i].find(particular))):
                    #se potriveste titlul, dar nu si orasul
                    #salvam daca nimic pana acum
                    Rbest=R[1][i]
    if(Rbest!=()):
        return [Rbest[1], Rbest[0]]
    
    

def getProperty(html,property):
    #functie generala de extragere a unei valori
    #din table-ul html al paginii
    #pe baza cheii din prima coloana a tabelului
    html = html.replace("\n","").replace("\r","").replace("\t\t\t","^")
    try:
        #print html
        el=re.compile(property+"[\t\^]*([^\^]*)\^").findall(html)[0]
        return el
    except:
        return ''
    
def getSMSurface(html):
    #input html clean cu striptags
    #intoarce suprafata, metri patrati - get Square Meters Surface
    surface = getProperty(html,"Suprafa.*?a:")
    try:
        return surface[:surface.find(" ")]
    except:
        return ''
    
 
def getMonthlyPrice(html):
    #input html clean cu striptags
    #intoarce chiria lunara, EUR -
    price =  getProperty(html,"disponibil.*?\.")
    try:
        return price[:price.find(" ")]
    except:
        return ''
    
def areExpensesIncluded(html):
    are = getProperty(html,"n pre.*?:")
    if(are=="Nu"):
        return 0
    if(are=="Da"):
        return 1
    return -1

def getAvailableRooms(html):
    return getProperty(html,"Camere disponibile:")

def getListingDate(html):
    rawdate = getProperty(html,"Data anun.*?ului:")
    return rawdate



#Tests:   

#ch=cleanHtml('http://www.cautcoleg.ro/22869/caut-colegi-de-apartament-zona-dristor-metrou',1)
ch = cleanHtml('http://www.cautcoleg.ro/22453/caut-colega-de-apartament-zona-titan-metrou',1)
#print 'ok ch'
sl = getStringLocation(ch)
#print 'ok sl'
Coordinates = getCoordinatesLocation(sl)
print "http://maps.yahoo.com/#mvt=h&lat="+Coordinates[0]+"&lon="+Coordinates[1]+"&zoom=16"
print "data adaugare: "+getListingDate(ch)
print "suprafata: "+getSMSurface(ch)
print "camere disponibile: "+getAvailableRooms(ch)
print "pret lunar: "+getMonthlyPrice(ch)
print "intretinere inclusa: "+str(areExpensesIncluded(ch))


#wikimapia.search(locatie)
