from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
from time import sleep


class LabourWebsite:
    """Class for automating tasks on the Labour website."""

    def __init__(self, url):
        """
        Constructor to initialize the LabourWebsite class.

        Parameters:
        url (str): The URL of the Labour website.
        """
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.action = ActionChains(self.driver)

    def boot(self):
        """Function to navigate to the Labour website and maximize the window."""
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.wait(5)

    def wait(self, secs):
        """
        Function to pause script execution for a specified number of seconds.

        Parameters:
        secs (int): The number of seconds to wait.
        """
        sleep(secs)

    def quit(self):
        """Function to quit the Chrome WebDriver."""
        self.driver.quit()

    def findElementByXPATH(self, Xpath):
        """
        Function to find an element by XPath.

        Parameters:
        Xpath (str): The XPath of the element to find.

        Returns:
        WebElement: The found element.
        """
        return self.driver.find_element(by=By.XPATH, value=Xpath)

    def close_banner(self):
        """Function to close a banner if it is on a webpage."""
        popup_close_button = self.findElementByXPATH('/html/body/div[1]/div[3]/div/div[2]/button')
        if popup_close_button:
            popup_close_button.click()
            self.wait(3)
            print("Banner closed successfully")
        else:
            print("No Banner found")

    def go_to_monthly_progross_report(self):
        """Function to navigate to the monthly progress report page."""
        self.boot()
        self.close_banner()
        self.wait(2)
        try:
            # Hover to menu and click the documents to open sub menu
            documents_menu = self.findElementByXPATH('//*[@id="nav"]/li[7]')
            self.action.move_to_element(documents_menu).perform()
            self.wait(3)
            # Navigating to the monthly progress page
            self.findElementByXPATH('//*[@id="nav"]/li[7]/ul/li[2]').click()
            self.wait(5)
        except Exception as e:
            print(f"Error navigating to monthly progress report: {e}")

    def download_report(self):
        """Function to download a report by fetch the url of the document."""
        try:
            self.findElementByXPATH(
                '/html/body/section[3]/div/div/div[3]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[2]/a'
            ).click()
            self.wait(2)
            if EC.alert_is_present()(self.driver): # Accept if any alert button is present
                alert = self.driver.switch_to.alert
                alert.accept()
                self.wait(3)
            else:
                # Wait for the button to be clickable
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "button"))).click()
        except Exception as e:
            print("Error while navigating to monthly progress report:", e)
            print("Error while downloading report:", e)
        finally:
            self.driver.switch_to.window(self.driver.window_handles[-1]) # switch to document window
            document_url = self.driver.current_url      # fetch the url of the document page
            response = requests.get(document_url)
            if response.status_code == 200:
                filepath = "Latest_monthly_Progress_Report.pdf"
                with open(filepath, "wb") as f:     # open the file get the content and write in the pdf file.
                    f.write(response.content)
                    print("Report downloaded successfully")
            else:
                print("Error downloading report")
            self.driver.close()     # Close the document page
            self.driver.switch_to.window(self.driver.window_handles[0]) # switch to the home page
            self.wait(3)
            self.driver.back()   # Go back to the home page
            self.wait(5)

    def go_to_photo_gallery(self):
        """Function to navigate to the photo gallery page."""
        self.close_banner()
        self.wait(2)
        try:

            # Hover over the Media menu and click on the Photo Gallery page
            documents_menu = self.findElementByXPATH('//*[@id="nav"]/li[10]')
            self.action.move_to_element(documents_menu).perform()
            self.wait(3)
            # Navigating to the photo gallery page
            self.findElementByXPATH('//*[@id="nav"]/li[10]/ul/li[2]').click()
            self.wait(5)
        except Exception as e:
            print(f"Error navigating to Photo gallery: {e}")

    def download_photos(self):
        """Function to download photos from the photo gallery."""
        
        self.wait(5)
        for i in range(1, 11):
            image_xpath = f'//*[@id="fontSize"]/div/div/div[3]/div[2]/div[1]/div/div/div[2]/div[2]/table/tbody/tr[{i}]/td[3]/div[1]/div/img'
            url = self.findElementByXPATH(image_xpath).get_attribute('src')
            print("Image URL is :", url)
            response = requests.get(url)
            if response.status_code == 200:
                filePath = f"Labour_Photos/image {i}.jpg"
                f = open(filePath, 'wb')
                f.write(response.content)
                f.close()
            else:
                print("Error downloading the images")


if __name__ == "__main__":
    url = "https://labour.gov.in/"
    obj = LabourWebsite(url)
    obj.go_to_monthly_progross_report()
    obj.download_report()
    obj.go_to_photo_gallery()
    obj.download_photos()
    obj.quit()
