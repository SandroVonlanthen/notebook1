


from urllib import request
from bs4 import BeautifulSoup
#
urlbase = " https://www.indeed.com/q-"
listjobs= ['teacher','lawyer','data-scientist']
urlfinisch = "-jobs.html"
returnDict= {}

for elemnts in listjobs:
    
    url = urlbase+elemnts+urlfinisch
    res = request.urlopen(url)
    soup = BeautifulSoup(res, 'html.parser')
    companyList =[]
    firstcompany= soup.find_all(class_ ="companyName")
    for company in firstcompany:
        companyList. append(company.getText())
    returnDict[elemnts]= companyList

#print(returnDict)    

for key, value in returnDict.items():
    print(key, ' : ', value)

