import os
from selenium import webdriver
import time
from variables import *
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
#changing default downloading dir                                       #write download directory here
preferences = {"download.default_directory": r"C:\Users\Harshit Bansal\PycharmProjects\seleniumScraping"}
options.add_experimental_option("prefs", preferences)
driver = webdriver.Chrome(options=options)
driver.get("https://www.amfiindia.com/ter-of-mf-schemes") #web address

#solve: used for downloading and renaming .xls files
def solve(name,year,month,type,cat_subcat):
    try:
        #for clicking xls icon
        ter = WebDriverWait(driver, 5).until(
            lambda x: x.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[6]/div[1]/form/input[2]"))
        ter.click()
        #Diff Time because "All" files are larger in size and takes more time to rename. So to prevent cascading effect "All" files are renamed in 2 seconds and other are renamed in 1 second
        if(name=='All'):
            time.sleep(2)
        else:
            time.sleep(1)
        for filename in os.listdir():
            try:
                if filename.startswith("AMFI"):
                    #all downloaded files start with "amfi", so this is finding a file with "amfi" in it and is renaming it according to arguments of function
                    currName = filename
                    newName=f"{name}#{year}${month}%{type}_{cat_subcat}.xls"
                    os.rename(currName, newName)
            except:
                #if os is unable to rename a file it will remove the file so that it doesn't cause problem with further downloads
                print("unable to rename")
                os.remove(filename)
    except:
        #when no file is present for current values
        print("NO DATA")


#iterating through a particular mf
for i in range(len(xp_mutual_fund)):
    try:
        #xpath of mf dropdown icon
        driver.find_element_by_xpath("//div[6]//span[1]//a[1]//span[2]").click()
        #xpath of particular mf
        driver.find_element_by_xpath(xp_mutual_fund[i]).click()
        #time.sleep so that webpage can load properly after selecting an item
        time.sleep(0.5)
    except:
        #bypass any errors because we don't want to stop whole process
        continue
    #iterating through year
    for j in range(len(year)):
        try:
            #xpath of year dropdown
            driver.find_element_by_xpath("//div[@id='divFinTER']//span[@class='ui-button-text']").click()
            #xpath of selecting year. Year list is defined in variable.py
            driver.find_element_by_xpath(f"//a[contains(text(),'{year[j]}')]").click()
            time.sleep(0.5)
        except:
            continue
        #iterating through months
        for k in range(len(month_dictionary[year[j]])):
            try:
                #xpath of month dropdown
                driver.find_element_by_xpath("//div[@class='common-content']//div[2]//span[1]//a[1]//span[2]").click()
                #xpath for selecting month
                driver.find_element_by_xpath(f"//a[contains(text(),'{month_dictionary[year[j]][k]}')]").click()
                time.sleep(0.5)
            except:
                continue
            for l in range(len(dummy1)):
                #for l=0 we have 6 fields and for l=1,2 we have 5 fields.. so we will deal both cases separately because components are dynamic
                #l=0 open ended
                #l=1 interval Fund
                #l=2 close ended
                #look at variable.py typeOfMF to understantand scheme structure
                if(l==0):
                    try:
                        driver.find_element_by_xpath("//div[@id='divNav']//span[@class='ui-button-text']").click()
                        driver.find_element_by_xpath("//a[contains(text(),'Open Ended')]").click()
                        time.sleep(0.5)
                    except:
                        continue
                    for m in range(len(dummy2)):
                        #dummy2=['Debt Scheme','Equity Scheme','Hybrid Scheme','Other Scheme','Solution Oriented Scheme']
                        try:
                            driver.find_element_by_xpath("//div[@id='divMFScheme']//span[@class='ui-button-text']").click()
                            driver.find_element_by_xpath(f"//a[contains(text(),'{dummy2[m]}')]").click()
                            time.sleep(0.5)
                        except:
                            continue
                        for n in range(len(typeOfMF[dummy1[l]][dummy2[m]])):
                            #finding xpaths with using 'contains' cause problem because many schemes have common name like short duration fund and ultra short duration fund. So these cases are dealt separately
                            try:
                                driver.find_element_by_xpath("//div[@id='divSubSchemeComp']//span[@class='ui-button-text']").click()
                            except:
                                continue
                            #we are taking if statements here because for these elements, xpath of values changes. Xpath gets confused when we use contains.. because some schemes have common string
                            if (typeOfMF[dummy1[l]][dummy2[m]][n] == 'Short Duration Fund'):
                                try:
                                    driver.find_element_by_xpath("//ul[6]//li[7]//a[1]").click()
                                    time.sleep(0.5)
                                    driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                                    time.sleep(1)
                                    solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],'Debt Scheme_Short Duration Fund')
                                    continue
                                except:
                                    continue
                            if (typeOfMF[dummy1[l]][dummy2[m]][n] == 'Long Duration Fund'):
                                try:
                                    driver.find_element_by_xpath("//ul[6]//li[10]//a[1]").click()
                                    time.sleep(0.5)
                                    driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                                    time.sleep(1)
                                    solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],'Debt Scheme_Long Duration Fund')
                                    continue
                                except:
                                    continue

                            if (typeOfMF[dummy1[l]][dummy2[m]][n] == 'Mid Cap Fund'):
                                try:
                                    driver.find_element_by_xpath("//ul[6]//li[5]//a[1]").click()
                                    time.sleep(0.5)
                                    driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                                    time.sleep(1)
                                    solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],'Equity Scheme_Mid Cap Fund')
                                    continue
                                except:
                                    continue
                            #this will run when there is no confusion between xpaths containing same string
                            if(typeOfMF[dummy1[l]][dummy2[m]][n]!='Short Duration Fund' or typeOfMF[dummy1[l]][dummy2[m]][n]!='Long Duration Fund' or typeOfMF[dummy1[l]][dummy2[m]][n]!='Mid Cap Fund' ):
                                try:
                                    driver.find_element_by_xpath(f"//a[contains(text(),'{typeOfMF[dummy1[l]][dummy2[m]][n]}')]").click()
                                    time.sleep(0.5)
                                    driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                                    time.sleep(1)
                                    solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],f"{dummy2[m]}_{typeOfMF[dummy1[l]][dummy2[m]][n]}")
                                    continue
                                except:
                                    continue


                if(l!=0):
                    # l=1 interval Fund
                    # l=2 close ended
                    #for interval fund and close ended
                    try:
                        driver.find_element_by_xpath("//div[@id='divNav']//span[@class='ui-button-text']").click()
                        driver.find_element_by_xpath(f"//a[contains(text(),'{dummy1[l]}')]").click()
                        time.sleep(0.5)
                    except:
                        continue
                    for m in range(len(typeOfMF[dummy1[l]])):
                        #iterating through subSchemes for common value of l.
                        try:
                            driver.find_element_by_xpath("//div[@id='divSubSchemeComp']//span[@class='ui-button-text']").click()
                            time.sleep(0.5)
                            driver.find_element_by_xpath(f"//a[contains(text(),'{typeOfMF[dummy1[l]][m]}')]").click()
                            time.sleep(0.5)
                            driver.find_element_by_xpath("//a[@id='hrfGo']").click()
                            time.sleep(1)
                            solve(mutual_funds[i],year[j],month_dictionary[year[j]][k],dummy1[l],f"{typeOfMF[dummy1[l]][m]}")
                        except:
                            continue

