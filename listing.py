import constants
class Listing():
    
    def __init__(self,url='',id=0):
        self.url=url
        self.id=id
    
    def getSite():
    #stabileste apartenenta listingului
    #returneaza 1/0 gasit/negasit
    #salveaza in proprietatea 'site' a obiectului
        for i in constants.sites:
            for matches in constants.url_matches[i]:
                if (self.url.find(matches)==0):
                    self.site=i
                    return 1