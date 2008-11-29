import common,re,wikimapia
import time # for benchmarking only

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
    
def getAddress(string_location):
    return string_location[:string_location.rfind("(")]
    
def getLocation(string_location):
    #intoarce locatia, adica Orasul
    town=string_location[(string_location.rfind("(")+1):string_location.rfind(")")]
    town=town[6:]
    if(town[:6]=="Bucure"):
        town="Bucharest"
    return town
    
def getCountry(string_location):
    #intoarce tara
    return 'Romania'
    
def getCoordinatesLocation(address,location,country):
    #input: .. 
    #dandu-se locatia in string, se vor gasi coordonatele
    #return
    town=location
    town_country= town+ ", "+country
    R=[]
    particular=address
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
    
    
def getInternalId(url):
    return re.compile("cautcoleg.ro\/([0-9]*?)\/").findall(url)[0]

def getProperty(html,property,index=0):
    #functie generala de extragere a unei valori
    #din table-ul html al paginii
    #pe baza cheii din prima coloana a tabelului
    html = html.replace("\n","").replace("\r","").replace("\t\t\t","^")
    try:
        #print html
        el=re.compile(property+"[\t\^]*([^\^]*)\^").findall(html)[index]
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
    #input: clean html, strip tags
    #Intretinerea inclusa? 0 sau 1
    are = getProperty(html,"n pre.*?:")
    if(are=="Nu"):
        return 0
    if(are=="Da"):
        return 1
    return -1

def getAvailableRooms(html):
    #input: clean html, strip tags
    #camere disponibile inchirierii
    return getProperty(html,"Camere disponibile:")

def getListingDate(html):
    #input: clean html, strip tags
    #intoarce data adaugarii, YYYY-MM-DD
    rawdate = getProperty(html,"Data anun.*?ului:")
    return rawdate

def getImages(html,internal_id):
    #Atentie! se primeste clean html, dar fara strip tags! si idul intern cautcoleg.ro
    #images[i][0]-adresa imagine mare, images[i][1]-adresa thumbnail
    i=1
    images=[]
    while(html.find("showSitePhotos.php?ad_id="+str(internal_id)+"&amp;number="+str(i))>-1):
        images.append(["http://www.cautcoleg.ro/showPhoto.php?type=site&ad_id="+str(internal_id)+"&number="+str(i),\
        "http://www.cautcoleg.ro/showPhoto.php?type=thumbs&ad_id="+str(internal_id)+"&number="+str(i)])
        i+=1
    return images

def getTitle(html):
    #to be done!!
    pass
    
def getRoomsNo(html):
    #to be done!!
    pass

def getDescription(html):
    #input: clean stripped html
    return getProperty(html,"Descriere")
    
def getFeatures(html):
    #input: clean stripped html
    return getProperty(html,"Facilit.*?i")
    
def getOtherInfo(html): #to be repaired!!
    #input: clean stripped html
    return getProperty(html,"aut coleg.*? de apartament",1)








#Tests:   
start = time.time()
#ch=cleanHtml('http://www.cautcoleg.ro/22869/caut-colegi-de-apartament-zona-dristor-metrou',1)

url='http://www.cautcoleg.ro/22453/caut-colega-de-apartament-zona-titan-metrou'
url='http://www.cautcoleg.ro/22264/caut-colega-de-apartament-zona-dristor'

chnostrip = cleanHtml(url,0)
print "grabbed in "+str(time.time()-start)[:-7]+" seconds"
ch = common.strip_tags(chnostrip)
#print ch.replace("\n","").replace("\r","").replace("\t\t\t","^")
#print 'ok ch'
sl = getStringLocation(ch)
location = getStringLocation(sl)
country = getCountry(sl)
address = getAddress(sl)
#print 'ok sl'
Coordinates = getCoordinatesLocation(address,location,country)
print "grabbed and located in "+str(time.time()-start)[:-7]+" seconds"
print "http://maps.yahoo.com/#mvt=h&lat="+Coordinates[0]+"&lon="+Coordinates[1]+"&zoom=16"
print "data adaugare: "+getListingDate(ch)
print "suprafata: "+getSMSurface(ch)
print "camere disponibile: "+getAvailableRooms(ch)
print "pret lunar: "+getMonthlyPrice(ch)
print "intretinere inclusa: "+str(areExpensesIncluded(ch))
print "imagini: "+str(getImages(chnostrip,getInternalId(url)))
print "\ndescriere: "+getDescription(ch)
print "\nfeatures: "+getFeatures(ch)
print "\nAlte info: "+getOtherInfo(ch)

print "grabbed, located and parsed in "+str(time.time()-start)[:-7]+" seconds"

#wikimapia.search(locatie)
