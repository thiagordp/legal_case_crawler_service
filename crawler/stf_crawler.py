"""


"""
import os
import random
import time
from datetime import timedelta, datetime

from pyautogui import hotkey
from selenium import webdriver

from util.path_constants import DEST_DATASET_PATH
from util.utils import get_date_formatted, check_court
from util.value_path import XPATH_PROC, XPATH_INTEIRO_TEOR


class StfCrawler:

    def __init__(self, base_url, limit_date, items_per_page=250):
        self.base_url = base_url
        self.limit_date = limit_date
        self.items_per_page = items_per_page

    def init_crawler(self):

        if not check_court("STF"):
            os.mkdir(DEST_DATASET_PATH + "stf/")

        date_finish = datetime.today()

        date_init = date_finish + timedelta(days=-7)

        driver = webdriver.Firefox()
        driver.minimize_window()

        for i in range(50):

            if (date_init - self.limit_date).total_seconds() < 0:
                break

            str_date_init = get_date_formatted(date_init, separator="", reverse=False)
            str_date_finish = get_date_formatted(date_finish, separator="", reverse=False)

            print(str_date_init, "\t", str_date_finish)

            url = self.base_url.replace("@dateFrom", str_date_init)
            url = url.replace("@dateTo", str_date_finish)
            url = url.replace("@items_per_page", str(self.items_per_page))

            self._crawl_interval(driver, url, self.items_per_page)

            # Update dates
            date_finish = date_init + timedelta(days=-1)
            date_init = date_finish + timedelta(days=-7)

            time.sleep(2)

    def _crawl_interval(self, driver, url_interval, items_per_page):
        if random.random() < 0.05:
            driver.close()
            driver.quit()

            driver = webdriver.Firefox()
            driver.minimize_window()

        # delay = 3  # seconds
        # try:
        #     myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        #     print("Page is ready!")
        # except TimeoutException:
        #     print("Loading took too much time!")
        # Get list of object from displayed documents

        for i in range(1, 300):
            try:
                final_url = url_interval.replace("@page", str(i))
                driver.get(final_url)

                for proc_j in range(items_per_page):
                    proc_obj = driver.find_element_by_xpath(XPATH_PROC.replace("@index", str(i)))

                    inteiro_teor_obj = proc_obj.find_element_by_xpath(XPATH_INTEIRO_TEOR)

                    # Continuar aqui
                    # Capturar ao mesmo tempo o metadado e o arquivo PDF
                    inteiro_teor_obj.click()

                    hotkey('ctrl', 's')
                    hotkey('enter')
                    time.sleep(1)

            except:
                break
            finally:
                time.sleep(10)

    def get_document_content(self, title, url):
        pass
