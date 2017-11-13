# -*- coding: utf-8 -*-
import pandas as pd
from datetime import timedelta, datetime

def main(capital, period):

    # leer historico de precios
    df_data = pd.read_csv('/Users/mike/calculadora-alsea2/data/ALSEA.MX.csv')   
    df_data.Date = df_data.Date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    # determino perio de muestra
    beg_date = df_data.Date.min()
    end_date = beg_date + timedelta(days=period)
    print('periodo muestra: {} - {}'.format(beg_date, end_date))

    # obtengo muestra de datos a utilizar
    df_sample = df_data[(df_data.Date >= beg_date) & (df_data.Date <= end_date)]

    # calcular desviacion estandar
    close_std  = df_sample.Close.std()
    print('desviacion std: {}'.format(close_std))

    # establecer precios de compra y venta
    end_date = df_sample.Date.max()
    close_price = df_sample[(df_sample.Date == end_date)].Close
    goal_bid_price = float(close_price) - float(close_std)
    goal_ask_price = float(close_price) + float(close_std)

    print('meta de compra: {}'.format(goal_bid_price))
    print('meta de venta: {}'.format(goal_ask_price))

    # establecer momento de compra
    df_bid = df_data[(df_data.Date > end_date) & (df_data.Close <= goal_bid_price)]
    if df_bid.shape[0] > 0:
        bid_date = df_bid.iloc[0].Date
        bid_price = float(df_bid.iloc[0].Close)
        stocks = capital / bid_price
        print('fecha de compra: {}'.format(bid_date))
        print('precio de compra: {}'.format(bid_price))
        print('acciones: {}'.format(stocks))

    # establecer momento de venta
    df_ask = df_data[(df_data.Date > bid_date) & (df_data.Close >= goal_ask_price)]
    if df_ask.shape[0] > 0:
        ask_date = df_ask.iloc[0].Date
        ask_price = float(df_ask.iloc[0].Close)
        capital = stocks * ask_price
        print('fecha de venta: {}'.format(ask_date))
        print('precio de venta: {}'.format(ask_price))
        print('capital: {}'.format(capital))
        print('rend directo: {}%'.format((ask_price / bid_price - 1) * 100))
        # print('dias inversion: {}'.format())
        

    # TODO: determinar precio de venta
    # TODO: vender
    return True

if __name__ == '__main__':
    capital = float(raw_input('capital: '))
    periodo = int(raw_input('periodo: '))
    print(main(capital, periodo))