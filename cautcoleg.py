import httplib2,common,re  #,wikimapia

def cleanHtml(url,striptags=0):
    #trage sursa html a paginii si opreste doar ce e folositor
    #care urmeaza sa treaca in viitor prin expresii regulate
    try:
        uh = httplib2.Http(".cache")
        ky,c =  uh.request(url,"GET")
    except:
        print "Connection error to "+string(url)
        return ''
    html = c[(c.find("<div id=\"site_content\">")+23):c.find("<div id=\"site_statusbar\">")]
    if(striptags==1):
        html = common.strip_tags(html)
    return html
    



def getStringLocation(html):
    #intoarce locatia asa cum e definita de user pe site
    html = html.replace("\n","").replace("\r","").replace("\t\t\t","^")
    try:
        return re.compile("Localizare:[\t\^]*([^\^]*)\^").findall(html)[0]
    except:
        return ''
    
    
#Suprafata:
def getSMSurface(html):
    #intoarce suprafata, metri patrati - get Square Meters Surface
    html = html.replace("\n","").replace("\r","").replace("\t\t\t","^")
    try:
        el=re.compile("Suprafa.*?a:[\t\^]*([^\^]*)\^").findall(html)[0]
        return el[:el.find(" ")]
    except:
        return ''
    
 

#Tests:   
print getSMSurface(cleanHtml('http://www.cautcoleg.ro/22931/caut-colega-de-apartament-zona-rahova-alexandriei',1))
#wikimapia.search(locatie)