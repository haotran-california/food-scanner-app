from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
from PIL import Image
import requests
import io
import time
import os 

class Parser: 
    def __init__(self):
        self.url = "https://nutrition.sa.ucsc.edu/"
        #self.browser = webdriver.Chrome("/home/hao/Documents/Personal/python/projects/selenium/chromedriver")
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.dinngHallList = ["College Nine/John R. Lewis Dining Hall", "Cowell/Stevenson Dinning Hall", "Crown/Merrill Dinning Hall", "Porter/Kresge Dinning Hall", "Oakes Cafe", "Global Village Cafe", "Stevenson Coffee House", "Porter Market", "Perk Coffee Bars"]
        self.data = {}
        self.conn = None

    def load(self):
        self.browser.get(self.url)
        self.browser.implicitly_wait(5)

    def selectDinningHall(self, name): 
        links = self.browser.find_elements(By.TAG_NAME,"a")
        for link in links:
            print(link.text) 
            if link.text == name: 
                print("Found it")
                link.click()
                break

    def loadDateQuery(self): 
        select = Select(self.browser.find_element(By.TAG_NAME, "select"))
        lastOption = select.options[-1]
        #lastOption.click()
 
        #inputs = self.browser.find_elements(By.TAG_NAME, "input")
        #for input in inputs:  
        #    if input.get_attribute("value") == "Go!": 
        #        input.submit()
        #        break
        
        self.url += lastOption.get_attribute("value") 
        self.load()

    def loadQuery(self, day, month, year): 
        query = self.browser.current_url
        querySplit = query.split("=")
        newDate = str(month) + "%2f" + str(day) + "%2f" + str(year)
        querySplit[-1] = newDate
        newQuery = "".join([x + "=" for x in querySplit])
        print(newQuery)
        self.url = newQuery[0:len(newQuery)-1]
        self.load()
    

    def openMenu(self, option): 
        links = self.browser.find_elements(By.TAG_NAME, "a")
        link = None
        if option == "Breakfast": 
            link = links[2]
        elif option == "Lunch": 
            link = links[3]
        elif option == "Dinner": 
            link = links[4]
        elif option == "Late Night": 
            link = link[5]

        link.click()

    def setMenu(self): 
        inputsQTY = self.browser.find_elements(By.NAME, "QTY")
        for input in inputsQTY:
            input.send_keys(1) 

        inputs = self.browser.find_elements(By.TAG_NAME, "input")
        for input in inputs: 
            if input.get_attribute("value") == "Show Nutrition Report": 
                input.click()
                break 
            
    #def parseMenu(self): 
    #    menuList = []

    #    #spans = self.browser.find_elements(By.TAG_NAME, "span")
    #    #for span in spans: 
    #    #    if span.text != "": 
    #    #        menuItems.append(span.text)
    #    
    #    menuItems = self.browser.find_elements(By.XPATH, "//div[@class='shortmenurecipes']/span[1]")
    #    for item in menuItems: 
    #        menuList.append(item.text)

    #    print(menuList)
    #    return menuList 

    def parseMenu(self): 
        menuItems = []
        menuP = []
        menuCals = []
        menuCarbs = []
        menuProteins = []
        menuFats = []
        
        itemNames = self.browser.find_elements(By.TAG_NAME, "a")
        for item in itemNames: 
            #self.data[item.text] = self.data.get(item.text, (0, 0, 0, 0))
            menuItems.append(item.text)

        itemP = self.browser.find_elements(By.CLASS_NAME, "nutrptportions")
        for p in itemP: 
            menuP.append(p.text)

        itemValues = self.browser.find_elements(By.CLASS_NAME, "nutrptvalues")
        count = 0
        for val in itemValues: 
            count += 1 
            if count % 5 == 1: 
                menuCals.append(val.text)
                continue 
            elif count % 5 == 2:  
                menuProteins.append(val.text)
                continue 
            elif count % 5 == 3:
                menuCarbs.append(val.text)
                continue 
            elif count % 5 == 0: 
                menuFats.append(val.text)
                continue
            else: 
                continue 
        
        n = len(menuItems)
        for i in range(n): 
            data = (menuItems[i], menuP[i], menuCals[i], menuCarbs[i], menuProteins[i], menuFats[i])
            self.insertDB(data)
                

    def createDBConnection(self): 
        BASE = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(BASE, "database.db")
        self.conn = sqlite3.connect(DB_PATH)
        print("Created DB Connection")
        

    def insertDB(self, dataTuple): 
        sql =  ''' INSERT INTO AllFood (name, proportions, calories, carbs, proteins, fats)
                VALUES(?, ?, ?, ?, ?, ?)  '''

        cur = self.conn.cursor()
        cur.execute(sql, dataTuple)
        self.conn.commit()
        return cur.lastrowid

parser = Parser()
parser.createDBConnection()
parser.load()
parser.selectDinningHall("Cowell/Stevenson Dining Hall")
parser.loadDateQuery()
parser.loadQuery(24, 10, 2022)
parser.openMenu("Lunch")
parser.setMenu()
parser.parseMenu()
print("DONE")
time.sleep(100)

#parser.browser.quit()

