from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

class CowinSite:     # Class for Cowinsite to perform and call the action
    def __init__(self, url):    # Constructor method to initiate the process
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.all_windows = []

    def boot(self):    # Boot function to access the website
        self.driver.get(self.url)
        self.original_window = self.driver.current_window_handle
        self.driver.maximize_window()
        self.all_windows.append(self.original_window)
        self.sleep(5)

    @staticmethod
    def sleep(seconds):    # Sleep function to delay each processs
        sleep(seconds)

    def faq_new_tab(self):    # Function to open the FAQ to open in new tab
        faq_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'FAQ')]")
        faq_link.click()
        sleep(5)
        for window in self.driver.window_handles:    # To open in a new window from the original window
            if window != self.original_window and window not in self.all_windows:
                self.all_windows.append(window)

    def partners_new_tab(self):    # Function to open the partners to open in new tab
        partners_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Partners')]")
        partners_link.click()
        sleep(5)
        for window in self.driver.window_handles:    ## To open in a new window from the original window
            if window != self.original_window and window not in self.all_windows:
                self.all_windows.append(window)

    def window_id(self):    # Function to achieve the window ID
        print("Window/Frame IDs:")
        for window_id in self.all_windows:
            print(window_id)

    def close_return_to_home(self):    # Function to close the new tab and get to the home window
        for window in self.driver.window_handles:
            if window != self.original_window:
                self.driver.switch_to.window(window)
                self.driver.close()
        sleep(10)
        self.driver.switch_to.window(self.original_window)

url = "https://www.cowin.gov.in/"

cowin_site = CowinSite(url)        # Instantiate CowinSite
cowin_site.boot()                # Open the website
cowin_site.faq_new_tab()        # Open new tab for FAQ
cowin_site.partners_new_tab()    # Open new tab for Partners
cowin_site.window_id()            # Print window/frame IDs
cowin_site.close_return_to_home()    # Close new tabs and return to the home page
