# Этот файл заточен под работу с фьючерсами, для акций нужно изменить параметры.
# Плюс сейчас не хавтает аналитической части,
# она происходит уже в самой табдице (Посредством Google Sheets например).

import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt



# Часть для обработки файла с данными
hist_candles_brent = pd.read_csv('csv_files/brent062022_report.csv')

# hist_candles_brent.drop(columns=['Unnamed: 0'], inplace=True) # Убираем лишнюю нумерацию(Лишние столбцы)
# for i in range(0, 9):
#     hist_candles_brent.drop([i], inplace=True) # Убираем значеня для которых нет рассчитаных индексов МА и ЕМА
#
# Убираем повторения названий из выгрузки
# hist_candles_brent.drop_duplicates(subset=['time', 'volume', 'open', 'close', 'high', 'low'], inplace=True)
# Убираем пропуски значений
# hist_candles_brent.dropna(inplace=True)

# Проверка очищенных данных
# print(hist_candles_brent)
# print(hist_candles_brent.dtypes)

# Перезапись в файл данных
# hist_candles_brent.to_csv('csv_files/brent062022_report.csv', mode='w')
# print("Record complete")


# Добавление индикаторов
# hist_candles_brent['ema'] = ta.ema(hist_candles_brent['close'], 10)
# hist_candles_brent['ma'] = ta.sma(hist_candles_brent['close'], lenght=10)

# Проверка
# print(hist_candles_brent[['time', 'close', 'ema', 'ma']].tail(30))
# Запись в файл данных
# hist_candles_brent.to_csv('csv_files/brent062022_list.csv', mode='w')
# print("Record complete")


def ma_ema_cross_strategy_test(historical_candles_df):
    open_positions = 0  # Текущие открытые позиции
    check_rule = [bool, bool, bool]  # Массив для проверки по правилам
    condition_sell = [False, True, False]  # Правило 1
    condition_buy = [True, False, True]  # Правило 2
    close = historical_candles_df['close']
    ma = historical_candles_df['ma']
    ema = historical_candles_df['ema']
    historical_candles_df['contract_turnover'] = 'NaN'
    contract_turnover = historical_candles_df['contract_turnover']
    historical_candles_df['deal'] = 'NaN'
    deal = historical_candles_df['deal']
    historical_candles_df['comission'] = 'NaN'
    broker_comission = historical_candles_df['comission']


    for indx in range(len(historical_candles_df)):

        indx_min_1 = indx - 1

        # Условие которое может быть пригодится
        # 1 Condition
        # if ma.iloc[indx] > ma.iloc[indx_min_1]:
        #    check_rule[0] = True
        # else:
        #     check_rule[0] = False

        # 2 Condition
        if ema.iloc[indx] > ema.iloc[indx_min_1]:
            check_rule[1] = True
        else:
            check_rule[1] = False
        # 3 Condition
        if ma.iloc[indx] > ema.iloc[indx]:
            check_rule[2] = True
        else:
            check_rule[2] = False
        # 4 Condition
        if ma.iloc[indx_min_1] > ema.iloc[indx_min_1]:
            check_rule[3] = True
        else:
            check_rule[3] = False
        order_positions = int

        if open_positions == 0 and check_rule == condition_sell:
            order_positions = -1
        elif open_positions == 0 and check_rule == condition_buy:
            order_positions = 1
        elif open_positions == -1:
            order_positions = 2
        elif open_positions == 1:
            order_positions = -2

        if check_rule == condition_buy and open_positions != 1:
            deal.iloc[indx] = 'buy'
            contract_turnover.iloc[indx] = order_positions * close.iloc[indx] / 0.01 * 6.41814
            broker_comission.iloc[indx] = abs(order_positions * close.iloc[indx] / 0.01 * 6.41814 * 0.0004)
        elif check_rule == condition_sell and open_positions != -1:
            deal.iloc[indx] = 'sell'
            contract_turnover.iloc[indx] = order_positions * close.iloc[indx] / 0.01 * 6.41814
            broker_comission.iloc[indx] = abs(order_positions * close.iloc[indx] / 0.01 * 6.41814 * 0.0004)

        if open_positions == 0 and check_rule == condition_buy:
            open_positions += 1
        elif open_positions == -1 and check_rule == condition_buy:
            open_positions += 2
        elif open_positions == 0 and check_rule == condition_sell:
            open_positions -= 1
        elif open_positions == 1 and check_rule == condition_sell:
            open_positions -= 2
        else:
            open_positions = open_positions

            # Далее три опции:

    # Построение графика при необходимости (нужно еще раскомментировать импорт matplotlib)
    # with plt.style.context('Solarize_Light2'):
    #     a = historical_candles_df['time']
    #     b = historical_candles_df['close']
    #     c = historical_candles_df['ma']
    #     d = historical_candles_df['ema']
    #     plt.plot(a, b, a, c, a, d)
    #     plt.show()

    # Вывод полученных значений
    print(historical_candles_df)

    # Запись значений в файл со своим названием
    # historical_candles_df.to_csv('csv_files/brent062022_report.csv')
    # print('Record to file complete')

ma_ema_cross_strategy_test(hist_candles_brent)

