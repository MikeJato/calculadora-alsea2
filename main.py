# -*- coding: utf-8 -*-

import pandas as pd

def main(period):
    print('hola')

    # TODO: leer historico de precios
    df_data = pd.read_csv('/Users/mike/calculadora-inversion/data/ALSEA.MX.csv')   
    first_date = df_data.
    # TODO: comprar a precio de mercado
    # TODO: calcular desviacion estandar del perioro desde fecha base
    # TODO: determinar precio de venta
    # TODO: vender

if __name__ == '__main__':
    periodo = raw_input('determine el periodo de inversion: ')
    print(main(periodo))