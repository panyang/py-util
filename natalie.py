from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

def login(driver, email, password):
    page = "https://accounts.google.com"
    driver.get(page)
    email_box = WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((By.ID, "Email")))
    email_box.send_keys(email)
    next_button = driver.find_element_by_id("next")
    next_button.click()

    password_box = WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((By.ID, "Passwd")))
    password_box.send_keys(password)
    signIn_button = driver.find_element_by_id("signIn")
    signIn_button.click()
    WebDriverWait(driver, 10).until(
        expected_conditions.invisibility_of_element_located((By.ID, "signIn")))
        
if __name__ == "__main__":
    browser = webdriver.Chrome()
    #login(browser, "baoshengvisa2013@gmail.com", "Praisethelord2013")
    #login(browser, 'pic.bo.zhi@gmail.com', '20030810')
    login(browser, "kellybosong@gmail.com", "Phd2012!")
    #login(browser, "zhi.han@gmail.com", "2012Math!")
    browser.get("https://www.youtube.com/watch?"
                "v=VgRtt02Bk7g"
                "&list=PLPbWBWC5Faw2PeTdWnAKgxvNIM6yEphD0")
    time.sleep(3600) # seconds
    browser.close()

    
