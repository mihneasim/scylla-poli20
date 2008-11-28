import re,httplib2

def strip_tags(value):
    #"Return the given HTML with all tags stripped."
    return re.sub(r'<[^>]*?>', '', value) 

def request(url,type="GET",body='',headers={}):
    if(type=="POST"):
        headers['Content-type']='application/x-www-form-urlencoded'
    try:
        uh = httplib2.Http(".cache")
        ky,c =  uh.request(url,type,body,headers)
    except:
        return '',''
    return ky,c
    
'''remember:
  fromt=fromt.replace(/[\s+-\/\\$!@#%^&*()]+/g,'%20');
  fromt=fromt.replace(/^%20|%20$/g,'');
'''