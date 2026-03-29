import streamlit as st
from streamlit import session_state as SST
from services.sentiment import SentimentService

page_title = "Эмоциональный тон текста"

if "model" not in SST:
    SST.model = SentimentService()

st.title(page_title)

st.write("Это приложение позволяет анализировать эмоциональный тон текста.")

text = st.text_input("Введите текст для анализа", key="text")


if st.button("Анализировать"):
    st.write(f"Вы ввели: {text}")

    result = SST.model.analyze(text)
    st.write("Результат:")
    st.success(result[0]["label"])
    st.write("Вероятность: " + str(result[0]["score"]))
