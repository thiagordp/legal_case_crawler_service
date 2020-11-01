"""
JUSBrasil Crawler

@author Thiago Dal Pont
@data Oct 23, 2020
"""
import glob
import json
import os
import random
import time
from datetime import datetime, timedelta

import pandas as pd
import tqdm
from selenium import webdriver

from util.path_constants import DEST_DATASET_PATH
from util.utils import get_date_formatted, check_court
from util.value_path import BASE_URL_JUSBRASIL


class JusBrasilCrawler:
    def __init__(self, base_url_links="", items_per_page=250):
        self.base_url = base_url_links
        self.items_per_page = items_per_page

    def init_crawler(self):

        base_idtopico = 10000001

        global TRIBUNALS_PATH

        for id_topico in range(base_idtopico, base_idtopico + 300):
            TRIBUNALS_PATH = glob.glob(DEST_DATASET_PATH + "*")
            print("=" * 100)
            print("T" + str(id_topico))

            date_finish = datetime.today() + timedelta(days=-2)
            date_init = date_finish + timedelta(days=-0)

            driver = webdriver.Firefox()
            driver.minimize_window()

            for i in range(50000):
                str_date_init = get_date_formatted(date_init)
                str_date_finish = get_date_formatted(date_finish)

                print(str_date_init, "\t", str_date_finish)

                url = BASE_URL_JUSBRASIL.replace("@dateFrom", str_date_init)
                url = url.replace("@dateTo", str_date_finish)
                url = url.replace("@id_topico", "idtopico=T" + str(id_topico))

                self.crawl_interval(url, str_date_init + "_" + str_date_finish, "T" + str(id_topico))

                # Update dates
                date_finish = date_init + timedelta(days=-1)
                date_init = date_finish + timedelta(days=0)

                time.sleep(5)

    def crawl_interval(self, driver, url_interval, file_name, topico):

        data = []

        global TRIBUNALS_PATH

        errors = 0
        for page_i in tqdm.tqdm(range(1, 10001)):

            if errors > 3:
                # driver.close()
                driver.quit()

                driver = webdriver.Firefox()
                driver.minimize_window()

                errors = 0

            try:
                if random.random() < 0.00001:
                    driver.quit()

                    driver = webdriver.Firefox()
                    driver.minimize_window()
                    time.sleep(5)

                url = url_interval.replace("@page", str(page_i))
                driver.get(url)

                time.sleep((random.random()) * 4)

                # Get list of object from displayed documents

                doc_snippets_list = driver.find_elements_by_class_name("DocumentSnippet")

                if len(doc_snippets_list) == 0:
                    # print("No results found")
                    break

                for doc_snippet in doc_snippets_list:
                    aref_obj = doc_snippet.find_element_by_tag_name("a")
                    title = aref_obj.text

                    court = title.split()[0]
                    url = aref_obj.get_attribute("href")
                    data_publicacao = doc_snippet.find_element_by_class_name("BaseSnippetWrapper-highlight-date").text.split()[-1]

                    data.append([title, court, data_publicacao, url])

                    # self.get_document_content(title, url)

                time.sleep((random.random()) * 4)
                errors = 0
            except Exception as e:
                print("Error\t", e)

                errors += 1

                time.sleep(5 * (1 + random.random()))

        file_path = DEST_DATASET_PATH + topico

        TRIBUNALS_PATH = glob.glob(DEST_DATASET_PATH + "*")

        if not check_court(topico):
            try:
                os.mkdir(file_path)
                os.mkdir(file_path + "/links/")
                os.mkdir(file_path + "/cases/")
            except:
                pass

        df = pd.DataFrame(data=data, columns=["title", "court", "data_publicacao", "url"])

        for col in df:
            df[col] = df[col].str.replace(r'\\', '')

        # df.to_json(file_path + file_name + ".jsonl", orient='records', lines=True, force_ascii=False)

        list_parsed_dict = df.to_dict(orient="records")
        with open(file_path + "/links/" + file_name + ".jsonl", "w+") as f:
            for parsed_dict in list_parsed_dict:
                json.dump(parsed_dict, f, ensure_ascii=False)
                f.write("\n")

    def get_document_content(self, json_doc, driver=webdriver.Firefox(), output_path=""):

        url = json_doc["url"]
        driver.get(url)

        time.sleep(1)
        lens = list()
        unprint_objs = driver.find_elements_by_class_name("unprintable")

        texts = [l.text for l in unprint_objs]
        lens = [len(l.split()) for l in texts]
        ls = max(lens)

        text = texts[lens.index(ls)]

        # Get metadata

        metadata_group_obj = driver.find_element_by_class_name("DocumentPage-aside-content")

        metadata_obj_list = metadata_group_obj.find_elements_by_class_name("JurisprudenceDetails-group")

        for metadata_obj in metadata_obj_list:
            t = metadata_obj.text.split("\n")
            print(t)
            print("="*10)

        x = 0

