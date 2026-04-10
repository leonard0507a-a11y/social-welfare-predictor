import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SocialWelfarePredictorKZ", layout="wide", page_icon="🛡️")

# Языки
lang_options = {"Русский": "ru", "English": "en", "Қазақша": "kk"}
selected_lang = st.sidebar.selectbox("🌐 Тіл / Language / Язык", options=list(lang_options.keys()))
lang = lang_options[selected_lang]

# Переводы (улучшенные)
translations = {
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
        "recommended_services": "Рекомендуемые социальные услуги",
        "map_title": "Карта регионов Казахстана (уровень цифровой зрелости)",
        "satisfaction_title": "Результаты опроса граждан (n=1200)",
    },
    "en": {
        "title": "SocialWelfarePredictorKZ",
        "subtitle": "Prototype of Predictive Social Needs Assessment System",
        "citizen_data": "Citizen Data",
        "age": "Age (years)",
        "region": "Region",
        "income": "Average monthly income per family member (tenge)",
        "family_size": "Family size",
        "digital_literacy": "Digital literacy level (1-5)",
        "predict": "Calculate Prediction",
        "results": "Prediction Results",
        "recommended_services": "Recommended Social Services",
        "map_title": "Map of Kazakhstan Regions (Digital Maturity)",
        "satisfaction_title": "Citizen Survey Results (n=1200)",
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
        "recommended_services": "Ұсынылатын әлеуметтік қызметтер",
        "map_title": "Қазақстан аймақтарының картасы (цифрлық жетілу деңгейі)",
        "satisfaction_title": "Азаматтар сауалнамасының нәтижелері (n=1200)",
    }
}

t = translations[lang]

# Боковая панель
st.sidebar.header("📋 " + t["citizen_data"])

age = st.sidebar.slider(t["age"], 18, 90, 45)
region_list = ["Астана", "Алматы", "Шымкент", "Павлодарская обл.", "Карагандинская обл.", 
               "Восточно-Казахстанская обл.", "Алматинская обл.", "Туркестанская обл.", 
               "Мангистауская обл.", "Актюбинская обл.", "Северо-Казахстанская обл."]
region = st.sidebar.selectbox(t["region"], region_list)

income = st.sidebar.number_input(t["income"], min_value=0, value=85000, step=5000)
family_size = st.sidebar.slider(t["family_size"], 1, 10, 4)
digital_literacy = st.sidebar.slider(t["digital_literacy"], 1, 5, 3)

if st.sidebar.button(t["predict"], type="primary", use_container_width=True):
    # Улучшенная модель
    risk = 0.28
    if income < 70000: risk += 0.32
    if family_size >= 5: risk += 0.20
    if age > 60: risk += 0.25
    if digital_literacy <= 2: risk += 0.18
    if region in ["Туркестанская обл.", "Мангистауская обл.", "Актюбинская обл."]: risk += 0.15
    
    risk_score = round(min(0.97, risk), 2)

    st.success(f"**{t['results']}**: Вероятность нуждаемости — **{risk_score:.0%}**")

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Вероятность нуждаемости", f"{risk_score:.0%}")
    with col2: st.metric("Регион", region)
    with col3: st.metric("Цифровая грамотность", f"{digital_literacy}/5")

    # Рекомендуемые услуги
    st.subheader(t["recommended_services"])
    services = [
        "Адресная социальная помощь",
        "Пособие по инвалидности",
        "Технические средства реабилитации",
        "Пособие на рождение ребёнка",
        "Социальные услуги на дому",
        "Лекарственное обеспечение (Social Wallet)",
        "Школьное питание через ваучеры",
        "Пособие по уходу за ребёнком"
    ]
    for service in services:
        st.write(f"✅ {service}")

    # Графики из диссертации
    st.subheader(t["satisfaction_title"])
    sat_df = pd.DataFrame({
        "Показатель": ["Удовлетворённость", "Полная автоматизация", "Проактивные услуги"],
        "Значение (%)": [68, 35, 15]
    })
    fig = px.bar(sat_df, x="Показатель", y="Значение (%)", text="Значение (%)", color="Показатель")
    st.plotly_chart(fig, use_container_width=True)

    # Карта регионов (улучшенная)
    st.subheader(t["map_title"])
    map_df = pd.DataFrame({
        "Регион": ["Астана", "Алматы", "Шымкент", "Павлодар", "Караганда", "ВКО", "Алматы обл.", "Туркестан", "Мангистау"],
        "Цифровая зрелость (%)": [78, 76, 71, 68, 65, 62, 59, 48, 53],
        "lat": [51.17, 43.25, 42.33, 52.28, 49.97, 49.95, 43.90, 42.32, 43.65],
        "lon": [71.45, 76.95, 69.60, 76.97, 72.79, 82.61, 77.02, 69.60, 51.20]
    })
    fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", color="Цифровая зрелость (%)",
                                size="Цифровая зрелость (%)", hover_name="Регион",
                                color_continuous_scale="Blues", mapbox_style="carto-positron", zoom=4.8, height=600)
    st.plotly_chart(fig_map, use_container_width=True)

    st.info("Прототип разработан Л.Б. Тюлюгеновой в рамках диссертации (2026). Может быть интегрирован с Alem.ai.")

st.caption("SocialWelfarePredictorKZ © 2026 | Диссертационное исследование")
