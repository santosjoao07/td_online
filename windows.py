import streamlit as st
import pandas as pd
import numpy as np


# =======================================================================================================================
# Função definir janela


def define_janela(tx, minimo, maximo, janelas, tipo):
    n_janelas = janelas.shape[0]
    idx_mediana = n_janelas // 2
    q_mediana = janelas.iloc[idx_mediana]

    if tipo == 'TxCompra':
        q_prev_mediana = janelas.iloc[idx_mediana-1]
        q_penultimo = janelas.iloc[-2]
        q_ultimo = janelas.iloc[-1]

        i = 1
        while q_penultimo == maximo or q_ultimo == maximo:
            q_penultimo = janelas.iloc[n_janelas-i-1]
            q_ultimo = janelas.iloc[n_janelas-i]
            i += 1

        if tx >= minimo and tx <= q_prev_mediana:
            st.write('Compra péssima! :thumbsdown:')
        elif tx > q_prev_mediana and tx <= q_mediana:
            st.write('Compra ruim! :-1:')
        elif tx > q_mediana and tx <= q_penultimo:
            st.write('Compra boa! :ok_hand:')
        elif tx > q_penultimo and tx <= q_ultimo:
            st.write('Compra ótima! :grin:')
        elif tx > q_ultimo and tx <= maximo:
            st.write('Compra excelente! :sunglasses:')
        else:
            st.caption(f'Condição ainda não verificada!')
    else:
        q_pos_mediana = janelas.iloc[idx_mediana-1]
        q_segundo = janelas.iloc[1]
        q_primeiro = janelas.iloc[0]

        i = 1
        while q_segundo == minimo or q_primeiro == minimo:
            q_segundo = janelas.iloc[i+1]
            q_primeiro = janelas.iloc[i]
            i += 1

        if tx <= maximo and tx >= q_pos_mediana:
            st.write('Venda péssima! :thumbsdown:')
        elif tx < q_pos_mediana and tx >= q_mediana:
            st.write('Venda ruim! :-1:')
        elif tx < q_mediana and tx >= q_segundo:
            st.write('Venda boa! :ok_hand:')
        elif tx < q_segundo and tx >= q_primeiro:
            st.wirte('Venda boa! :grin:')
        elif tx < q_primeiro and tx >= minimo:
            st.write('Venda ótima! :sunglasses:')
        else:
            st.write(f'Condição ainda não verificada!')

# =======================================================================================================================
# Função qual janela


def qual_janela(df, tipo='TxCompra', n_janelas=[]):
    '''
    Quanto mais janelas, maior a acuracia/rigor para definir a qualidade da
    compra/venda
    '''

    today = pd.Timestamp('today').strftime("%Y-%m-%d")
    # today = pd.Timestamp('2023-01-19T12').strftime("%Y-%m-%d")
    df_today = df.query('Data==@today')
    tx = df_today.loc[:, tipo].item()
    minimo = df[tipo].min()
    maximo = df[tipo].max()

    st.write(
        f'{tipo} hoje: {tx:.2f}%; Min: {minimo:.3f}%; Max: {maximo:.3f}%;')

    for n_j in n_janelas:
        st.write(f'Para {n_janelas[0]} janelas: ')
        qtl = np.array([i / n_j for i in range(1, n_j)])
        janelas = df[tipo].quantile(qtl)
        st.table(janelas)
        define_janela(tx, minimo, maximo, janelas, tipo)
