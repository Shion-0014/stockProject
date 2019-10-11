
def comp_sma(data, num_data):
    return data['終値'].tail(num_data).mean()


def comp_rsi(data, num_data):
    diff = data['終値'].diff().tail(num_data)
    up, down = diff.copy(), diff.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    rsi = up.mean() / (up.mean() + down.abs().mean()) * 100
    return rsi


def comp_sma_global(data, num_data):
    data['SMA'] = data['終値'].rolling(window=num_data).mean()
    return data


def comp_rsi_global(data, num_data):
    diff = data['終値'].diff()
    up, down = diff.copy(), diff.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    up = up.rolling(window=num_data).mean()
    down = down.abs().rolling(window=num_data).mean()
    data['RSI'] = up / (up + down) * 100
    return data
