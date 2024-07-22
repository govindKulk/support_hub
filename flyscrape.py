import time
from selenium.webdriver.common.by import By
import pandas as pd

def get_news_from_the_fly(driver, tikr):
    url = f"https://thefly.com/news.php?symbol={tikr}"

    driver.get(url)
    time.sleep(5)

    while True:
        print("Scrolling down")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        date_elements = driver.find_elements(By.CSS_SELECTOR, '.dateDivision.fixedLine')
        for element in date_elements:

            if any(sentence in element.text for sentence in ['Over a month ago', 'Over a quarter ago', 'Over a year ago']):
                print("Breaking")
                break
            else:
                print("Scrolling down")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

        news_elements = driver.find_elements(By.CSS_SELECTOR, '.tr_noticia td .story_header a')
        news = [ news_element.text for news_element in news_elements]
        links = [ news_element.get_attribute('href') for news_element in news_elements]

        req_news = []
        for i, single_news in enumerate(news):
            single_news = single_news.lower()
            
            if any(word in single_news for word in ['target', 'raised', 'raise', 'raised by']):
                req_news.append({'news': single_news, 'link': links[i]})

        return req_news