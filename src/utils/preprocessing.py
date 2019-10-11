import datetime

import numpy as np
import pandas as pd


# 取引日についてと実時間の出力
def make_traiding_time(x):
    lis = x.replace(':', '/').split('/')
    return datetime.datetime(int(lis[0]), int(lis[1]), int(lis[2]), int(lis[3]), int(lis[4]))


# 取り引き日をJSTに変換するローカル函数
def make_real_time(x):
    if x.time() >= datetime.time(16, 30):
        return x - datetime.timedelta(days=1)
    else:
        return x


# 日付情報を実際に変換する函数
def convert_real_time(data):
    data['traiding_time'] = data['日付'] + '/' + data['時間']
    # ?
    data['traiding_time'] = data['traiding_time'].map(make_traiding_time)
    data['real_time'] = data['traiding_time'].map(make_real_time)
    return data


# 曜日の算出するローカル函数（0:月, .., 6:日）
def comp_weekday(x):
    date_list = x.split('/')
    weekday = datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2])).weekday()
    return weekday


# 日付情報の分離統合をする函数
def date_split(data):
    # 日付情報の分離
    data_date = data['日付'].str.split('/', expand=True).astype('int')
    data_time = data['時間'].str.split(':', expand=True).astype('int')

    # 統合
    data_date.columns = ['year', 'month', 'day']
    data_time.columns = ['hour', 'min']
    data_date = pd.concat([data_date, data_time], axis=1)
    data = pd.concat([data_date, data], axis=1)
    return data


# 月末フラグの作成
def make_monthend(data):
    # 月末は1, 月末の最終時間は2
    # 月の差分をとって月末フラグを作成。
    diff = data['month'].diff().values
    diff = np.append(diff[1:], 0)
    diff_frag = list(np.where(diff == 1))

    # 月末の日付を抽出
    end_dates = [data.values[i, 5] for i in diff_frag][0]
    # 月末フラグを作成
    data['end_of_month_frag'] = data['日付'].map(lambda x: 1 if x in end_dates else 0)
    return data


# endfragの作成
def make_endfrag(data):
    # endfragの作成
    data['1min_endfrag'] = 1
    data['5min_endfrag'] = 0
    data['15min_endfrag'] = 0
    data['30min_endfrag'] = 0
    data['1h_endfrag'] = 0
    data['1d_endfrag'] = 0
    data['1w_endfrag'] = 0
    data['1m_endfrag'] = 0

    # 分単位で欠損がないことを仮定
    # 1d, 1w, 1mは15:15を終値としているが、min, h系統は15:14を終値としてとっている...。
    data['5min_endfrag'].mask(data['min'] % 5 == 4, 1, inplace=True)
    data['15min_endfrag'].mask(data['min'] % 15 == 14, 1, inplace=True)
    data['30min_endfrag'].mask(data['min'] % 30 == 14, 1, inplace=True)
    data['1h_endfrag'].mask(data['min'] == 14, 1, inplace=True)  # 今のままだと5:30を終値とできない。5:14を終値とする。
    data['1d_endfrag'].mask((data['hour'] == 15) & (data['min'] == 15), 1, inplace=True)  # 一日の終値は日中取引の終値をいう。
    data['1w_endfrag'].mask((data['weekday'] == 4) & (data['hour'] == 15) & (data['min'] == 15), 1, inplace=True)
    data['1m_endfrag'].mask((data['end_of_month_frag'] == 1) & (data['hour'] == 15) &
                            (data['min'] == 15), 1, inplace=True)

    return data


# 前処理を完結する函数
def preprocessing(data):
    data = convert_real_time(data)
    data['weekday'] = data['日付'].map(comp_weekday)
    data = date_split(data)
    data = make_monthend(data)
    data = make_endfrag(data)
    data = data.loc[:,['real_time', '始値', '高値', '安値', '終値', '1min_endfrag', '5min_endfrag', '15min_endfrag',
                       '1h_endfrag', '1d_endfrag', '1w_endfrag', '1m_endfrag']]
    return data


if __name__ == '__main__':

    data = pd.read_csv('../../data/raw/N225f_2019.csv')
    data = preprocessing(data)
    data.to_csv('../../data/processed/stock_price.csv', index=False)

