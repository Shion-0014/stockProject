from time import sleep
import pandas as pd
from utils.strategy_index_functions import comp_rsi, comp_sma
from utils.line_notify import LINENotifyBot
from settings import DATAFILE, DIC_endfrag, DIC_k, ACCESS_TOKEN


if __name__ == '__main__':

    print('何分移動平均？')
    N = int(input())

    print('時間足を以下の中から選択してください.')
    print('1min, 5min, 15min, 30min, 1h, 1d, 1w, 1m')
    TIME_LEG = str(input())

    print('SMAの条件を指定してください.')
    SMA_TH_LOW = int(input())
    SMA_TH_HIGH = int(input())
    print('RSIの条件を指定してください.')
    RSI_TH_LOW = int(input())
    RSI_TH_HIGG = int(input())

    # linebotインスタンスを生成
    bot = LINENotifyBot(access_token=ACCESS_TOKEN)

    # データの数を計算
    num_data = int(N / DIC_k[TIME_LEG])

    while True:
        # dataの取得
        data = pd.read_csv(DATAFILE)

        # 現在の値を取得
        data_now = data.iloc[-1, :]

        # 時間分解能に対応する, 各足の終値を取得
        data = data[data[DIC_endfrag[TIME_LEG]] == 1]
        # 末尾が一致していないなら現在のものを加える。一致しているならそのままでいい。
        if data_now[DIC_endfrag[TIME_LEG]] != 1:
            data = pd.concat([data, pd.DataFrame(data_now).T], axis=0)

        sma = comp_sma(data, num_data)
        rsi = comp_rsi(data, num_data)

        # Lineに通知
        if sma >= SMA_TH_LOW and sma <= SMA_TH_HIGH and rsi >= RSI_TH_LOW and rsi <= RSI_TH_HIGG:
            bot.send(message='株価が条件値を満たしました')

        sleep(5)
