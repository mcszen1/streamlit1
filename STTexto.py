import pandas as pd
import streamlit as st
from collections import Counter
import matplotlib.pyplot as plt
import string
import io

st.title('Analista de Textos')

st.header('Palavras Frequentes')
st.write('A partir de um arquivo de texto txt vamos gerar um gráfico com as palavras mais frequentes')
numero = st.slider('Quantas palavras frequentes quer no gráfico?', 5, 50, 25, 5)

def bytestotext(filename):
    # Ler o conteúdo do BytesIO
    content = filename.getvalue().decode('utf-8')
    
    # Salvar o conteúdo em um arquivo
    with open('texto.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(content)


def frequentes(arquivo, numero):
    # 1. Leia o arquivo de texto
    with open('texto.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    # 2. Tokenização
    translator = str.maketrans('', '', string.punctuation)
    words = [word.lower().translate(translator) for word in text.split()]

    with open('stop_words_brazil.txt', mode='r', encoding='utf-8') as file:
        stopw1 = [str(s.strip()) for s in file.readlines()]
    textos=[t for t in words if t.lower() not in stopw1 if len(t)>2]

    # 3. Contagem de palavras

    word_count = Counter(textos)

    # 4. Liste as palavras mais frequentes
    return word_count.most_common(numero)

try:
    filename=st.file_uploader('Insira seu arquivo txt', type='txt')

    f=bytestotext(filename)
    top_words = frequentes('texto.txt', numero)

except AttributeError:
    st.write('Aguardando o seu arquivo')

try:
    words, counts = zip(*top_words)

    
    plt.figure(figsize=(12,8))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Contagem')
    plt.ylabel('Palavras')
    plt.title(str(numero)+' Palavras mais frequentes')
    plt.gca().invert_yaxis()  # para exibir a palavra mais comum no topo
    st.pyplot(plt)

except NameError:
    st.write('Com seu arquivo vou mostrar um gráfico com as palavras mais frequentes')
