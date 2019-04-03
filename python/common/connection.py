
import requests

class Connection:
    def __init__(self, name, username, password):
        self.__constructUrl(name)
        self.__uname = username
        self.__passw = password
        
    def __constructUrl(self, name):
        self.__url = "https://"+name+"atlassian.net"


