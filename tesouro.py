from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from datetime import date
import windows

# importação dos dados

import pandas as pd

# df_ipca_2020 = pd.read_excel("https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2020/NTN-B_Principal_2020.xls",
#                    sheet_name=[0,1,2,3], header=1,
#                    parse_dates=[0], date_parser= lambda t: pd.to_datetime(t,format="%d/%m/%Y"))

df_ipca_1 = pd.read_excel("https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2021/NTN-B_Principal_2021.xls",
                          sheet_name=[0, 1, 2, 3], header=1,
                          parse_dates=[0], date_parser=lambda t: pd.to_datetime(t, format="%d/%m/%Y"))

df_ipca_2 = pd.read_excel("https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2022/NTN-B_Principal_2022.xls",
                          sheet_name=[0, 1, 2, 3], header=1,
                          parse_dates=[0], date_parser=lambda t: pd.to_datetime(t, format="%d/%m/%Y"))

df_ipca_3 = pd.read_excel("https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/sistd/2023/NTN-B_Principal_2023.xls",
                          sheet_name=[0, 1, 2, 3, 4], header=1,
                          parse_dates=[0], date_parser=lambda t: pd.to_datetime(t, format="%d/%m/%Y"))

ipca2035 = pd.concat([df_ipca_1[2], df_ipca_2[2], df_ipca_3[3]])
ipca2045 = pd.concat([df_ipca_1[3], df_ipca_2[3], df_ipca_3[4]])

# =======================================================================================================================
# renomeando colunas

c = {'Dia': 'Data',
     'Taxa Compra Manhã': 'TxCompra',
     'Taxa Venda Manhã': 'TxVenda',
     'PU Compra Manhã': 'PuCompra',
     'PU Venda Manhã': 'PuVenda',
     'PU Base Manhã': 'PuBase'}

ipca2035.rename(columns=c, inplace=True)
ipca2045.rename(columns=c, inplace=True)

ipca2035['TxCompra'] = ipca2035['TxCompra']*100
ipca2045['TxCompra'] = ipca2045['TxCompra']*100

ipca2035['TxVenda'] = ipca2035['TxVenda']*100
ipca2045['TxVenda'] = ipca2045['TxVenda']*100


# =======================================================================================================================

st.title('Informações básicas - IPCA 2035')
today = pd.Timestamp('today').strftime("%Y-%m-%d")
df_today_1 = ipca2035.query("Data==@today")
st.table(df_today_1)

st.title('Informações básicas - IPCA 2045')
today = pd.Timestamp('today').strftime("%Y-%m-%d")
df_today_1 = ipca2045.query("Data==@today")
st.table(df_today_1)


# =======================================================================================================================
# Select IPCA

form = st.form("my_form")

title_ipca_option = form.selectbox(
    'Selecione o título do IPCA',
    ('IPCA 2035', 'IPCA 2045'))

if (title_ipca_option == 'IPCA 2035'):
    title_ipca_value = ipca2035
else:
    title_ipca_value = ipca2045

# =======================================================================================================================
# Select Taxa

rate_option = form.selectbox(
    'Selecione o tipo de transação',
    ('Compra', 'Venda'))

if (rate_option == 'Compra'):
    rate_value = 'TxCompra'
else:
    rate_value = 'TxVenda'

# =======================================================================================================================
# Select Janela

windows_option = form.selectbox(
    'Selecione o número de janelas',
    ('4', '6', '8', '10'))


if (windows_option == '4'):
    windows_value = np.array([4])
elif (windows_option == '6'):
    windows_value = np.array([6])
elif (windows_option == '8'):
    windows_value = np.array([8])
elif (windows_option == '10'):
    windows_value = np.array([10])

# =======================================================================================================================
# Executando a função

form.form_submit_button('Verificar janela', on_click=windows.qual_janela(
    title_ipca_value, rate_value, windows_value), use_container_width=True, type='primary')
