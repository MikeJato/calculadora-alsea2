# -*- coding: utf-8 -*-
import pandas as pd
from datetime import timedelta, datetime

def obtener_bid_ask(df_data, end_date, periodo):
    
    # determino periodo de muestra
    beg_date = end_date + timedelta(days=-period)
    print('periodo muestra: {} - {}'.format(beg_date, end_date))
 
    # obtengo muestra de datos a utilizar
    df_sample = df_data[(df_data.Date >= beg_date) & (df_data.Date <= end_date)]

    # calcular desviacion estandar
    close_std  = float(df_sample.Close.std())
    print('desviacion std: {}'.format(close_std))

    # establecer precios de compra y venta
    end_date = df_sample.Date.max()
    close_price = float(df_sample[(df_sample.Date == end_date)].Close)
    goal_bid_price = close_price - close_std
    goal_ask_price = close_price + close_std

    return goal_bid_price, goal_ask_price

def identificar_compra(df_data, end_date, goal_bid_price):
    
    df_bid = df_data[(df_data.Date > end_date) & (df_data.Close <= goal_bid_price)]

    if df_bid.shape[0] > 0:
        bid_date = df_bid.iloc[0].Date
        bid_price = float(df_bid.iloc[0].Close)
        print('compra!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('fecha: {}, precio: ${}'.format(bid_date, bid_price))

        return bid_date, bid_price

    else:
        raise Exception('imposible comprar')

def identificar_venta(df_data, bid_date, goal_ask_price):
    
    df_ask = df_data[(df_data.Date > bid_date) & (df_data.Close >= goal_ask_price)]
    if df_ask.shape[0] > 0:
        ask_date = df_ask.iloc[0].Date
        ask_price = float(df_ask.iloc[0].Close)
        print('venta!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('fecha: {}, precio: ${}'.format(ask_date, ask_price))

        return ask_date, ask_price
        
    else:
        raise Exception('imposible vender')

def main(capital, period):
    
    beg_capital = capital           # capital inicial

    # leer historico de precios
    df_data = pd.read_csv('/Users/mike/calculadora-alsea2/data/ALSEA.MX.csv')   
    df_data.Date = df_data.Date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    # determino periodo de muestra
    date = df_data.Date.min() + timedelta(days=period)
    fTrade = True
    stocks = 0

    while fTrade:
        
        print('---------------------')
        
        try:

            # obtengo precios de compra y venta
            goal_bid_price, goal_ask_price = obtener_bid_ask(df_data, date, period)
            print('metas: {} - {}'.format(goal_bid_price, goal_ask_price))

            # establecer momento de compra
            bid_date, bid_price = identificar_compra(df_data, date, goal_bid_price)
            stocks = int(capital / bid_price)
            print('acciones: {} ({} / {})'.format(stocks, capital, bid_price))
            capital -= stocks * bid_price

            # establecer momento de venta
            ask_date, ask_price = identificar_venta(df_data, bid_date, goal_ask_price)
            capital += stocks * ask_price
            print('capital: {}, rend: {}%'.format(capital, (ask_price / bid_price - 1) * 100))
            stocks = 0

            # siguiene ciclo
            date = ask_date

        except Exception as exc:
            print(str(exc))
            fTrade = False

    print('---------------------')

    last_price = float(df_data[(df_data.Date == df_data.Date.max())].Close)
    last_capital = stocks * last_price + capital

    print('capital final: ${} (${} x {} + ${})'.format(last_capital, last_price, stocks, capital))
    print('rendimiento: {}%'.format((last_capital / beg_capital - 1) * 100))
    print('muestreo: {}'.format(period))

    return True

if __name__ == '__main__':
    capital = float(raw_input('capital: '))
    period = int(raw_input('periodo: '))
    print(main(capital, period))