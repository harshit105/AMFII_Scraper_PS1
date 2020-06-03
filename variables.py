from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.amfiindia.com/ter-of-mf-schemes'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

#year- Scraped(Automatic)
yrlocation=page_soup.find('div',{'id':'divFinTER'})
yroptions=yrlocation.find_all("option")
year=[x.text for x in yroptions]
# print(year)
#year=['2020-2021','2019-2020', '2018-2019']

#month_dictionary- Add new month after every 1 month manually
month_dictionary={
    '2018-2019':['March-2019','February-2019','January-2019','December-2018','November-2018','October-2018','September-2018','August-2018','July-2018','June-2018','May-2018','April-2018','January-2018'],
    '2019-2020':['April-2020','March-2020','February-2020','January-2020','December-2019','November-2019','October-2019','September-2019','August-2019','July-2019','June-2019','May-2019','April-2019'],
    '2020-2021':['June-2020','May-2020','April-2020']
}


#type of mf's- dict. made manually
dummy1=['Open Ended','Interval Fund','Close Ended']
dummy2=['Debt Scheme','Equity Scheme','Hybrid Scheme','Other Scheme','Solution Oriented Scheme']
typeOfMF={
    "Open Ended":{
        "Debt Scheme":['Overnight Fund','Liquid Fund','Ultra Short Duration Fund','Low Duration Fund','Money Market Fund','Short Duration Fund','Medium Duration Fund','Medium to Long Duration Fund','Long Duration Fund','Dynamic Bond','Corporate Bond Fund','Credit Risk Fund','Banking and PSU Fund','Gilt Fund','Gilt Fund with 10 year constant duration','Floater Fund'],
        "Equity Scheme":['Multi Cap Fund','Large Cap Fund','Large & Mid Cap Fund','Mid Cap Fund','Small Cap Fund','Dividend Yield Fund','Value Fund','Contra Fund','Focussed Fund','Sectoral/ Thematic','ELSS'],
        "Hybrid Scheme":['Conservative Hybrid Fund','Balanced Hybrid Fund','Aggressive Hybrid Fund','Dynamic Asset Allocation or Balanced Advantage','Multi Asset Allocation','Arbitrage Fund','Equity Savings'],
        "Other Scheme":['Index Funds','Gold ETF','Other  ETFs','FoF Overseas','FoF Domestic'],
        "Solution Oriented Scheme":['Retirement Fund','Children’s Fund']
    },
    "Interval Fund":['Growth','Income'],
    "Close Ended":['Assured Return','Balanced','ELSS','Fund of Funds - Domestic','Gilt','Growth','Income','Liquid','Money Market']
}

#mutual_funds
mflocation=page_soup.find('div',{'id':'divMFNameScheme'})
mfoptions=mflocation.find_all("option")
mutual_funds=[y.text for y in mfoptions]
mutual_funds.pop(0)
mutual_funds.pop(0)


#xpath of mutual funds
xp_mutual_fund=[]
for i in range(len(mutual_funds)):
    xp_mutual_fund.append(f"//a[contains(text(),'{mutual_funds[i]}')]")
xp_mutual_fund.pop(26)
xp_mutual_fund[26] = "//li[27]//a[1]"
xp_mutual_fund.pop(0)







