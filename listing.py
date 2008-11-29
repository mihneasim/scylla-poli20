import constants
class Listing():
    
    def __init__(self,url='',id=0,site='',internal_id=0,title='',surface=0,rooms_no=0,available_rooms=0,price=0,monthly_price=0,expenses_included=0,coordinates=[], \
    images=[],string_location='',address='',location='',country='',zip=0,listing_date='', \
    features='',description='',other_info=''):
        self.url=url
        self.id=id
        self.site=site
        self.internal_id=internal_id
        
        self.title=title
        self.coordinates=coordinates
        self.surface=surface
        self.rooms_no=rooms_no #total number of rooms
        self.available_rooms=available_rooms
        self.price=price #pret proprietate
        self.monthly_price=monthly_price #chirie lunara
        self.expenses_included=expenses_included #intretinerea inclusa? 0/1
        self.listing_date=listing_date #data adaugarii anuntului, YYYY-MM-DD
        self.images = images #[i][0]-cale imagine mare, [i][1]-cale thumbnail daca exista
        self.string_location=string_location #locatia asa cum e definita pe site
        self.address=address #adresa (orice fara oras sau tara)
        self.location=location #orasul
        self.country=country #tara
        self.zip = zip
        
        self.features=features #gresie, faianta, gaze etc.
        self.description=description
        self.other_info = other_info #mesajul proprietarului, alte informatii etc.
        
        
    
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