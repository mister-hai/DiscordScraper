
class ParentClass(object):
    def __new__(cls, *args, **kwargs):
        return super(__class__, cls).__new__(cls, *args, **kwargs)
    def __init__(self):
        self.data = {}
    def __call__(self):
        return self.data

class ChildClass(ParentClass):
    def __new__(cls, *args, **kwargs):
        print(super(__class__, cls).__new__(cls, *args, **kwargs))
    def __init__(self):
        self.data = {}
    def __call__(self):
        print("class name: " + self.__class__)

#now a more advanced example

# Python3 code to explain
# the type() function
  
# Class of type dict
class DictType:
    DictNumber = {1:'John', 2:'Wick',
                  3:'Barry', 4:'Allen'}
      
    # Will print the object type
    # of existing class
    print(type(DictNumber))
  
# Class of type list    
class ListType:
    ListNumber = [1, 2, 3, 4, 5]
      
    # Will print the object type
    # of existing class
    print(type(ListNumber))
  
# Class of type tuple    
class TupleType:
    TupleNumber = ('Geeks', 'for', 'geeks')
      
    # Will print the object type
    # of existing class
    print(type(TupleNumber))
  
# Creating object of each class    
d = DictType()
l = ListType()
t = TupleType()

class DiscordAuth(requests.auth.AuthBase):
    '''Change the nam, change the project.
    Basic requests Auth() implementation'''
    def __new__(cls, *args, **kwargs):
        #default fake value
        cls.username = "MisterHai"
        cls.token   = "NzE0NjA3NTAyOTg1MDAzMDgw.XxV-HQ.mn5f97TDYXtuFVgTwUccfsW4Guk"
        return super(DiscordAuth, cls).__new__(cls, *args, **kwargs)

    def __init__(self, token):
        if token:
            self.token = token

    def __call__(self):
        return self.username, self.token

class APIRequest():
    '''uses Requests to return specific routes from a base API url
    used for future stuff'''
    def __new__(cls, *args, **kwargs):
        #default fake value
        cls.apibaseurl = str
        cls.data       = bytes
        cls.thing      = bytes
        return super(__class__, cls).__new__(cls, *args, **kwargs)

    def __init__(self, apibaseurl:str, thing:str):
        pass

    def request(self, url, auth=('user', 'pass')):
        '''makes the actual request'''
        self.request_url = requote_uri("{}{}".format(self.apibaseurl,str(self.thing)))
        blueprint("[+] Requesting Resource: " + makered(self.request_url) + "\n")
        self.request_return = requests.get(self.request_url, auth=auth)
        return self.request_return

    def checkurlagainstdomain(self,urltoscan,listofdomains):
        parsedurl = urlparse(urltoscan)
        qwer = parsedurl.netloc.split('/')[2].split(':')[0]
        if qwer in listofdomains:
            return True
        else:
            return False

