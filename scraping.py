
# probably want to create fake account to login with
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from config import EMAIL, PASSWORD

def login(driver):
    # get login page
    driver.get("http://www.twitter.com/login")
    time.sleep(2)

    # save email and password field elements
    email = driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input')
    password = driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input')

    # enter email and password
    email.send_keys(EMAIL)
    password.send_keys(PASSWORD)
    password.send_keys(Keys.RETURN)

# This function currently does not get any emojis
def add_follower_info(i, df, driver):

    # Get follower name
    name = driver.find_element_by_xpath('''//*[@id="react-root"]
            /div/div/div/main/div/div/div/div/div/div[2]/
            section/div/div/div/div['''+str(i+1)+''']/div/div/
            div/div[2]/div[1]/div[1]/a/div/div[1]/div[1]/span''')
    name = name.text

    # Get follower username
    username = driver.find_element_by_xpath('''//*[@id="react-root"]
            /div/div/div/main/div/div/div/div/div/div[2]/
            section/div/div/div/div['''+str(i+1)+''']/div/div/
            div/div[2]/div[1]/div[1]/a/div/div[2]/div/span''')
    username = username.text

    # Try to get follower bio
    try:
        bio = driver.find_element_by_xpath('''//*[@id="react-root"]
                /div/div/div/main/div/div/div/div/div/div[2]/
                section/div/div/div/div['''+str(i+1)+''']/div/div/
                div/div[2]/div[2]''')
        # strip bio of newline chars
        bio = bio.text.replace('\n', ' ')

    # If no bio, initialize to empty string
    except:
        bio = ''

    # Append follower to df
    # Using df.loc to avoid duplicate entries
    finally:
        df.loc[username] = [name, bio]

        return df


# can get emoji unicode from urls, but having trouble converting to unicode
# print('hi there \U0001f62e')

# emoji1 = pass
# url = emoji1.get_attribute('src')
# emoji = url.split('/')[-1]
# emoji = emoji.split('.')[0]
## this part is causing an error
# emoji = '\U000'+emoji

def get_height(driver):
    height = driver.execute_script("return document.body.scrollHeight")
    return height

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

###################
## Main function ##
###################
## this gets a dataframe from scratch ##
## TODO haven't finished functionality to pass source csv file
def get_follower_info(username, source=None):
    if source == None:
        # Initializing dataframe
        df = pd.DataFrame()
        df['Name'] = []
        df['Bio'] = []
    else:
        df = pd.read_csv(source)

    # Opening browser
    driver = webdriver.Chrome()

    # Logging in
    login(driver)
    time.sleep(5)

    # Navigating to follower page
    driver.get("https://twitter.com/{}/followers".format(username))
    time.sleep(5)

    ## Scrolling down the page and scraping info along the way
    while True:
        for i in range(20):
            df = add_follower_info(i, df, driver)

        print("Total followers found: ", len(df))

        last_height = get_height(driver)
        scroll_down(driver) 
        time.sleep(2) 
        new_height = get_height(driver)  
        
        # If scrolling down hasn't changed the height of
        # the page, it's at the end
        if new_height == last_height:
            scroll_down(driver)    
            time.sleep(10)
            new_height = get_height(driver)
            if new_height == last_height:
                break

    driver.close()

    return df


# tip: right click on element in source code and copy xpath




# action = ActionChains(driver)
# action.move_to_element(follower_name).perform()

#Kumar Thangudu
# I love this for its uniqueness ability to specify parameters. Hugely useful!

# Adding this [crawly] to my running list of Scraping and Crawling Technologies!

# http://scrapinghub.com
# http://www.outwit.com/products/hub/
# http://webroots.io
# http://kimonolabs.com
# http://grabby.io
# http://fullcontact.com
# http://emailhunter.co
# http://clearbit.com
# http://toofr.com
# http://import.io
# http://kimonolabs.com
# http://apifier.com (my number one favorite)
# http://elink.club
# http://www.eliteproxyswitcher.com/ - ;)
# http://www.uipath.com/
# http://diffbot.com
# http://cloudscrape.com
# http://community.screen-scraper....
# https://commoncrawl.org/
# http://www.fminer.com/
# https://scraperwiki.com/
# http://nutch.apache.org/
# http://www.ubotstudio.com/index7
# http://mozenda.com
# http://fivefilters.org/


# credentials = {
#     "session[username_or_email]":"scottphuston@gmail.com",


#     }


# GET FREE PROXY LIST
 #### MOFIFY, DON'T USE TRANSPARENT PROXIES
## from https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/

# https://medium.com/ml-book/multiple-proxy-servers-in-selenium-web-driver-python-4e856136199d

# This also works:
# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
# req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
# proxies = req_proxy.get_proxy_list() #this will create proxy list
### Again, need to exit to not use transparent proxies


# import requests
# from lxml.html import fromstring
# def get_proxies():
#     url = 'https://free-proxy-list.net/'
#     response = requests.get(url)
#     parser = fromstring(response.text)
#     proxies = set()
#     # looks in top 10 results
#     for i in parser.xpath('//tbody/tr')[:10]:
#         # if Https = 'yes'
#         if i.xpath('.//td[7][contains(text(),"yes")]'):
#             #Grabbing IP and corresponding PORT
#             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
#             proxies.add(proxy)
#     return proxies



# _____________________________________
