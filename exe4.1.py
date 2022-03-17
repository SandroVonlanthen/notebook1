



from urllib import request
from bs4 import BeautifulSoup


res = request.urlopen("http://forecast.weather.gov/MapClick.php?lat=21.3049&lon=-157.8579")
soup = BeautifulSoup(res, 'html.parser')

#temp = soup.find(id_ =  "detailed-forecast-body")

temp = soup.find("div", {"id": "detailed-forecast-body"})

temp1= temp.find_all("div", {"class": "row row-even row-forecast"})
temp2= temp.find_all("div", {"class": "row row-odd row-forecast"})


for i in range(7):
    
    quando2 = temp2[i].find(class_ =  "col-sm-2 forecast-label").getText()
    info2 = temp2[i].find(class_ =  "col-sm-10 forecast-text").getText()
    print("%s:  %s"%(quando2, info2))

    quando1 = temp1[i].find(class_ =  "col-sm-2 forecast-label").getText()
    info1 = temp1[i].find(class_ =  "col-sm-10 forecast-text").getText()
    print("%s:  %s"%(quando1, info1))



