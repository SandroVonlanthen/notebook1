
### Fill out and print a full sentence describing the temperature in F and C. 
from urllib import request
from bs4 import BeautifulSoup

res = request.urlopen("http://forecast.weather.gov/MapClick.php?lat=21.3049&lon=-157.8579")
soup = BeautifulSoup(res, 'html.parser')


temp_F = soup.find(class_ =  "myforecast-current-lrg").getText()
temp_C  = soup.find(class_ =  "myforecast-current-sm").getText()