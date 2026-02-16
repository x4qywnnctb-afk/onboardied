# 🚀 Quick Start Guide
## Adyen Onboarding Research Dashboard v2.0

---

## ⚡ 3 kroki do uruchomienia

### 1️⃣ Zainstaluj zależności
```bash
pip install streamlit pandas plotly matplotlib seaborn numpy
```

### 2️⃣ Uruchom aplikację
```bash
cd "/path/to/voice of learner"
streamlit run app.py
```

### 3️⃣ Otwórz w przeglądarce
Aplikacja automatycznie otworzy się pod adresem: **http://localhost:8501**

---

## 📊 Co zobaczysz?

### Sidebar Navigation
Wybierz jeden z 9 wykresów:
- ⭐ **Chart 5:** Financial Cost (FEATURED)
- ⭐ **Chart 7:** Industry Benchmarks (FEATURED)
- ⭐ **Chart 8:** Competitive Landscape (FEATURED)
- **Chart 1:** Radar Ratings
- **Chart 2:** Ramp-Up Gap
- **Chart 3:** Sentiment Butterfly
- **Chart 4:** Platform Heatmap
- **Chart 6:** Knowledge Deficit
- **Chart 9:** Timeline

### Automatyczne generowanie
Po pierwszym uruchomieniu aplikacja:
1. ✅ Tworzy bazę SQLite (`adyen_research.db`) z 9 tabelami
2. ✅ Ładuje dane z `feedback_data.csv`
3. ✅ Generuje wykresy i zapisuje je do `adyen_charts/`

---

## 🌐 Alternatywa: Galeria HTML (bez instalacji)

Jeśli nie chcesz instalować zależności, otwórz:
```bash
open adyen_charts/index.html
```

**Uwaga:** Wykresy PNG muszą zostać wygenerowane przez aplikację Streamlit przynajmniej raz!

---

## 🛠️ Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit --user
```

### ❌ "Cannot connect to database"
Usuń starą bazę i uruchom ponownie:
```bash
rm adyen_research.db
streamlit run app.py
```

### ❌ "Charts not generated"
Kliknij na każdy wykres w sidebar, aby wymusić generację.

---

## 📁 Struktura po uruchomieniu

```
voice of learner/
├── app.py                          ✅ Główna aplikacja
├── feedback_data.csv              ✅ Dane sentiment
├── requirements.txt               ✅ Zależności
├── README.md                      ✅ Pełna dokumentacja
├── QUICKSTART.md                  ✅ Ten plik
├── adyen_research.db             🆕 Baza SQLite (auto)
└── adyen_charts/                 🆕 Folder wykresów
    ├── 01_radar_ratings.png      🆕
    ├── 02_rampup_gap.png         🆕
    ├── 03_sentiment_butterfly.png 🆕
    ├── 04_platform_heatmap.png   🆕
    ├── 05_revenue_per_fte.html   🆕 (interaktywny)
    ├── 06_knowledge_deficit_donut.png 🆕
    ├── 07_industry_benchmarks.html 🆕 (interaktywny)
    ├── 08_competitive_matrix.html 🆕 (interaktywny)
    ├── 09_timeline.png           🆕
    └── index.html                ✅ Galeria

🆕 = Generowane automatycznie
✅ = Dostarczone w projekcie
```

---

## 🎯 Najważniejsze wnioski (TL;DR)

1. **€10M+ rocznej straty** — 6-miesięczna luka w onboardingu
2. **24% spadek revenue/FTE** w H1 2023
3. **Context Deficit** (#1 problem) = 24% negatywnych wzmianek
4. **Manager Onboarding: 1.3/5.0** (Comparably) — najniższa ocena
5. **Adyen brakuje structured onboarding layer** vs konkurencja

---

## 📧 Masz pytania?

Zobacz pełną dokumentację: **README.md**

---

**Powodzenia! 🚀**
