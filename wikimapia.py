import urllib,re

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable


class Wikimapia:
    def search(q):
        q=q.replace(" ","%2520")
        url='http://wikimapia.org/sys/search4/?q='+q
        f=urllib.urlopen(url).read()
        items=re.compile("<span class=\"sname\">(.*?)</span>").findall(f)
        coords=re.compile("parent\.zoom_from_inf\(([0-9\.]*),([0-9\.]*),([0-9]*)\)").findall(f)
        locations=re.compile("<span class=\"desc\">(.*?)</span>").findall(f)
        
        print "Items: "+str(items)
        print "Coordinates: "+str(coords)
        print "Locations: "+str(locations)
        
        return [items,coords,locations]
        #print f
    search=Callable(search)

Wikimapia.search("lia manoliu")