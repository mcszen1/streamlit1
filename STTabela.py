import pandas as pd
import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt
st.image('labcom_logo_preto.jpg')
st.head('Analista de Tabelas - Versão teste')
uploaded_file=st.file_uploader('Insira seu arquivo csv', type='csv')

if uploaded_file is not None:

    df=pd.read_csv(uploaded_file, encoding='utf-8')
else:
    st.write('Não tenho dados e por isso até você selecionar algum arquivo vou apresentar o erro abaixo')
    
if df is not None:
    delet=st.multiselect('Selecione as colunas para deletar', df.columns)
    df2=df.drop(delet, axis=1)
    st.write(df2)
    reduz=st.multiselect('Selecione as colunas para gerar uma nova tabela', df2.columns)
    df3=df2.loc[:,reduz]
    st.write(df3.columns)
    order=st.multiselect('Selecione uma coluna para ordenar a tabela', df3.columns)
    st.write(df3.sort_values(order, ascending=False))

else:
    st.write('Ainda não tenho os dados da sua tabela')
with open('stop_words_brazil.txt', mode='r', encoding='utf-8') as file:
    stopw1 = [str(s.strip()) for s in file.readlines()]
coluna_textos=st.multiselect('Selecione a coluna de textos da tabela que quer analisar', df3.columns)
textos=''.join(df3[coluna_textos[0]].tolist())
textos1=[p for p in textos.split() if p.lower() not in stopw1 if len(p)>2]
word_count=Counter(textos1)

for word, count in word_count.most_common(25):
        st.write(word, count)

words, counts = zip(*word_count.most_common(25))

plt.figure(figsize=(12,8))
plt.barh(words, counts, color='skyblue')
plt.xlabel('Count')
plt.ylabel('Words')
plt.title('Top 25 Most Common Words')
plt.gca().invert_yaxis()  # para exibir a palavra mais comum no topo
st.pyplot(plt)
