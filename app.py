import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="SocialWelfarePredictorKZ", layout="wide", page_icon="🛡️")

# ================== ЯЗЫКИ ==================
languages = {
    "Русский": "ru",
    "English": "en",
    "Қазақша": "kk"
}

selected_lang = st.sidebar.selectbox("🌐 Тіл / Language / Язык", options=list(languages.keys()))
lang_code = languages[selected_lang]

# Переводы
t = {
    "ru": {
        "title": "SocialWelfarePredictorKZ",
        "subtitle": "Прототип системы предиктивной оценки нуждаемости в социальных услугах Казахстана",
        "citizen_data": "Данные гражданина",
        "age": "Возраст (лет)",
        "region": "Регион",
        "income": "Среднемесячный доход на члена семьи (тенге)",
        "family_size": "Количество членов семьи",
        "digital_literacy": "Уровень цифровой грамотности (1-5)",
        "predict": "Рассчитать прогноз нуждаемости",
        "results": "Результаты прогноза",
        "services": "Рекомендуемые социальные услуги",
        "map": "Карта регионов Казахстана (уровень цифровой зрелости)",
        "satisfaction": "Результаты социологического опроса (n=1200)",
    },
    "en": {
        "title": "SocialWelfarePredictorKZ",
        "subtitle": "Prototype of Predictive Social Needs Assessment System in Kazakhstan",
        "citizen_data": "Citizen Data",
        "age": "Age (years)",
        "region": "Region",
        "income": "Average monthly income per family member (tenge)",
        "family_size": "Family size",
        "digital_literacy": "Digital literacy level (1-5)",
        "predict": "Calculate Needs Prediction",
        "results": "Prediction Results",
        "services": "Recommended Social Services",
        "map": "Map of Kazakhstan Regions (Digital Maturity)",
        "satisfaction": "Survey Results (n=1200)",
    },
    "kk": {
        "title": "SocialWelfarePredictorKZ",
        "subtitle": "Әлеуметтік қызметтерге мұқтаждықты болжау жүйесінің прототипі",
        "citizen_data": "Азамат туралы мәліметтер",
        "age": "Жасы (жыл)",
        "region": "Аймақ",
        "income": "Отбасы мүшесіне шаққандағы орташа айлық табыс (теңге)",
        "family_size": "Отбасы мүшелерінің саны",
        "digital_literacy": "Цифрлық сауаттылық деңгейі (1-5)",
        "predict": "Мұқтаждық болжамын есептеу",
        "results": "Болжам нәтижелері",
        "services": "Ұсынылатын әлеуметтік қызметтер",
        "map": "Қазақстан аймақтарының картасы (цифрлық жетілу деңгейі)",
        "satisfaction": "Сауалнама нәтижелері (n=1200)",
    }
}[lang_code]

# ================== БОКОВАЯ ПАНЕЛЬ ==================
st.sidebar.header("📋 " + t["citizen_data"])

age = st.sidebar.slider(t["age"], 18, 90, 45)
regions = ["Астана", "Алматы", "Шымкент", "Павлодарская обл.", "Карагандинская обл.", 
           "Восточно-Казахстанская обл.", "Алматинская обл.", "Туркестанская обл.", 
           "Мангистауская обл.", "Актюбинская обл.", "Северо-Казахстанская обл.", "Другие"]
region = st.sidebar.selectbox(t["region"], regions)

income = st.sidebar.number_input(t["income"], min_value=0, value=85000, step=5000)
family_size = st.sidebar.slider(t["family_size"], 1, 10, 4)
digital_literacy = st.sidebar.slider(t["digital_literacy"], 1, 5, 3)

# ================== ОСНОВНАЯ ЧАСТЬ ==================
st.title(t["title"])
st.subheader(t["subtitle"])
st.caption("Автор: Tyulyugenova L.B. | Диссертационное исследование, 2026")

if st.button(t["predict"], type="primary", use_container_width=True):
    # Простая, но реалистичная модель
    risk = 0.25
    if income < 70000: risk += 0.30
    if family_size >= 5: risk += 0.18
    if age > 60: risk += 0.22
    if digital_literacy <= 2: risk += 0.15
    if region in ["Туркестанская обл.", "Мангистауская обл.", "Актюбинская обл."]: risk += 0.12
    
    risk_score = round(min(0.98, risk), 2)

    st.success(f"**{t['results']}** — Вероятность нуждаемости: **{risk_score:.0%}**")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Вероятность нуждаемости", f"{risk_score:.0%}")
        st.metric("Уровень цифровой грамотности", f"{digital_literacy}/5")
    with col2:
        st.metric("Регион", region)
        st.metric("Доход на члена семьи", f"{income:,} ₸")

    # Рекомендуемые услуги
    st.subheader(t["services"])
    services = [
        "Адресная социальная помощь",
        "Пособие по инвалидности",
        "Технические средства реабилитации",
        "Пособие на рождение ребёнка",
        "Социальные услуги на дому",
        "Лекарственное обеспечение через Social Wallet",
        "Школьное питание (ваучеры)",
        "Пособие по уходу за ребёнком"
    ]
    
    recommended = [s for s in services if risk_score > 0.45]
    for service in recommended[:5]:
        st.write(f"✅ {service}")

    # Графики из диссертации
    st.subheader(t["satisfaction"])
    satisfaction_df = pd.DataFrame({
        "Показатель": ["Удовлетворённость электронными услугами", "Полностью автоматизированные процессы", "Проактивные услуги"],
        "Значение (%)": [68, 35, 15]
    })
    fig_bar = px.bar(satisfaction_df, x="Показатель", y="Значение (%)", text="Значение (%)", color="Показатель")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Карта регионов
    st.subheader(t["map"])
    map_data = pd.DataFrame({
        "Регион": ["Астана", "Алматы", "Шымкент", "Павлодарская", "Карагандинская", 
                   "Восточно-Казахстанская", "Алматинская", "Туркестанская", "Мангистауская"],
        "Цифровая зрелость (%)": [78, 76, 70, 68, 64, 61, 58, 48, 52],
        "lat": [51.17, 43.25, 42.33, 52.28, 49.97, 49.95, 43.90, 42.32, 43.65],
        "lon": [71.45, 76.95, 69.60, 76.97, 72.79, 82.61, 77.02, 69.60, 51.20]
    })

    fig_map = px.scatter_mapbox(map_data, lat="lat", lon="lon", 
                                color="Цифровая зрелость (%)",
                                size="Цифровая зрелость (%)",
                                hover_name="Регион",
                                color_continuous_scale=px.colors.sequential.Blues,
                                mapbox_style="carto-positron",
                                zoom=4.5, height=550)
    st.plotly_chart(fig_map, use_container_width=True)

    st.info("Прототип разработан в рамках диссертационного исследования Л.Б. Тюлюгеновой (2026). "
            "Может быть интегрирован с платформой Alem.ai или Социальным кошельком.")

# Нижняя информация
st.caption("© 2026 | Разработано как практическая апробация предиктивной модели (Глава 4.4)")