import os
from selenium import webdriver
import time
from variables import *
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
                                                        #write download directory here
preferences = {"download.default_directory": r"C:\Users\Harshit Bansal\PycharmProjects\seleniumScraping"}
options.add_experimental_option("prefs", preferences)
driver = webdriver.Chrome(options=options)
driver.get("https://www.amfiindia.com/ter-of-mf-schemes")


def solve(name,year,month,type,cat_subcat):
    try:
        ter = WebDriverWait(driver, 5).until(
            lambda x: x.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[6]/div[1]/form/input[2]"))
        ter.click()
        if(name=='All'):
            time.sleep(2)
        else:
            time.sleep(1)
        for filename in os.listdir():
            if filename.startswith("AMFI"):
                currName = filename
                newName=f"{name}_{year}_{month}_{type}_{cat_subcat}.xls"
                os.rename(currName, newName)

    except:
        print("NO DATA")



for i in range(len(xp_mutual_fund)):
    driver.find_element_by_xpath("//div[6]//span[1]//a[1]//span[2]").click()
    driver.find_element_by_xpath(xp_mutual_fund[i]).click()
    time.sleep(0.5)

    for j in range(len(year)):
        driver.find_element_by_xpath("//div[@id='divFinTER']//span[@class='ui-button-text']").click()
        driver.find_element_by_xpath(f"//a[contains(text(),'{year[j]}')]").click()
        time.sleep(0.5)

        for k in range(len(month_dictionary[year[j]])):
            driver.find_element_by_xpath("//div[@class='common-content']//div[2]//span[1]//a[1]//span[2]").click()
            driver.find_element_by_xpath(f"//a[contains(text(),'{month_dictionary[year[j]][k]}')]").click()
            time.sleep(0.5)

            for l in range(len(dummy1)):
                if(l==0):
                    driver.find_element_by_xpath("//div[@id='divNav']//span[@class='ui-button-text']").click()
                    driver.find_element_by_xpath("//a[contains(text(),'Open Ended')]").click()
                    time.sleep(0.5)
                    for m in range(len(dummy2)):
                        driver.find_element_by_xpath("//div[@id='divMFScheme']//span[@class='ui-button-text']").click()
                        driver.find_element_by_xpath(f"//a[contains(text(),'{dummy2[m]}')]").click()
                        time.sleep(0.5)
                        for n in range(len(typeOfMF[dummy1[l]][dummy2[m]])):
                            driver.find_element_by_xpath("//div[@id='divSubSchemeComp']//span[@class='ui-button-text']").click()
                            if (typeOfMF[dummy1[l]][dummy2[m]][n] == 'Short Duration Fund'):
                                driver.find_element_by_xpath("//ul[6]//li[7]//a[1]").click()
                                time.sleep(0.5)
                                driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                                time.sleep(1)
                                solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],'Debt Scheme_Short Duration Fund')
                                continue
                            if (typeOfMF[dummy1[l]][dummy2[m]][n] == 'Long Duration Fund'):
                                driver.find_element_by_xpath("//ul[6]//li[10]//a[1]").click()
                                time.sleep(0.5)
                                driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                                time.sleep(1)
                                solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],'Debt Scheme_Long Duration Fund')
                                continue
                            if (typeOfMF[dummy1[l]][dummy2[m]][n] == 'Mid Cap Fund'):
                                driver.find_element_by_xpath("//ul[6]//li[5]//a[1]").click()
                                time.sleep(0.5)
                                driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                                time.sleep(1)
                                solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],'Equity Scheme_Mid Cap Fund')
                                continue
                            if(typeOfMF[dummy1[l]][dummy2[m]][n]!='Short Duration Fund' or typeOfMF[dummy1[l]][dummy2[m]][n]!='Long Duration Fund' or typeOfMF[dummy1[l]][dummy2[m]][n]!='Mid Cap Fund' ):
                                driver.find_element_by_xpath(f"//a[contains(text(),'{typeOfMF[dummy1[l]][dummy2[m]][n]}')]").click()
                                time.sleep(0.5)
                                driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                                time.sleep(1)
                                solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],f"{dummy2[m]}_{typeOfMF[dummy1[l]][dummy2[m]][n]}")
                                continue


                if(l!=0):
                    driver.find_element_by_xpath("//div[@id='divNav']//span[@class='ui-button-text']").click()
                    driver.find_element_by_xpath(f"//a[contains(text(),'{dummy1[l]}')]").click()
                    time.sleep(2)
                    for m in range(len(typeOfMF[dummy1[l]])):
                        driver.find_element_by_xpath("//div[@id='divSubSchemeComp']//span[@class='ui-button-text']").click()
                        time.sleep(0.5)
                        driver.find_element_by_xpath(f"//a[contains(text(),'{typeOfMF[dummy1[l]][m]}')]").click()
                        time.sleep(0.5)
                        driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                        time.sleep(1)
                        solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],f"{typeOfMF[dummy1[l]][m]}")


