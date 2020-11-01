"""

"""
import glob
import json
import os
import random
import time
from datetime import datetime, timedelta

import tqdm
from selenium import webdriver

from crawler.jusbrasil_crawler import JusBrasilCrawler
from util.path_constants import DEST_DATASET_PATH
from util.utils import get_date_formatted
from util.value_path import TOPICOS_COURTS, BASE_URL_JUSBRASIL


def crawler_collect_links():
    initial_date = datetime.strptime("31/12/2010", '%d/%m/%Y')
    limit_date = datetime.strptime("01/01/2009", '%d/%m/%Y')

    driver = webdriver.Firefox()
    driver.minimize_window()

    for id_topico in TOPICOS_COURTS:

        date_finish = initial_date
        date_init = date_finish + timedelta(days=-0)

        for i in range(50000):
            os.system("clear")
            if (date_init - limit_date).total_seconds() < 0:
                print("\tMinimum Date reached")
                break

            str_date_init = get_date_formatted(date_init)
            str_date_finish = get_date_formatted(date_finish)

            now = datetime.now()

            print("=" * 100)
            print("T" + str(id_topico))
            print(now.strftime("%Y-%m-%d %H:%M:%S"))
            print(str_date_init, "\t", str_date_finish)

            # Run process here
            # subprocess.run(["python", "subproc_crawler.py", str_date_init, str_date_finish, str_date_init + "_" + str_date_finish, str(id_topico)])
            # os.system("python subproc_crawler.py " + str_date_init + " " + str_date_finish + " " + str_date_init + "_" + str_date_finish + " " + str(id_topico))

            url = BASE_URL_JUSBRASIL.replace("@dateFrom", str_date_init)
            url = url.replace("@dateTo", str_date_finish)
            url = url.replace("@id_topico", "idtopico=T" + str(id_topico))

            jusbrasil_crawler = JusBrasilCrawler(url, 250)
            jusbrasil_crawler.crawl_interval(driver, url, str_date_init + "_" + str_date_finish, "T" + str(id_topico))

            date_finish = date_init + timedelta(days=-1)
            date_init = date_finish + timedelta(days=0)

            # time.sleep((1 + random.random()) * 3)

            if random.random() < 0.01:
                time.sleep(60)


def crawler_collect_texts_from_links():
    list_courts_link_files = glob.glob(DEST_DATASET_PATH + "*")

    driver = webdriver.Firefox()
    driver.minimize_window()

    for court in list_courts_link_files:
        print("=" * 100)
        print(court.split("/")[-1].strip())

        file_links = glob.glob(court + "/links/*")

        crawler = JusBrasilCrawler()

        documents = list()
        print("Read files with links")
        for file_link in tqdm.tqdm(file_links):

            for line in open(file_link, encoding="utf-8"):
                documents.append([json.loads(line), file_link])

        random.shuffle(documents)
        print("Collecting texts")
        for doc in tqdm.tqdm(documents):
            json_doc, file_path = doc

            output_path = "/".join(file_path.split("/")[:-1]) + "/"

            crawler.get_document_content(json_doc, driver, output_path)


def main():
    # crawler_collect_links()
    crawler_collect_texts_from_links()


if __name__ == '__main__':
    main()
