import datetime
from time import sleep
import csv
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import settings
from utils.preprocessing import preprocessing

# ブラウザのオプションを格納する変数。
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

def get_stock_price(url):
    # ブラウザを起動する
    driver = webdriver.Chrome(chrome_options=options)
    # ブラウザでアクセスする
    driver.get(url)
    # HTMLを文字コードをUTF-8に変換してから取得。
    html = driver.page_source.encode('utf-8')
    # BeautifulSoupで扱えるようにパース。
    soup = BeautifulSoup(html, "html.parser")

    return soup.select_one("#last_last").text.strip(',')


if __name__ == '__main__':

    while True:
        dt_now = datetime.datetime.now()
        list_data = []
        st_price = get_stock_price(settings.URL)

        list_data[0:2] = [dt_now.strftime('%Y/%m/%d'), dt_now.strftime('%H:%M')]
        list_data[2:-1] = [st_price.replace(',', '') for i in range(4)]
        list_data.append(0.0)

        while True:
            if dt_now.minute == datetime.datetime.now().minute:

                st_price_new = get_stock_price(settings.URL).replace(',', '')
                # 高値の更新
                if list_data[3] < st_price_new:
                    list_data[3] = st_price_new
                # 安値の更新
                if list_data[4] > st_price_new:
                    list_data[4] = st_price_new
                # 終値の更新
                list_data[5] = st_price_new

                # sleep
                sleep(5)

            else:
                # dataframeに変更
                data = np.array(list_data).reshape(1, -1)
                data = pd.DataFrame(data, columns=['日付','時間','始値','高値','安値','終値','出来高'])
                data = preprocessing(data)
                list_data = list(data.iloc[0, :])

                with open(settings.DATAFILE, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(list_data)
                break

