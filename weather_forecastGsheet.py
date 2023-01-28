import gspread
from urllib.request import urlopen
from bs4 import BeautifulSoup

gc=gspread.service_account(filename='biofarmingmanager-creds.json')
sh=gc.open('Web_scraping_forecast').sheet1
request_data_location=sh.acell('A1').value

q1 = request_data_location.lower()
q2="http://www."
q3=".climatemps.com/temperatures.php"
query=q2+q1+q3
print('This is the link from where the forecast is obtained -', query)


html=urlopen(query)
bsObj=BeautifulSoup(html,"html.parser")

print(bsObj.body.h2)

Table_forecast_weather = bsObj.find("table",{"class":"countrytable"})

row_headers=[]
for i in Table_forecast_weather.find_all('tr'):
    for j in i.find_all('th'):
        row_headers.append(j.text)
print(row_headers)

tableValues=[]
for i in Table_forecast_weather.find_all('tr')[1:]:
    td_tags=i.find_all('td')
    td_values=[j.text for j in td_tags]
    tableValues.append(td_values)
print(td_values)

sh.update('A2', query)
sh.update('A3', row_headers)
sh.update('A4', td_values)
