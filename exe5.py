
import requests
from bs4 import BeautifulSoup

header= requests.get("https://stackoverflow.com/questions/52570933/what-is-the-request-header-by-default-in-python-requests")

print ("--------------")

print (requests.get("https://stackoverflow.com/questions/52570933/what-is-the-request-header-by-default-in-python-requests").headers)
print ("--------------")

payload = {
"Host": "stackoverflow.com",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate, br",
"Referer": "https://www.google.com/",
"Connection": "keep-alive",
"Cookie": "prov=027c9553-0c4f-5a19-43a6-81f2aa78c4f1; _ga=GA1.2.9612263.1601718222; __gads=ID=076b06a0bc6ee9cf-2270a5dc60cd003a:T=1616424877:S=ALNI_MYxVIkTMVzrUCWQbQo_jz4Ig-Qr2Q; OptanonConsent=isIABGlobal=false&datestamp=Tue+Apr+06+2021+11%3A34%3A30+GMT%2B0200+(Central+European+Summer+Time)&version=6.10.0&hosts=&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1; OptanonAlertBoxClosed=2021-04-06T09:34:30.144Z; __gpi=UID=00000221a204aabf:T=1645990110:RT=1645990110:S=ALNI_MZw-f4WqT6TTBDgA5JMrf6mkm1Srg; _gid=GA1.2.648197543.1647509312",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "cross-site",
"Cache-Control": "max-age=0",
"TE": "trailers"
}

print (requests.get("https://stackoverflow.com/questions/52570933/what-is-the-request-header-by-default-in-python-requests", headers=payload).headers)


