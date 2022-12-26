from selenium import webdriver
from selenium.webdriver.common.by import By
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

#service = ChromeService(executable_path=ChromeDriverManager().install())
USER_NAME = "haoanhtran7@gmail.com"
PASSWORD = "Happyman7"

driver = webdriver.Chrome(r"C:\Users\haoan\programing\python\projects\selenium\chromedriver")

driver.get("https://www.myfitnesspal.com/account/login")
driver.implicitly_wait(10)

#LOGIN SCRIPT 
usernameForm = driver.find_element(By.ID, "email")
passwordForm = driver.find_element(By.ID, "password")

usernameForm.send_keys(USER_NAME)
passwordForm.send_keys(PASSWORD)

buttons = driver.find_elements(By.TAG_NAME, "button")
for button in buttons: 
    if button.get_attribute("type") == "submit": 
        button.submit()

#ADD FOOD
time.sleep(5)
title = driver.current_url
print(title)


wait = WebDriverWait(driver, 10)
desired_url = "https://www.myfitnesspal.com"
wait.until(EC.title_is(desired_url))


