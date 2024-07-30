import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime, timedelta

def get_news_from_the_fly(driver, tikr):
    url = f"https://thefly.com/news.php?symbol={tikr}"
    
    driver.get(url)
    time.sleep(5)

    
    while True:
        # print("Scrolling down")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
  

        date_elements = driver.find_elements(By.CSS_SELECTOR, '.dateDivision.fixedLine')

        for element in date_elements:

            if any(sentence in element.text for sentence in ['Over a month ago', 'Over a quarter ago', 'Over a year ago']):
                # print("Breaking")
                break
            else:
                # print("Scrolling down")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # driver.implicitly_wait(2)


        req_news = []

  
            
        table_elements = driver.find_elements(By.CSS_SELECTOR, '.news_table')
        latest_found_date = None
        for table_element in table_elements:
            if table_element.text == '':
                continue
            news_elements = table_element.find_elements(By.CSS_SELECTOR, '.tr_noticia td .story_header a')
            news = [ news_element.text for news_element in news_elements]
            links = [ news_element.get_attribute('href') for news_element in news_elements]

            date_text = None
        
            try:
                date_text = table_element.find_element(By.CSS_SELECTOR, '.dateDivisionRow').get_attribute('data-date')
                latest_found_date = date_text
            except NoSuchElementException:
                date_text = latest_found_date
                
            # print(date_text, "date_text")
            date_obj = datetime.fromisoformat(date_text)
            if datetime.now() - date_obj > timedelta(days=30):
                break
            for i, single_news in enumerate(news):
                single_news = single_news.lower()
            
                if any(word in single_news for word in ['target', 'raised', 'raise', 'raised by']):
                    req_news.append({'news': single_news, 'link': links[i], 'date': date_text})


        

        return req_news