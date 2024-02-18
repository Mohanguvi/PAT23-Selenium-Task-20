from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep


class CowinSite:
    """Class representing interactions with the Cowin website."""

    def __init__(self):
        """Initialize the CowinSite class."""
        self.url = "https://www.cowin.gov.in/"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.original_window = None

    def boot(self):
        """Method to boot up the Cowin website."""
        self.driver.get(self.url)
        self.original_window = self.driver.current_window_handle
        self.driver.maximize_window()
        sleep(5)

    def FAQ_tab_window_ID(self):
        """
        Method to click on a link, open FAQ in new tab, print the window ID.

        Parameters:
            The text of the link to be clicked.
        """
        link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'FAQ')]")
        link.click()
        sleep(5)
        # Switch to the second window handle (tab) in the list of window handles
        new_window = self.driver.window_handles[1]
        print(f"FAQ Window ID = {new_window}")
        return new_window

    def Partners_tab_window_ID(self):
        """
        Method to click on a link, Partners in new tab, print the window ID.

        Parameters:
            The text of the link to be clicked.
        """
        link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Partners')]")
        link.click()
        sleep(5)
        # Switch to the third window handle (tab) in the list of window handles
        new_window = self.driver.window_handles[2]
        print(f"Partners Window ID = {new_window}")
        return new_window

    def return_to_home(self):
        """Method to return to the home page."""
        self.driver.switch_to.window(self.original_window)

    def close_tab(self, window_id):
        """Method to close the tab with the specified window ID."""
        self.driver.switch_to.window(window_id)
        self.driver.close()
        self.driver.switch_to.window(self.original_window)

    def quit(self):
        """Method to quit the browser."""
        self.driver.quit()


# Main part of the script
if __name__ == "__main__":
    obj = CowinSite()  # Instantiate CowinSite
    obj.boot()  # Open the website
    main_window = obj.original_window
    faq_window = obj.FAQ_tab_window_ID()    # Open FAQ page in new tab, print window ID
    partners_window = obj.Partners_tab_window_ID()  # Open Partners page in new tab, print window ID
    obj.close_tab(partners_window)  # Close Partners tab
    sleep(5)
    obj.close_tab(faq_window)   # Close FAQ window
    sleep(5)
    obj.quit()  # Quit the browser

'''Output: 
            FAQ Window ID = 57F2C085A64A77AF7B4D08110DFF3805
            Partners Window ID = 6EEA494ADBF21857F86A33EDA35756D0'''
