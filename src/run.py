import pandas as pd
from utils.strategy_index_functions import comp_rsi, comp_sma
from settings import DATAFILE, DIC_endfrag, DIC_k


if __name__ == '__main__':

    print('何分移動平均？')
    N = int(input())

    print('時間足を以下の中から選択してください.')
    print('1min, 5min, 15min, 30min, 1h, 1d, 1w, 1m')
    TIME_LEG = str(input())

    # データの数を計算
    num_data = int(N / DIC_k[TIME_LEG])

    # dataの取得
    data = pd.read_csv(DATAFILE)

    # 現在の値を取得
    data_now = data.iloc[-1, :]

    # 時間分解能に対応する, 各足の終値を取得
    data = data[data[DIC_endfrag[TIME_LEG]] == 1]
    # 末尾が一致していないなら現在のものを加える。一致しているならそのままでいい。
    if data_now[DIC_endfrag[TIME_LEG]] != 1:
        data = pd.concat([data, pd.DataFrame(data_now).T], axis=0)

    SMA = comp_sma(data, num_data)
    RSI = comp_rsi(data, num_data)

    print(SMA, RSI)

