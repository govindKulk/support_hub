
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime
import pandas as pd
import requests


from flyscrape import get_news_from_the_fly
from preprocess import preprocess
from helpers import generate_file_name


# Sector is not available on finviz
required_fields = ["Ticker",
"Volume",
"Price",
"Change",
"Market Cap",
"Short Float",
"Short Interest",
"Short Ratio",]

tikrs = ["VABK", "AAPL"]




"""
This function is used to get the finviz data for the tikrs
and store it in a file named ex: 26 july before market.csv

Parameters:
timeframe (str): The time frame of the data. Default is "after"

Returns:
None
"""

def main(timeframe = "after"):
    bzpro_data = pd.read_csv("./bz.csv");
    tikrs = bzpro_data["TIKR"].tolist()

    all_data = []

    for i, tikr in enumerate(tikrs):
        single_data = get_finviz_data(tikr)
        all_data.append(single_data)

    df2 = pd.DataFrame(all_data)
    
    file_name = generate_file_name(timeframe)
    pd.concat([bzpro_data, df2], axis=1).to_csv(file_name, index = False)


    print("Done")

def get_finviz_data(tikr):


    url = f"https://finviz.com/quote.ashx?t={tikr}&p=d#statements"

    try:
        driver.get(url)
        time.sleep(2)  # Adjust sleep time as needed

        # Wait for the data table to load before proceeding
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".snapshot-table2 tbody"))
        )

        data_table = driver.find_element(By.CSS_SELECTOR, ".snapshot-table2 tbody")
        data_rows = data_table.find_elements(By.CSS_SELECTOR, "tr")

        data_labels = []
        data_values = []

        for row in data_rows:
            tds = row.find_elements(By.CSS_SELECTOR, "td")
            for td in range(0, len(tds), 2):
                if tds[td].text in required_fields:
                    data_labels.append(tds[td].text)
                    data_values.append(tds[td + 1].text)

        data = dict(zip(data_labels, data_values))
        print(f"Data for {tikr}\n {data}")
        return data

    except (NoSuchElementException, TimeoutError, TimeoutException) as e:
        print(f"Error scraping data for {tikr}: {e}")
        data = {field: "No Data" for field in required_fields}
        return data


def setup_selenium_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")

    # path to chromedriver; change it to your path.
    path = r"C:\Users\govind\Downloads\chromedriver\chromedriver-win64\chromedriver.exe"
    service = Service(executable_path = path)
    driver = webdriver.Chrome(service = service, options=chrome_options)

    return driver



def get_the_fly_news(driver, tikrs):
    # get news data
    all_news_data = []
    for tikr in tikrs:
        news = get_news_from_the_fly(driver, tikr)
        for n in news:
            all_news_data.append({'TIKR': tikr, 'News': n['news'], 'Link': n['link'], 'Date': n['date']})
        time.sleep(10)

    news_df = pd.DataFrame(all_news_data, columns=['TIKR', 'News', 'Link'])
    file_name = generate_file_name(suffix="news_data")
    news_df.to_csv(file_name, index=False)


# setup your selenium driver here
driver = setup_selenium_driver()

# it prepocesses the data from benzinga pro
# store data in file named bzpre.csv in the same directory
# preprocess(pd.read_csv("bzpre.csv"))

# it is used to get the finviz data and add it to bzpro data
# stores data in file named finviz_data_16724.csv
# main()

# it is used to get the news data from the fly
# stores data in file named news_data.csv
# update the global tikrs variable with the tikrs you want to get the news for
get_the_fly_news(driver, tikrs)

driver.quit()


    


    



