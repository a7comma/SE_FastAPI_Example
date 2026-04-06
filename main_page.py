import streamlit as st
from coloraide import Color
from streamlit import session_state as SST
from services.sentiment import SentimentService

page_title = "Эмоциональный тон текста"


def get_gradient_colors(label: str) -> list[str]:
    if label == "POSITIVE":
        basic_colors = ["#14532d", "#22c55e", "#bbf7d0"]
    elif label == "NEGATIVE":
        basic_colors = ["#7f1d1d", "#ef4444", "#fecaca"]
    else:
        basic_colors = ["#334155", "#64748b", "#cbd5e1"]

    gradient = Color.interpolate(basic_colors, space="srgb")

    return [
        gradient(0).to_string(hex=True),
        gradient(0.5).to_string(hex=True),
        gradient(1).to_string(hex=True),
    ]


def show_result_card(label: str, score: float) -> None:
    first_color, second_color, third_color = get_gradient_colors(label)

    if label == "POSITIVE":
        text_color = "#f0fdf4"
    elif label == "NEGATIVE":
        text_color = "#fff1f2"
    else:
        text_color = "#f8fafc"

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {first_color} 0%, {second_color} 55%, {third_color} 100%);
            border-radius: 22px;
            padding: 24px;
            margin-top: 16px;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.18);
            color: {text_color};
        ">
            <div style="font-size: 14px; opacity: 0.85; margin-bottom: 8px;">
                Результат анализа
            </div>
            <div style="font-size: 34px; font-weight: 700; margin-bottom: 10px;">
                {label}
            </div>
            <div style="font-size: 18px;">
                Вероятность: {score:.4f}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if "model" not in SST:
    SST.model = SentimentService()

st.title(page_title)

st.write("Это приложение позволяет анализировать эмоциональный тон текста.")

text = st.text_input("Введите текст для анализа", key="text")

if st.button("Анализировать"):
    st.write(f"Вы ввели: {text}")

    result = SST.model.analyze(text)
    st.write("Результат:")
    show_result_card(result[0]["label"], result[0]["score"])
