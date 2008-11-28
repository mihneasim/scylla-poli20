import urllib,re,common
'''
class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable


class Wikimapia:
'''
def search(q,latstart=44.426801,lonstart=26.10211):
    #remember to use some urlencoding instead
    qencoded=q.replace(" ","%2520")
    #common.request('http://wikimapia.org/#lat=44.8402907&lon=24.9609375&z=3&l=0&m=a&v=2')
    url='http://wikimapia.org/sys/search4/?q='+qencoded
    posts={'y':int(round(latstart*10000000)),'x':int(round(lonstart*10000000)),'z':16, 'start':0, 'jtype':'', 'try':0, 'qu':q}
    ky,f=common.request(url,"POST",urllib.urlencode(posts))
    items=re.compile("<span class=\"sname\">(.*?)</span>").findall(f)
    coords=re.compile("parent\.zoom_from_inf\(([0-9\.]*),([0-9\.]*),([0-9]*)\)").findall(f)
    locations=re.compile("<span class=\"desc\">(.*?)</span>").findall(f)
    
    #print "Items: "+str(items)
    #print "Coordinates: "+str(coords)
    #print "Locations: "+str(locations)
    
    return [items,coords,locations]
    #print f
#search=Callable(search)
#Test:
#search("lia manoliu")