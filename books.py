import json
from scraper import *
from data import  *
s = scraper()

cs = set()

def getCategories(url):
    response = s.getRequest(url)
    parsedResponse = s.parseResponse(response)
    articles = parsedResponse.find_all('article')
    for article in articles:
        a = article.find('h2',{'class':'entry-title'}).find('a')
        url = a['href']
        bookname = str(a.text).strip(' \n \n ')
        if bookname not in books_data:
            book = {}
            book['author']=[]
            book['desc'] = ''
            book['url'] = url
            books_data[bookname] = book
            print('\t\t' + bookname)
    return

def printData(data,name):
    data = json.dumps(data,indent=4)
    print(data)
    file = open(name+'.js','w')
    file.write(data)
    file.close()

def start():
    page = 1
    while page < 667:
        print('at page' + str(page))
        getCategories('http://www.allitebooks.com/page/' + str(page))
        page = page + 1

def printBook(b,book):
    b = '"' + b + '" :'
    print(b)
    bdata = json.dumps(book,indent=4)
    print(bdata)
    with open("books_data.js","a") as file:
        file.write(b)
        file.write(bdata)
    return

def downThem():
    i = 0
    for b in books_data:
        i = i + 1
        try:
            book = books_data[b]
            url = book['url']
            book['cat'] = []
            book['pdf'] = ''
            response = s.getRequest(url)
            parsedResponse = s.parseResponse(response)
            detail = parsedResponse.find('div',{'class':'book-detail'}).find('dl').findAll('dd')
            for a in detail[0].findAll('a'):
                author = a.text.strip(' \n \n ')
                book['author'].append(author)
            for a in detail[-1].findAll('a'):
                cat = a.text.strip(' \n \n ')
                book['cat'].append(cat)
            book['desc'] = str(parsedResponse.find('div',{'class':'entry-content'}).text).strip(' \n \n ')
            book['pdf'] = str(parsedResponse.find_all('span',{'class':'download-links'})[0].find('a')['href'])
            url = book['pdf']
            pdf = url.split('/')[-1]
            print(str(i) + '\t' + b)
            if i%500 == 0:
                printData(i)
            #s.downloadFile(url,'bookspdf',pdf)
        except:
            pass

for b in books_data:
    c = set(books_data[b]['cat'])
    cs = cs | c

stats = {
    'categories':[]
}
for c in cs:
    stats['categories'].append(c)

printData(stats,'stats')



