# Этот файл заточен под работу с фьючерсами, для акций нужно изменить параметры.
# Плюс сейчас не хавтает аналитической части,
# она происходит уже в самой табдице (Посредством Google Sheets например).

import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt




# Часть для обработки файла с данными
hist_candles_brent = pd.read_csv('csv_files/brent062022_list.csv')

hist_candles_brent.drop(columns=['Unnamed: 0'], inplace=True) # Убираем лишнюю нумерацию(Лишние столбцы)
for i in range(0, 9):
    hist_candles_brent.drop([i], inplace=True) # Убираем значеня для которых нет рассчитаных индексов МА и ЕМА
#
# Убираем повторения названий из выгрузки
hist_candles_brent.drop_duplicates(subset=['time', 'volume', 'open', 'close', 'high', 'low'], inplace=True)
# Убираем пропуски значений
hist_candles_brent.dropna(inplace=True)

# Проверка очищенных данных
print(hist_candles_brent)
print(hist_candles_brent.dtypes)

# Перезапись в файл данных
hist_candles_brent.to_csv('csv_files/brent062022_report.csv', mode='w')
print("Record complete")


# Добавление индикаторов
# hist_candles_brent['ema'] = ta.ema(hist_candles_brent['close'], 10)
# hist_candles_brent['ma'] = ta.sma(hist_candles_brent['close'], lenght=10)

# Проверка
# print(hist_candles_brent[['time', 'close', 'ema', 'ma']].tail(30))
# Запись в файл данных
# hist_candles_brent.to_csv('csv_files/brent062022_list.csv', mode='w')
# print("Record complete")


def ma_ema_cross_strategy_test(historical_candles_df):
    hcdf = historical_candles_df
    open_positions = 0  # Текущие открытые позиции
    check_rule = [bool, bool, bool]  # Массив для проверки по правилам
    condition_sell = [False, True, False]  # Правило 1
    condition_buy = [True, False, True]  # Правило 2
    ma = hcdf['ma']
    ema = hcdf['ema']
    hcdf['contract_turnover'] = 0
    hcdf['deal'] = pd.NaT
    hcdf['commission'] = 0



    for indx in range(len(hcdf)):

        indx_min_1 = indx - 1
        if indx_min_1 < 0:
            continue

        # Условие которое может быть пригодится
        # 1 Condition
        # if ma.loc[indx, ()] > ma.loc[indx, ()_min_1]:
        #    check_rule[0] = True
        # else:
        #     check_rule[0] = False

        # 2 Condition
        if ema[indx] > ema[indx_min_1]:
            check_rule[0] = True
        else:
            check_rule[0] = False
        # 3 Condition
        if ma[indx] > ema[indx]:
            check_rule[1] = True
        else:
            check_rule[1] = False
        # 4 Condition
        if ma[indx_min_1] > ema[indx_min_1]:
            check_rule[2] = True
        else:
            check_rule[2] = False
        order_positions = int

        if open_positions == 0 and check_rule == condition_sell:
            order_positions = -1
        elif open_positions == 0 and check_rule == condition_buy:
            order_positions = 1
        elif indx == len(hcdf) - 2:
            order_positions = -1 * open_positions
        elif open_positions == -1:
            order_positions = 2
        elif open_positions == 1:
            order_positions = -2

        if check_rule == condition_buy and open_positions != 1:
            hcdf.loc[indx, 'deal'] = 'buy'
            hcdf.loc[indx, 'contract_turnover'] = order_positions * hcdf.loc[indx, 'close'] / 0.01 * 6.41814
            hcdf.loc[indx, 'commission'] = abs(order_positions * hcdf.loc[indx, 'close'] / 0.01 * 6.41814 * 0.0004)
        elif check_rule == condition_sell and open_positions != -1:
            hcdf.loc[indx, 'deal'] = 'sell'
            hcdf.loc[indx, 'contract_turnover'] = order_positions * hcdf.loc[indx, 'close'] / 0.01 * 6.41814
            hcdf.loc[indx, 'commission'] = abs(order_positions * hcdf.loc[indx, 'close'] / 0.01 * 6.41814 * 0.0004)
        elif indx == len(hcdf) - 2:
            hcdf.loc[indx, 'deal'] = 'close'
            hcdf.loc[indx, 'contract_turnover'] = order_positions * hcdf.loc[indx, 'close'] / 0.01 * 6.41814
            hcdf.loc[indx, 'commission'] = abs(order_positions * hcdf.loc[indx, 'close'] / 0.01 * 6.41814 * 0.0004)

        if open_positions == 0 and check_rule == condition_buy:
            open_positions += 1
        elif open_positions == -1 and check_rule == condition_buy:
            open_positions += 2
        elif open_positions == 0 and check_rule == condition_sell:
            open_positions -= 1
        elif open_positions == 1 and check_rule == condition_sell:
            open_positions -= 2
        elif indx == len(hcdf)-2:
            open_positions = 1 - open_positions
        else:
            open_positions = open_positions

            # Далее три опции:

    # Построение графика при необходимости (нужно еще раскомментировать импорт matplotlib)
    # with plt.style.context('Solarize_Light2'):
    #     a = hcdf['time']
    #     b = hcdf['close']
    #     c = hcdf['ma']
    #     d = hcdf['ema']
    #     plt.plot(a, b, a, c, a, d)
    #     plt.show()

    # Вывод полученных значений
    hcdf.drop(columns=['Unnamed: 0'], inplace=True)
    hcdf.dropna(how='any', inplace=True)

    # print(hcdf)

    return hcdf

    # Запись значений в файл со своим названием
    # hcdf.to_csv('csv_files/brent062022_orders.csv', mode='w')
    # print('Record to file complete')


def check_profits(operations_df):
    operations_df.dropna(how='any', inplace=True)
    trade_result = 0
    commision_sum = 0
    # o = operations_df['contract_turnover']
    # c = operations_df['commission']
    for i in range(len(operations_df)):

        trade_result += operations_df['contract_turnover'].iloc[i]
        commision_sum += operations_df['commission'].iloc[i]

    return print(trade_result - commision_sum)


def record_orders_results(operations_df):
    operations_df.dropna(how='any', inplace=True)
    operations_df.to_csv('csv_files/brent062022_orders.csv')
    return print('Record orders results complete')


brent_report = pd.read_csv('csv_files/brent062022_report.csv')
df = ma_ema_cross_strategy_test(brent_report)

check_profits(df)
