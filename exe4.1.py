
### Fill out and print a full sentence describing the temperature in F and C. 
import requests
from bs4 import BeautifulSoup

res = requests.get("http://forecast.weather.gov/MapClick.php?lat=21.3049&lon=-157.8579")
soup = BeautifulSoup(res.content, 'html.parser')


temp_F = soup.find(class_ =  "myforecast-current-lrg").getText()
temp_C  = soup.find(class_ =  "myforecast-current-sm").getText()

