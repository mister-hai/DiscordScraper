
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

