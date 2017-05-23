import requests
import urllib
from bs4 import BeautifulSoup


class scraper:

    def __init__(self):
        self.s = requests.Session()

    def getRequest(self,url):
        response = self.s.get(url)
        return response

    def postRequest(self,url,data=None,json=None):
        response = self.s.post(url,data,json)
        return response

    def parseResponse(self,response):
        parsedResponse = BeautifulSoup(response.text,'lxml')
        return parsedResponse

    def downloadFile(self,url,path,fileName):
        urllib.request.urlretrieve(url,path + '/' + fileName)
        return

