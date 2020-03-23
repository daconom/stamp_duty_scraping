import requests
import time
import re
import traceback
import sys
import csv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from random import randint
from lxml import etree
from lxml.cssselect import CSSSelector

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=options)

#outFile= open('debtlist.csv', 'wt', encoding='utf8')
#nameFile= open('nameFile.csv', 'wt', encoding='utf8')
#ID_list=open('IDlist.csv', 'rt', encoding='utf8')

#Comment: importing ID list:
#for index, ID in enumerate(ID_list):
resp=browser.get('https://www.1000plus.am/en/search/mandatory')
time.sleep(1)
#Comment: For testing purposes, I use an arbitrary ID. Note that the IDs always need to have 8 digits (Just add a zero in the beginning)
ofn = "scraping_1000.csv"
#wt whipes the 
outFile = open(ofn, 'a', encoding='utf8')
outFile.write("ID;TIN_str;name;year;month;duty_amd;duty_usd\n")
with open('idlist.csv', 'r') as _idlist:
        id_list = csv.reader(_idlist)
        for id in id_list:
                time.sleep(3)
                browser.get('https://www.1000plus.am/en/search/mandatory')
                id_str="".join(id)
                ID = id_str.zfill(8) 
                if browser.find_elements_by_id("term_tax_code"):
                        browser.find_element_by_id("term_tax_code").send_keys(ID)
                        print("The current ID is %s" % ID)

                        #Submit
                        browser.find_element_by_xpath('//*[@id="mandatory-search-form"]/div/div[4]').click()
                        time.sleep(1.9)
                        if browser.find_elements_by_xpath("//*[@class='zebra-table-box']"):
                                box=browser.find_element_by_xpath("//*[@class='zebra-table-box']").get_attribute("innerText")
                                print(box)
                        if browser.find_elements_by_xpath("//*[@id='wrapper']/main/div[2]/div/div/table/tbody/tr[2]/td[4]/a"):
                                outFile = open(ofn, 'a', encoding='utf8')
                                time.sleep(1.2)
                                browser.find_element_by_xpath("//*[@id='wrapper']/main/div[2]/div/div/table/tbody/tr[2]/td[4]/a").click()
                                time.sleep(0.5)
                                tab = browser.find_elements_by_xpath("//*[@class='donation-title fs46 helvetica-neue-thin tc drop-down-title']")

                                years = browser.find_elements_by_xpath("//*[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-title fs46 helvetica-neue-thin tc drop-down-title']")
                                name =  browser.find_element_by_xpath("//*/td[@class='fs14'][1]").text

                                number_of_years=len(years)
                                if (number_of_years == 0):
                                        months= browser.find_elements_by_xpath("//div[@class='donation-box']/p[@class='donation-month fb fs20']")
                                        donations_amd= browser.find_elements_by_xpath("//div[@class='donation-list tc list ']/div[@class='donation-box']/div[@class='sum-list']/p[4]")
                                        donations_usd= browser.find_elements_by_xpath("//div[@class='donation-list tc list ']/div[@class='donation-box']/div[@class='sum-list']/p[1]")

                                        for j in range(len(months)):
                                                month=months[j].get_attribute("innerText") 
                                                donation_amd=donations_amd[j].get_attribute("innerText")
                                                donation_usd=donations_usd[j].get_attribute("innerText")
                                                test = "%s \t %s \t undefined \t %s \t %s \t %s" % (ID, name, month, donation_amd, donation_usd)
                                                print(test)
                                                outRow = "%s;%s;%s;undefined;%s;%s;%s\n" % (ID, id, name, month, donation_amd, donation_usd)
                                                outFile.write(outRow)  

                                for i in range(number_of_years):    
                                        year=years[i].text
                                        x = i+1
                                        months=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/p[@class='donation-month fb fs20']" % (x))
                                        donations_amd=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/div[@class='sum-list']/p[4]" % (x))
                                        donations_usd=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/div[@class='sum-list']/p[1]" % (x))
                                        for j in range(len(months)):
                                                month=months[j].get_attribute("innerText") 
                                                donation_amd=donations_amd[j].get_attribute("innerText")
                                                donation_usd=donations_usd[j].get_attribute("innerText")
                                                test = "%s \t %s \t %s \t %s \t %s \t %s" % (ID, name, year, month, donation_amd, donation_usd)
                                                print(test)
                                                outRow = "%s;%s;%s;%s;%s;%s;%s\n" % (ID, id, name, year, month, donation_amd, donation_usd)
                                                outFile.write(outRow)
                else:
                        time.sleep(600)
                        print("There was an Error 524 and we waited 10min. ID: %s" % (ID))
                        browser.get('https://www.1000plus.am/en/search/mandatory')
                        browser.find_element_by_id("term_tax_code").send_keys(ID)                     
                        #Submit
                        browser.find_element_by_xpath('//*[@id="mandatory-search-form"]/div/div[4]').click()
                        time.sleep(2)
                        if browser.find_elements_by_xpath("//*[@id='wrapper']/main/div[2]/div/div/table/tbody/tr[2]/td[4]/a"):
                                outFile = open(ofn, 'a', encoding='utf8')
                                time.sleep(1.2)
                                browser.find_element_by_xpath("//*[@id='wrapper']/main/div[2]/div/div/table/tbody/tr[2]/td[4]/a").click()
                                time.sleep(1)
                                tab = browser.find_elements_by_xpath("//*[@class='donation-title fs46 helvetica-neue-thin tc drop-down-title']")

                                years = browser.find_elements_by_xpath("//*[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-title fs46 helvetica-neue-thin tc drop-down-title']")
                                name =  browser.find_element_by_xpath("//*/td[@class='fs14'][1]").text

                                number_of_years=len(years)
                                print(number_of_years)
                                if (number_of_years == 0):
                                        months= browser.find_elements_by_xpath("//div[@class='donation-box']/p[@class='donation-month fb fs20']")
                                        donations_amd= browser.find_elements_by_xpath("//div[@class='donation-list tc list ']/div[@class='donation-box']/div[@class='sum-list']/p[4]")
                                        donations_usd= browser.find_elements_by_xpath("//div[@class='donation-list tc list ']/div[@class='donation-box']/div[@class='sum-list']/p[1]")

                                        for j in range(len(months)):
                                                month=months[j].get_attribute("innerText") 
                                                donation_amd=donations_amd[j].get_attribute("innerText")
                                                donation_usd=donations_usd[j].get_attribute("innerText")
                                                test = "%s \t %s \t %s \t %s \t %s \t %s" % (ID, name, month, donation_amd, donation_usd)
                                                print(test)
                                                outRow = "%s;%s;%s;undefined;%s;%s;%s\n" % (ID, id, name, month, donation_amd, donation_usd)
                                                outFile.write(outRow)  

                                for i in range(number_of_years):    
                                        year=years[i].text
                                        x = i+1
                                        months=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/p[@class='donation-month fb fs20']" % (x))
                                        donations_amd=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/div[@class='sum-list']/p[4]" % (x))
                                        donations_usd=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/div[@class='sum-list']/p[1]" % (x))
                                        for j in range(len(months)):
                                                month=months[j].get_attribute("innerText") 
                                                donation_amd=donations_amd[j].get_attribute("innerText")
                                                donation_usd=donations_usd[j].get_attribute("innerText")
                                                test = "%s \t %s \t %s \t %s \t %s \t %s" % (ID, name, year, month, donation_amd, donation_usd)
                                                print(test)
                                                outRow = "%s;%s;%s;%s;%s;%s;%s\n" % (ID, id, name, year, month, donation_amd, donation_usd)
                                                outFile.write(outRow)
                if (box == "The service is currently unavailable, please try later."):
                        time.sleep(100)
                        print("I slept 100s and will now try to use %s again" % (ID))
                        browser.get('https://www.1000plus.am/en/search/mandatory') 
                        browser.find_element_by_id("term_tax_code").send_keys(ID)
                        time.sleep(1)

                        #Submit
                        browser.find_element_by_xpath('//*[@id="mandatory-search-form"]/div/div[4]').click()
                        time.sleep(2)
                        if browser.find_elements_by_xpath("//*[@class='zebra-table-box']"):
                                box2=browser.find_element_by_xpath("//*[@class='zebra-table-box']").get_attribute("innerText")
                                print(box2)

                        if browser.find_elements_by_xpath("//*[@id='wrapper']/main/div[2]/div/div/table/tbody/tr[2]/td[4]/a"):
                                outFile = open(ofn, 'a', encoding='utf8')
                                time.sleep(1.2)
                                browser.find_element_by_xpath("//*[@id='wrapper']/main/div[2]/div/div/table/tbody/tr[2]/td[4]/a").click()
                                time.sleep(0.5)
                                tab = browser.find_elements_by_xpath("//*[@class='donation-title fs46 helvetica-neue-thin tc drop-down-title']")

                                years = browser.find_elements_by_xpath("//*[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-title fs46 helvetica-neue-thin tc drop-down-title']")
                                name =  browser.find_element_by_xpath("//*/td[@class='fs14'][1]").text

                                number_of_years=len(years)
                                if (number_of_years == 0):
                                        months= browser.find_elements_by_xpath("//div[@class='donation-box']/p[@class='donation-month fb fs20']")
                                        donations_amd= browser.find_elements_by_xpath("//div[@class='donation-list tc list ']/div[@class='donation-box']/div[@class='sum-list']/p[4]")
                                        donations_usd= browser.find_elements_by_xpath("//div[@class='donation-list tc list ']/div[@class='donation-box']/div[@class='sum-list']/p[1]")

                                        for j in range(len(months)):
                                                month=months[j].get_attribute("innerText") 
                                                donations_amd=donations_amd[j].get_attribute("innerText")
                                                donations_usd=donations_usd[j].get_attribute("innerText")
                                                test = "%s \t %s \t undefined \t %s \t %s \t %s" % (ID, name, month, donation_amd, donation_usd)
                                                print(test)
                                                outRow = "%s;%s;%s;undefined;%s;%s;%s\n" % (ID, id, name, month, donation_amd, donation_usd)
                                                outFile.write(outRow)  

                                for i in range(number_of_years):    
                                        year=years[i].text
                                        x = i+1
                                        months=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/p[@class='donation-month fb fs20']" % (x))
                                        donations_amd=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/div[@class='sum-list']/p[4]" % (x))
                                        donations_usd=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/div[@class='sum-list']/p[1]" % (x))
                                        for j in range(len(months)):
                                                month=months[j].get_attribute("innerText") 
                                                donation_amd=donations_amd[j].get_attribute("innerText")
                                                donation_usd=donations_usd[j].get_attribute("innerText")
                                                test = "%s \t %s \t %s \t %s \t %s \t %s" % (ID, name, year, month, donation_amd, donation_usd)
                                                print(test)
                                                outRow = "%s;%s;%s;%s;%s;%s;%s\n" % (ID, id, name, year, month, donation_amd, donation_usd)
                                                outFile.write(outRow)

                        if (box2 == "The service is currently unavailable, please try later."):
                                time.sleep(35)
                                print("I slept again for 35s and will try %s for the third time" % (ID))
                                browser.get('https://www.1000plus.am/en/search/mandatory') 
                                browser.find_element_by_id("term_tax_code").send_keys(ID)
                                time.sleep(1)

                                #Submit
                                browser.find_element_by_xpath('//*[@id="mandatory-search-form"]/div/div[4]').click()
                                time.sleep(2)
                                if browser.find_elements_by_xpath("//*[@class='zebra-table-box']"):
                                        box3=browser.find_element_by_xpath("//*[@class='zebra-table-box']").get_attribute("innerText")
                                        print(box3)
                                if browser.find_elements_by_xpath("//*[@id='wrapper']/main/div[2]/div/div/table/tbody/tr[2]/td[4]/a"):
                                        outFile = open(ofn, 'a', encoding='utf8')
                                        time.sleep(1.2)
                                        browser.find_element_by_xpath("//*[@id='wrapper']/main/div[2]/div/div/table/tbody/tr[2]/td[4]/a").click()
                                        time.sleep(0.5)
                                        tab = browser.find_elements_by_xpath("//*[@class='donation-title fs46 helvetica-neue-thin tc drop-down-title']")

                                        years = browser.find_elements_by_xpath("//*[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-title fs46 helvetica-neue-thin tc drop-down-title']")
                                        name =  browser.find_element_by_xpath("//*/td[@class='fs14'][1]").text

                                        number_of_years=len(years)
                                        if (number_of_years == 0):
                                                months= browser.find_elements_by_xpath("//div[@class='donation-box']/p[@class='donation-month fb fs20']")
                                                donations_amd= browser.find_elements_by_xpath("//div[@class='donation-list tc list ']/div[@class='donation-box']/div[@class='sum-list']/p[4]")
                                                donations_usd= browser.find_elements_by_xpath("//div[@class='donation-list tc list ']/div[@class='donation-box']/div[@class='sum-list']/p[1]")

                                                for j in range(len(months)):
                                                        month=months[j].get_attribute("innerText") 
                                                        donations_amd=donations_amd[j].get_attribute("innerText")
                                                        donations_usd=donations_usd[j].get_attribute("innerText")
                                                        test = "%s \t %s \t undefined \t %s \t %s \t %s" % (ID, name, month, donation_amd, donation_usd)
                                                        print(test)
                                                        outRow = "%s;%s;%s;undefined;%s;%s;%s\n" % (ID, id, name, month, donation_amd, donation_usd)
                                                        outFile.write(outRow)  

                                        for i in range(number_of_years):    
                                                year=years[i].text
                                                x = i+1
                                                months=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/p[@class='donation-month fb fs20']" % (x))
                                                donations_amd=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/div[@class='sum-list']/p[4]" % (x))
                                                donations_usd=browser.find_elements_by_xpath("//div[@class='popup-content pr donation-popup']/div[@class='donation-content drop-down']/div[@class='donation-list tc list  dn '][%d]/div[@class='donation-box']/div[@class='sum-list']/p[1]" % (x))
                                                for j in range(len(months)):
                                                        month=months[j].get_attribute("innerText") 
                                                        donation_amd=donations_amd[j].get_attribute("innerText")
                                                        donation_usd=donations_usd[j].get_attribute("innerText")
                                                        test = "%s \t %s \t %s \t %s \t %s \t %s" % (ID, name, year, month, donation_amd, donation_usd)
                                                        print(test)
                                                        outRow = "%s;%s;%s;%s,%s;%s;%s\n" % (ID, id, name, year, month, donation_amd, donation_usd)
                                                        outFile.write(outRow)  
print("Regular Finish")
browser.close()
