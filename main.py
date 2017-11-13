# -*- coding: utf-8 -*-

import pandas as pd
from datetime import timedelta, datetime

def main(capital, period):

    # leer historico de precios
    df_data = pd.read_csv('/Users/mike/calculadora-alsea2/data/ALSEA.MX.csv')   
    df_data.Date = df_data.Date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    # obtener fecha inicial
    beg_date = df_data.Date.min()

    # determino fecha final
    end_date = beg_date + timedelta(days=period)

    # obtengo muestra de datos a utilizar
    df_sample = df_data[(df_data.Date >= beg_date) & (df_data.Date <= end_date)]

    # calcular desviacion estandar
    close_std  = df_sample.Close.std()
    print('desviacion std: {}'.format(close_std))

    # establecer precios de compra y venta
    end_date = df_sample.Date.max()
    close_price = df_sample[(df_data.Date == end_date)].Close 
    goal_buy_price = float(close_price) - float(close_std)
    goal_ask_price = float(close_price) + float(close_std)

    print('meta de compra: {}'.format(goal_buy_price))
    print('meta de venta: {}'.format(goal_ask_price))

    # establecer siguiente compra
    buy_date = df_data[(df_data.Date > end_date) & (df_data.Close <= goal_buy_price)].iloc[0].Date
    buy_price = float(df_data[(df_data.Date == buy_date)].Close)
    values = float(capital / buy_price)
    print('fecha de compra: {}'.format(buy_date))
    print('precio de compra: {}'.format(buy_price))
    print('acciones: {}'.format(values))

    # TODO: determinar precio de venta
    # TODO: vender

if __name__ == '__main__':
    capital = float(raw_input('capital: '))
    periodo = int(raw_input('periodo: '))
    print(main(capital, periodo))