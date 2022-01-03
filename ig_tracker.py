import argparse
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="Instagram automation")
    # parser.add_argument('username', type=str, help='Instagram username')
    # parser.add_argument('password', type=str, help='Instagram password')
    parser.add_argument('-hl', '--headless', help="Run chrome webdriver in headless mode", action="store_true")
    args = parser.parse_args()
    # username = args.username
    # password = args.password
    if args.headless:
        headless = True
    else:
        headless = False

    chrome_options = webdriver.ChromeOptions()
    # Hide logging messages
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if headless:
        chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.instagram.com/")

    # Get username and password and enter them into login screen
    username = input("Enter Instagram username: ")
    password = input("Enter Instagram password: ")

    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()

    # Input 2FA code if user has one
    auth = input("Enter Instagram 2FA code (enter 'none' to skip): ")

    if auth != "none":
        driver.find_element_by_name('verificationCode').send_keys(auth)
        driver.find_element_by_tag_name('button').click()

    # Delay to allow everything to load
    time.sleep(5)

    # Get followers page
    driver.get("https://www.instagram.com/" + username)
    driver.find_element_by_partial_link_text('follower').click()
    #TODO -- maybe remove due to xpath dependency?
    pop_up_window = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))

    # Scroll through following list until it's all loaded
    last_height = driver.execute_script('return arguments[0].scrollTop',pop_up_window)
    while True:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',pop_up_window)
        time.sleep(1)
        new_height = driver.execute_script('return arguments[0].scrollTop',pop_up_window)
        if last_height == new_height:
            break
        last_height = driver.execute_script('return arguments[0].scrollTop',pop_up_window)

    # Get results and print
    followers_we = driver.find_elements_by_css_selector("a[class*='notranslate']")
    followers = []
    for i in followers_we:
        followers.append(i.text)
    for i in range(len(followers)):
        print(followers[i])



    # Get following page
    driver.get("https://www.instagram.com/" + username)
    driver.find_element_by_partial_link_text('following').click()
    #TODO -- maybe remove due to xpath dependency?
    pop_up_window = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))

    # Scroll through following list until it's all loaded
    last_height = driver.execute_script('return arguments[0].scrollTop',pop_up_window)
    while True:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',pop_up_window)
        time.sleep(1)
        new_height = driver.execute_script('return arguments[0].scrollTop',pop_up_window)
        if last_height == new_height:
            break
        last_height = driver.execute_script('return arguments[0].scrollTop',pop_up_window)

    # Get results and print
    following_we = driver.find_elements_by_css_selector("a[class*='notranslate']")
    following = []
    for i in following_we:
        following.append(i.text)
    for i in range(len(following)):
        print(following[i])


    # Compare the two lists
    print()
    not_following_them_back = np.setdiff1d(followers, following)
    print("Not following them back:")
    print(not_following_them_back)
    not_following_me_back = np.setdiff1d(following, followers)
    print("Not following me back:")
    print(not_following_me_back)
