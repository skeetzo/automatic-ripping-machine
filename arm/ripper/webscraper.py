#!/usr/bin/python3

import sys
sys.path.append("/opt/arm")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from threading import Timer

import time
import random
import sys
import re
import itertools
from colors import colorize
import args

AUTH_TIMEOUT = 60*2
DEBUG = args["debug"]
SHOW_WINDOW = args["showWindow"]
PRINTING = False
if int(args["verbose"]) > 0:
    PRINTING = True
DRIVER = False
URL = "https://www.wikipedia.com"
MAX_RESULTS = 10

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

class WebScraper:

    def __init__(self, url=URL):
        self.url = url
        self.browser = None
        self.tabs = []
        self.browserTimeout = False
        #
        self.spawn_browser()

    def go_to(self, url):
        try:
            url_ = str(self.browser.current_url).replace("http://www.", "")
            url__ = str(url).replace("http://www.", "")
            url_ = str(url_).replace("https://www.", "")
            url__ = str(url__).replace("https://www.", "")
            # print("{}  -  {}".format(self.browser.current_url, url))

            if str(url_) == str(url__) or str(url__) in str(url_):
                print("at -> {}".format(url__))
                self.browser.execute_script("window.scrollTo(0, 0);")

            elif self.search_for_tab("{}{}".format(ONLYFANS_HOME_URL, page)):
                print("found -> {}".format(page))
            else:
                print("goto -> {}".format(page))
                self.open_tab(url="{}{}".format(ONLYFANS_HOME_URL, page))
                self.browser.get(str(url))
                
                self.handle_alert()
                self.get_page_load()                

        except Exception as e:
            print("go to: {}".format(e))

    def search_for_tab(self, page):
        original_handle = self.browser.current_window_handle
        print("tabs: {}".format(self.tabs))
        try:
            for page_, handle, value in self.tabs:
                # print("{} = {}".format(page_, page))
                if str(page_) == str(page):
                    self.browser.switch_to_window(handle)
                    value += 1
                    print("successfully located tab in cache: {}".format(page))
                    return True
            for handle in self.browser.window_handles[0]:
                self.browser.switch_to_window(handle)
                if str(page) in str(self.browser.current_url):
                    print("successfully located tab: {}".format(page))
                    return True
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if str(page) in str(self.browser.current_url):
                    print("successfully located tab in windows: {}".format(page))
                    return True
            print("failed to locate tab: {}".format(page))
            self.browser.switch_to_window(original_handle)
        except Exception as e:
            if "Unable to locate window" not in str(e):
                print(e)
        return False

    def open_tab(self, url=None):
        if not url:
            Settings.err_print("Missing url")
            return False
        print("tab -> {}".format(url))
        # self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        # self.browser.get(url)
        # https://stackoverflow.com/questions/50844779/how-to-handle-multiple-windows-in-python-selenium-with-firefox-driver
        windows_before  = self.browser.current_window_handle
        print("Current Window Handle is : %s" %windows_before)
        windows = self.browser.window_handles
        self.browser.execute_script('''window.open("{}","_blank");'''.format(url))
        # self.browser.execute_script("window.open('https://www.yahoo.com')")
        WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(len(windows)+1))
        windows_after = self.browser.window_handles
        new_window = [x for x in windows_after if x not in windows][0]
        # self.browser.switch_to_window(new_window) <!---deprecated>
        self.browser.switch_to_window(new_window)
        print("Page Title after Tab Switching is : %s" %self.browser.title)
        print("New Window Handle is : %s" %new_window)
        if len(self.tabs) >= MAX_TABS:
            least = self.tabs[0]
            for i, tab in enumerate(self.tabs):
                if int(tab[2]) < int(least[2]):
                    least = tab
            self.tabs.remove(least)
        self.tabs.append([url, new_window, 0]) # url, window_handle, use count
        return True
    
    ######################################################################

    def search_metadata(title):
        # create search text from title
        # open firefox and go to url of search
        # get search result urls
        # open each url and check
        # if successful, i want to create a metadata.txt file
        # if failure, i want to create a metadata.txt file that uses the entered title as the updated album name
        pass

        def check_result(url_result):
            pass
            # returns true if correct page

        def parse_track_listing():
            pass
            # returns data

        def write_metadata(data):
            # create metadata.txt
            pass

        for result in url_results[:MAX_RESULTS]:
            if check_result(result):
                metadata = parse_track_listing()
                write_metadata(metadata)
                print("Successfully located metadata: more stuff")
                return

    def spawn_browser(self):      
        print("Spawning Browser")
        def firefox():
            try:
                from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                # options = webdriver.FirefoxOptions()
                # options.binary_location = "/usr/local/bin/geckodriver"
                # firefox needs non root
                d = DesiredCapabilities.FIREFOX
                opts = FirefoxOptions()
                d['loggingPrefs'] = {'browser': 'ALL'}
                opts.log.level = "trace"
                if not SHOW_WINDOW: opts.add_argument("--headless")
                # browser = webdriver.Firefox(options=opts, log_path='/var/log/onlysnarf/geckodriver.log')
                # browser = webdriver.Firefox(firefox_binary="/usr/local/bin/geckodriver", options=opts, capabilities=d)
                # browser = webdriver.Firefox(options=opts, desired_capabilities=d, log_path='/var/log/onlysnarf/geckodriver.log')
                browser = webdriver.Firefox(options=opts, desired_capabilities=d)
                browser = webdriver.Firefox(options=opts, capabilities=d, log_path='/var/log/bots/geckodriver.log')
                print("Spawned Browser - Firefox")
                return browser
            except Exception as e:
                Settings.warn_print("Missing Geckodriver")
                return False

        browser = firefox()
        if not browser: 
            print("Error: Unable to spawn browser")
            return False

        browser.implicitly_wait(30) # seconds
        browser.set_page_load_timeout(1200)
        print("Browser Spawned")
        self.browser = browser
        return True


    ################
    ##### Exit #####
    ################

    def exit(self):
        print("Exiting")
        if self.browser:
            self.browser.close()
            print("Browser Closed")
        self.browser = None

if __name__ == "__main__":

    url = URL
    bot = WebScraper()

    cd = None

    while True:
        try:
            bot.search(cd)
        except Exception:
            bot.exit()






logging.info("Starting DVD Movie Mainfeature processing")
logging.debug("Handbrake starting: " + str(job))
utils.SleepCheckProcess("HandBrakeCLI",int(job.config.MAX_CONCURRENT_TRANSCODES))
logging.debug("Setting job status to 'transcoding'")

db.session.commit()