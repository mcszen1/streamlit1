import streamlit as st
import pandas as pd
import numpy as np

# Função para calcular o valor da prestação
def calcular_prestacao(principal, taxa_juros, meses):
    if taxa_juros == 0: # Evitar divisão por zero
        return principal / meses
    else:
        taxa_mensal = taxa_juros / 100
        valor_prestacao = principal * (taxa_mensal * (1 + taxa_mensal)**meses) / ((1 + taxa_mensal)**meses - 1)
        return valor_prestacao

# Carregar dados do arquivo CSV
@st.cache
def carregar_dados(filepath):
    data = pd.read_csv(filepath, error_bad_lines=False, warn_bad_lines=True)
    return data

# Configurações iniciais do Streamlit
st.title('Simulador de Financiamento de Veículos')

# Carregar dados
data = carregar_dados('DadosTesteHonda.csv')
modelo_selecionado = st.selectbox('Escolha um modelo de carro:', data['MODELO'])

# Mostrar ficha do modelo selecionado
st.subheader('Ficha do Modelo')
modelo_dados = data[data['MODELO'] == modelo_selecionado]
if not modelo_dados.empty:
    st.write(modelo_dados)

# Simulação de financiamento
st.subheader('Simular Financiamento')
valor_entrada = st.slider('Valor da Entrada', 0, 30000, step=1000)
meses = st.slider('Número de Meses', 12, 60, step=1)
taxa_juros = st.slider('Taxa de Juros Mensal (%)', 0.0, 2.0, step=0.1)

if st.button('Calcular Prestação'):
    preco = modelo_dados.iloc[0]['PREÇO SUGERIDO']
    preco = preco.replace('R$', '').replace('.', '').replace(',', '.').strip()  # Ajustar formato do preço
    preco = float(preco) - valor_entrada
    prestacao = calcular_prestacao(preco, taxa_juros, meses)
    st.subheader('Detalhes do Financiamento:')
    st.write(f'Valor financiado: R$ {preco:,.2f}')
    st.write(f'Prestação mensal: R$ {prestacao:,.2f} por {meses} meses a uma taxa de {taxa_juros}% ao mês')
