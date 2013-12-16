class signalCaught(Exception):
    def __init__(self, *args):
        # *args is used to get a list of the parameters passed in
        self.args = [a for a in args]

class customCookies():
    def __init__(self):
        self
    
    def isLogged(self,cj):
        for cookie in cj:
            if (cookie.name == 'c_user') or (cookie.name == 'checkpoint'):
                return True
        return False
    
    def checkPoint(self,cj):
        for cookie in cj:
            if (cookie.name == 'checkpoint'):
                print  '\r Checkpoint - Error                            \r',
                return True
        return False
    

def signal_handler(signal, frame):
    print "\n Aborted by user.\n"
    raise signalCaught('Control C')