class Auth(object):
    def __init__(self,
                 apikey: str = None,
                 userkey: str = None,
                 username: str = None):
        self.apikey = apikey
        self.userkey = userkey
        self.username = username
