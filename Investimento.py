import time
import pandas as pd

import streamlit as st
from click import option
from select import select
from streamlit import slider


def main():
    st.title('Aprendendo a Investir com Streamlit')
    st.write('Aprender python na @ESCOLA EDC é muito legal :) ')

    st.header('Informe seu nome')
    input_text = st.text_input('Digite aqui por gentileza')
    if input_text:
        st.write('Seja bem vindo ', input_text,'!')

    st.header('Defina o valor que você deseja começar')
    slider_value = st.slider('Escolha um valor', 0, 100, 50)
    st.write('Você vai começar com:', slider_value)

    st.header('Defina onde deseja investir')
    opção = st.selectbox('Selecione uma opção:',
                         ['Nenhum','Nubank', 'Stone', 'Caixa', 'Neon'])

    st.header('Desempenho por banco')
    data = {
        "Banco": ["Nubank", "Caixa", "Neon", "Stone"],
        "Valores": [1000, 2000, 3000, 4000]
    }
    df = pd.DataFrame(data)
    df.set_index("Banco", inplace=True)
    st.line_chart(df)

    if opção:
        st.write('Seu banco de investimento é:', opção)

    st.header('Defina o prazo para resgate')
    checkbox_regate1 = st.checkbox('Na hora que eu quiser')
    checkbox_regate2 = st.checkbox('6 Meses')
    checkbox_regate3 = st.checkbox('1 Ano')

    st.header('Antes de finalizar, informe um documento')
    upload_doc = st.file_uploader('Anexe seu RG ou CNH:', type=['jpg', 'pdf', 'png'])
    if upload_doc:
        st.write('Arquivo Anexado:', upload_doc)

    checkbox_regate4 = st.checkbox('Concordo com os termos e condições de uso')

    if st.button('Cadastrar'):
        with st.spinner('Carregando...'):
            time.sleep(3)
        st.success('Você foi registrado na nossa base de dados!')


main()