from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

class CowinSite:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.all_windows = []

    def boot(self):
        self.driver.get(self.url)
        self.original_window = self.driver.current_window_handle
        self.driver.maximize_window()
        self.all_windows.append(self.original_window)
        self.sleep(5)

    @staticmethod
    def sleep(seconds):
        sleep(seconds)

    def click_and_open_faq_new_tab(self):
        faq_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'FAQ')]")
        faq_link.click()
        sleep(5)  # Add a small delay to allow the new tab to open
        for window in self.driver.window_handles:
            if window != self.original_window and window not in self.all_windows:
                self.all_windows.append(window)

    def click_and_open_partners_new_tab(self):
        partners_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Partners')]")
        partners_link.click()
        sleep(5)  # Add a small delay to allow the new tab to open
        for window in self.driver.window_handles:
            if window != self.original_window and window not in self.all_windows:
                self.all_windows.append(window)

    def print_window_ids(self):
        print("Window/Frame IDs:")
        for window_id in self.all_windows:
            print(window_id)

    def close_new_tabs_and_return_to_home(self):
        for window in self.driver.window_handles:
            if window != self.original_window:
                self.driver.switch_to.window(window)
                self.driver.close()
        sleep(10)
        self.driver.switch_to.window(self.original_window)

url = "https://www.cowin.gov.in/"

# Instantiate CowinSite
cowin_site = CowinSite(url)

# Open the website
cowin_site.boot()

# Open new tab for FAQ
cowin_site.click_and_open_faq_new_tab()

# Open new tab for Partners
cowin_site.click_and_open_partners_new_tab()

# Print window/frame IDs
cowin_site.print_window_ids()

# Close new tabs and return to the home page
cowin_site.close_new_tabs_and_return_to_home()