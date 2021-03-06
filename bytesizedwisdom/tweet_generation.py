
## login to AIDungeon

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import EMAIL, PASSWORD

import pickle

#TODO write wrapper for finding elements with try/except blocks that wait longer

def get_by_xpath(driver, xpath, wait_cycles=5, sleep_time=5):
    """
    Wrapper for finding elements by xpath with try/except blocks that wait 
    longer if the element is not found
    """

    elem = None


    # TODO fix bug where it goes through all cycles before exiting
    # TODO specify which exception to catch
    for _ in range(wait_cycles):
        try:
            elem = driver.find_element_by_xpath(xpath)
        except:
            print(f'waiting {sleep_time} seconds')
            time.sleep(sleep_time)
        else:
            break
    
    return elem

def login(driver):

    # get login page
    driver.get("https://play.aidungeon.io/main/loginRegister")
    time.sleep(2)

    # go to login tab
    login_tab = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/div[1]/div[1]')
    login_tab.click()

    # save email and password field elements
    
    email = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/div[2]/input')
    password = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[1]/div[3]/input')

    # enter email and password
    email.send_keys(EMAIL)
    password.send_keys(PASSWORD)
    
    # click LOGIN
    login = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div[2]/div/div')
    login.click()

def navigate_to_scenario(driver, reset=False):
    if not reset:
        # This block is for a popup that comes up sometimes about updates to the site
        try:
            enter = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div/div')
            enter.click()
        except:
            # don't need to do anything
            pass

        open_menu = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div')
        open_menu.click()

        time.sleep(2) 

        my_stuff = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div[4]')
        my_stuff.click()

        time.sleep(2)

        scenarios = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[3]/div[1]')
        scenarios.click()

        time.sleep(4)

    else:
        back = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div')
        back.click()

    run_scenario = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[7]/div[3]/div[5]')
    run_scenario.click()

    time.sleep(10)

def generate_text(driver, extend_tweets=3):

    # retrying even the first response because it is generated by GPT-2 not GPT-3
    retry = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[3]/div[2]/div[8]')
    retry.click()

    time.sleep(10)

    # getting rid of a popup that comes up sometimes
    try:
        enter = get_by_xpath(driver, '/html/body/div[2]')
        enter.click()
    except:
        # don't need to do anything
        pass
    
    # clicking enter to generate more text
    for _ in range(extend_tweets):
        # getting rid of a poput pthat comes up sometimes
        try:
            x_out = get_by_xpath(driver, '/html/body/div[3]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div[3]')
            x_out.click()
        # TODO specify exception
        except:
            pass

        # generating more text
        text_entry = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[3]/div[3]/div/div/textarea')
        text_entry.send_keys(Keys.RETURN)
        time.sleep(10)
    
    time.sleep(10)

    # getting text
    text_div = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div[2]')
    full_text = text_div.text

    # stripping out prompt
    prompt = get_by_xpath(driver, '//*[@id="root"]/div/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div[2]/span[1]')
    prompt = prompt.text

    generated_text = full_text[len(prompt):]
    
    return generated_text

def parse_text(text):
    # seperate tweets
    tweets = text.split('\n---\n')
    
    # check length of each and strip leading and trailing spaces, tabs, and newlines
    for tweet in tweets:
        if len(tweet)>280:
            tweets.remove(tweet)
        elif len(tweet)==0:
            tweets.remove(tweet)
        else:
            tweet = tweet.lstrip()
            tweet = tweet.rstrip()

    return tweets

###### Main program ######
driver = webdriver.Chrome(ChromeDriverManager().install())

login(driver)
navigate_to_scenario(driver)

tweets = []

for i in range(10):
    if i != 0:
        navigate_to_scenario(driver, reset=True) # this is repetetive on the first run

    text = generate_text(driver)
    new_tweets = parse_text(text)
    tweets.extend(new_tweets)

# write tweets to file
with open('tweets.data', 'wb') as filehandle:
    pickle.dump(tweets, filehandle)
