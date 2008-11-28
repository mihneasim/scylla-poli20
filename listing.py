import constants
class Listing():
    
    def __init__(self,url='',id=0,site='',surface=0,available_rooms=0,monthly_price=0,expenses_included=0,coordinates=[],string_location='',listing_date=''):
        self.url=url
        self.id=id
        self.site=site
        
        self.coordinates=coordinates
        self.surface=surface
        self.available_rooms=available_rooms
        self.monthly_price=monthly_price
        self.expenses_included=expenses_included
        self.listing_date=listing_date
        self.string_location=string_location
        
    
    def getSite():
    #stabileste apartenenta listingului la o platforma
    #returneaza 1/0 gasit/negasit
    #salveaza in proprietatea 'site' a obiectului
        for i in constants.sites:
            for matches in constants.url_matches[i]:
                if (self.url.find(matches)==0):
                    self.site=i
                    return 1
        return 0