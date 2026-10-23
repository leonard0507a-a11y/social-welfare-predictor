import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# =====================================================
# НАСТРОЙКА СТРАНИЦЫ
# =====================================================
st.set_page_config(
    page_title="SocialWelfarePredictorKZ",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# МУЛЬТИЯЗЫЧНОСТЬ
# =====================================================
lang_options = {"Русский": "ru", "English": "en", "Қазақша": "kk"}
selected_lang = st.sidebar.selectbox("🌐 Тіл / Language / Язык", options=list(lang_options.keys()))
lang = lang_options[selected_lang]

translations = {
    "ru": {
        "title": "SocialWelfarePredictorKZ",
        "subtitle": "Прототип системы предиктивной оценки нуждаемости в социальных услугах",
        "citizen_data": "Данные гражданина",
        "age": "Возраст (лет)",
        "region": "Регион",
        "income": "Среднемесячный доход на члена семьи (тенге)",
        "family_size": "Количество членов семьи",
        "digital_literacy": "Уровень цифровой грамотности (1-5)",
        "predict": "Рассчитать прогноз нуждаемости",
        "results": "Результаты прогноза",
        "recommended_services": "Рекомендуемые социальные услуги",
        "map_title": "Карта цифровой зрелости регионов",
        "satisfaction_title": "Результаты опроса граждан (n=1200)",
        "risk_low": "Низкий риск",
        "risk_medium": "Средний риск",
        "risk_high": "Высокий риск"
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
        "risk_low": "Low risk",
        "risk_medium": "Medium risk",
        "risk_high": "High risk"
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
        "risk_low": "Төмен қауіп",
        "risk_medium": "Орташа қауіп",
        "risk_high": "Жоғары қауіп"
    }
}

t = translations[lang]

# =====================================================
# РЕАЛЬНЫЕ ДАННЫЕ ПО РЕГИОНАМ КАЗАХСТАНА
# =====================================================

regions_data = pd.DataFrame({
    "Регион": [
        "г. Астана", "г. Алматы", "г. Шымкент",
        "Абай обл.", "Акмолинская обл.", "Актюбинская обл.",
        "Алматинская обл.", "Атырауская обл.", "Западно-Казахстанская обл.",
        "Жамбылская обл.", "Жетісу обл.", "Карагандинская обл.",
        "Костанайская обл.", "Кызылординская обл.", "Мангистауская обл.",
        "Павлодарская обл.", "Северо-Казахстанская обл.", "Туркестанская обл.",
        "Ұлытау обл.", "Восточно-Казахстанская обл."
    ],
    "Цифровая грамотность (%)": [
        97.61, 95.96, 91.60, 90.07, 91.41, 92.58,
        92.01, 85.51, 86.27, 87.01, 85.19, 90.50,
        92.30, 88.25, 87.03, 89.53, 79.62, 93.43,
        90.65, 90.28
    ],
    "Доступ к интернету (%)": [
        96.55, 95.21, 99.26, 93.25, 97.74, 94.52,
        94.63, 93.13, 92.01, 92.82, 92.21, 95.53,
        93.86, 89.19, 98.17, 98.02, 97.22, 98.89,
        97.15, 98.93
    ],
    "lat": [
        51.17, 43.25, 42.33, 50.41, 51.91, 50.28,
        43.90, 47.12, 51.22, 42.90, 45.00, 49.97,
        53.22, 44.85, 43.65, 52.28, 54.90, 42.32,
        48.00, 49.95
    ],
    "lon": [
        71.45, 76.95, 69.60, 80.26, 71.37, 57.17,
        77.02, 51.92, 51.38, 71.37, 78.00, 72.79,
        63.62, 65.50, 51.20, 76.97, 69.18, 69.60,
        67.00, 82.61
    ]
})

regions_data["Интегральный индекс"] = (
    regions_data["Цифровая грамотность (%)"] * 0.5 +
    regions_data["Доступ к интернету (%)"] * 0.5
).round(1)

def get_category(score):
    if score >= 90:
        return "Высокий (≥90%)"
    elif score >= 80:
        return "Средний (80-89%)"
    else:
        return "Низкий (<80%)"

regions_data["Категория"] = regions_data["Интегральный индекс"].apply(get_category)

color_map = {
    "Высокий (≥90%)": "#2ca02c",
    "Средний (80-89%)": "#ffcc00",
    "Низкий (<80%)": "#d62728"
}

regions_data["Размер"] = regions_data["Интегральный индекс"] / 2

region_list = regions_data["Регион"].tolist()

# =====================================================
# БОКОВАЯ ПАНЕЛЬ
# =====================================================
st.sidebar.header(f"📋 {t['citizen_data']}")

age = st.sidebar.slider(t["age"], 18, 90, 45)
region = st.sidebar.selectbox(t["region"], region_list)
income = st.sidebar.number_input(t["income"], min_value=0, value=85000, step=5000)
family_size = st.sidebar.slider(t["family_size"], 1, 10, 4)
digital_literacy = st.sidebar.slider(t["digital_literacy"], 1, 5, 3)

# =====================================================
# ОСНОВНАЯ ОБЛАСТЬ
# =====================================================
st.title(t["title"])
st.markdown(f"*{t['subtitle']}*")

tab1, tab2, tab3 = st.tabs(["🎯 " + t["results"], "🗺️ " + t["map_title"], "📊 " + t["satisfaction_title"]])

# ========== ВКЛАДКА 1 ==========
with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button(t["predict"], type="primary", use_container_width=True):
            risk = 0.28
            if income < 70000:
                risk += 0.32
            if family_size >= 5:
                risk += 0.20
            if age > 60:
                risk += 0.25
            if digital_literacy <= 2:
                risk += 0.18
            
            region_risk = regions_data[regions_data["Регион"] == region]["Интегральный индекс"].values
            if len(region_risk) > 0 and region_risk[0] < 85:
                risk += 0.15
            
            risk_score = round(min(0.97, risk), 2)
            
            if risk_score < 0.4:
                color = "green"
                risk_text = t["risk_low"]
            elif risk_score < 0.7:
                color = "orange"
                risk_text = t["risk_medium"]
            else:
                color = "red"
                risk_text = t["risk_high"]
            
            st.markdown(f"### {t['results']}")
            st.markdown(f"<h1 style='color:{color}; text-align:center;'>{risk_score:.0%}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;'>{risk_text}</p>", unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Вероятность нуждаемости", f"{risk_score:.0%}")
            with col_b:
                st.metric("Регион", region)
            with col_c:
                st.metric("Цифровая грамотность", f"{digital_literacy}/5")
            
            st.subheader(t["recommended_services"])
            services = [
                "✅ Адресная социальная помощь",
                "✅ Пособие по инвалидности",
                "✅ Технические средства реабилитации",
                "✅ Пособие на рождение ребёнка",
                "✅ Социальные услуги на дому",
                "✅ Лекарственное обеспечение (Social Wallet)",
                "✅ Школьное питание через ваучеры",
                "✅ Пособие по уходу за ребёнком"
            ]
            for service in services:
                st.write(service)
    
    with col2:
        st.markdown("### ℹ️ О методике расчёта")
        st.markdown("""
        **Интегральный индекс нуждаемости** рассчитывается на основе:
        
        | Фактор | Вклад |
        |--------|-------|
        | Низкий доход (<70 000 тг/чел) | +32% |
        | Пожилой возраст (>60 лет) | +25% |
        | Многодетная семья (≥5 чел) | +20% |
        | Низкая цифровая грамотность (1-2) | +18% |
        | Сложный регион (индекс <85%) | +15% |
        | Базовый риск | 28% |
        
        **Порог проактивного назначения:** риск >70%
        
        *Источник: авторская модель на основе данных опроса (n=1200) и экспертных интервью (n=30)*
        """)

# ========== ВКЛАДКА 2: КАРТА ==========
with tab2:
    st.markdown("## 🗺️ Интерактивная карта цифровой зрелости регионов Казахстана")
    st.markdown("*По данным Бюро национальной статистики РК за 2025 год*")
    
    with st.expander("ℹ️ О методике расчёта и источниках данных"):
        st.markdown("""
        **Интегральный индекс цифровой зрелости региона** рассчитан по формуле:
        
        `Индекс = (Цифровая грамотность × 0.5) + (Доступ к интернету × 0.5)`
        
        **Источники данных (Бюро национальной статистики РК, 2025 г.):**
        - Уровень цифровой грамотности населения (возраст 6-74 лет)
        - Доля пользователей сети Интернет (возраст 16-74 лет)
        
        **Цветовая индикация:**
        - 🟢 Зелёный — высокий уровень (≥90%)
        - 🟡 Жёлтый — средний уровень (80-89%)
        - 🔴 Красный — низкий уровень (<80%)
        """)
    
    fig_map = px.scatter_map(
        regions_data,
        lat="lat",
        lon="lon",
        color="Категория",
        color_discrete_map=color_map,
        size="Размер",
        size_max=25,
        hover_name="Регион",
        hover_data={
            "Интегральный индекс": ":.1f",
            "Цифровая грамотность (%)": ":.1f",
            "Доступ к интернету (%)": ":.1f",
            "lat": False,
            "lon": False,
            "Размер": False
        },
        zoom=4.5,
        center={"lat": 48.5, "lon": 68.0},
        height=600,
        title="<b>Цифровая зрелость регионов Казахстана (2025)</b>"
    )
    fig_map.update_layout(
        map_style="carto-positron",
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        top5 = regions_data.nlargest(5, "Интегральный индекс")[["Регион", "Интегральный индекс"]]
        fig_top5 = px.bar(
            top5, x="Регион", y="Интегральный индекс", text="Интегральный индекс",
            color="Интегральный индекс", color_continuous_scale="Greens",
            title="🏆 Топ-5 регионов по цифровой зрелости"
        )
        fig_top5.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_top5.update_layout(yaxis_range=[0, 100], height=400, showlegend=False)
        st.plotly_chart(fig_top5, use_container_width=True)
    
    with col2:
        bottom5 = regions_data.nsmallest(5, "Цифровая грамотность (%)")[["Регион", "Цифровая грамотность (%)"]]
        fig_bottom = px.bar(
            bottom5, x="Регион", y="Цифровая грамотность (%)", text="Цифровая грамотность (%)",
            color="Цифровая грамотность (%)", color_continuous_scale="Reds",
            title="⚠️ Регионы с наименьшей цифровой грамотностью"
        )
        fig_bottom.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_bottom.update_layout(yaxis_range=[0, 100], height=400, showlegend=False)
        st.plotly_chart(fig_bottom, use_container_width=True)
    
    with st.expander("📋 Полная таблица данных по регионам"):
        st.dataframe(
            regions_data[["Регион", "Интегральный индекс", "Категория", "Цифровая грамотность (%)", "Доступ к интернету (%)"]],
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("### 📌 Ключевые показатели")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Средний индекс по РК", f"{regions_data['Интегральный индекс'].mean():.1f}%")
    with col2:
        st.metric("Средняя цифровая грамотность", f"{regions_data['Цифровая грамотность (%)'].mean():.1f}%")
    with col3:
        st.metric("Средний доступ к интернету", f"{regions_data['Доступ к интернету (%)'].mean():.1f}%")
    with col4:
        high_regions = len(regions_data[regions_data["Категория"] == "Высокий (≥90%)"])
        st.metric("Регионов с высоким уровнем", high_regions)
    
    st.markdown("---")
    st.markdown("""
    **Аналитическое резюме:**
    
    1. **Лидеры** — города республиканского значения (Астана, Алматы, Шымкент), индекс >90%.
    2. **Наибольшее отставание** — Северо-Казахстанская область (79.6%).
    3. **Ключевой фактор** — низкая цифровая грамотность в сельских регионах.
    4. **Разрыв между регионами** — 18 процентных пунктов.
    
    *Источник: расчёты автора на основе данных БНС РК, 2025 г.*
    """)

# ========== ВКЛАДКА 3 ==========
with tab3:
    st.markdown("## 📊 Результаты социологического исследования")
    
    survey_df = pd.DataFrame({
        "Показатель": ["Удовлетворённость электронными услугами", "Полностью автоматизированные услуги", "Проактивные услуги"],
        "Значение (%)": [68, 35, 15],
        "Целевой показатель (2030)": [85, 70, 50]
    })
    
    fig_survey = px.bar(
        survey_df, x="Показатель", y="Значение (%)", text="Значение (%)",
        color="Показатель", title="Оценка текущего состояния цифровизации социальных услуг (опрос n=1200)"
    )
    fig_survey.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
    fig_survey.update_layout(yaxis_range=[0, 100], height=450, showlegend=False)
    st.plotly_chart(fig_survey, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **📌 Ключевые выводы опроса (n=1200):**
        - 68% граждан удовлетворены услугами
        - 73% доверяют защите данных
        - 70% готовы к проактивным услугам
        - 73% поддерживают ИИ при контроле человека
        """)
    with col2:
        st.markdown("""
        **⚠️ Основные барьеры:**
        - Недостаток навыков — 35%
        - Нет доступа к интернету — 28%
        - Опасения за данные — 22%
        - Недоверие к сервисам — 18%
        """)
    
    st.markdown("---")
    st.caption("Источник: авторский опрос населения (n=1200, 2024-2025) и экспертные интервью (n=30, 2025)")

st.markdown("---")
st.caption(f"SocialWelfarePredictorKZ © 2026 | {t['title']} | Диссертационное исследование Л.Б. Тюлюгеновой")
st.caption("Источники данных: Бюро национальной статистики РК (2025), авторский опрос населения (n=1200, 2024-2025)")
