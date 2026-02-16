# Adyen Onboarding Research — Evidence Dashboard v2.0

> **Baza dowodowa dla The Adyen Context Layer**
> Zaktualizowano: Luty 2026 | Autor: Serafima

---

## 📋 Spis treści

1. [Opis projektu](#-opis-projektu)
2. [Struktura plików](#-struktura-plików)
3. [Instalacja](#-instalacja)
4. [Uruchomienie](#-uruchomienie)
5. [Dane i tabele](#-dane-i-tabele)
6. [Wykresy](#-wykresy)
7. [Źródła danych](#-źródła-danych)

---

## 📊 Opis projektu

Dashboard analityczny prezentujący kompleksową bazę dowodową na temat wyzwań onboardingowych w Adyen. Projekt łączy dane z:
- **Blind** (357 recenzji, 2024-2025)
- **Glassdoor** (880 recenzji, 2022-2025)
- **Taro/Jointaro** (community feedback)
- **Indeed**
- **DORA State of DevOps 2024**
- **Atlassian/DX Report 2024**
- **Adyen Annual Reports**
- Raporty konkurencji (Stripe, Klarna)

### Kluczowe wnioski:
1. **€10M+ rocznej straty** z powodu 6-miesięcznej luki w produktywności onboardingowej
2. **24% spadek revenue/FTE** w H1 2023 podczas intensywnego zatrudniania
3. **Context Deficit** (dokumentacja + tribal knowledge) = #1 źródło problemów (24% negatywnych wzmianek)
4. **Manager Onboarding scored 1.3/5.0** (D-) na Comparably — najniższa ocena
5. **Adyen brakuje structured onboarding layer** w porównaniu do Stripe i Klarna

---

## 📁 Struktura plików

```
├── app.py                      # Główna aplikacja Streamlit
├── feedback_data.csv           # Dane sentiment_themes (13 tematów)
├── requirements.txt            # Zależności Python
├── README.md                   # Ta dokumentacja
├── adyen_research.db          # Baza SQLite (9 tabel, auto-generowana)
└── adyen_charts/              # Folder z wykresami
    ├── 01_radar_ratings.png
    ├── 02_rampup_gap.png
    ├── 03_sentiment_butterfly.png
    ├── 04_platform_heatmap.png
    ├── 05_revenue_per_fte.html       (⭐ FEATURED - interaktywny)
    ├── 06_knowledge_deficit_donut.png
    ├── 07_industry_benchmarks.html   (⭐ FEATURED - interaktywny)
    ├── 08_competitive_matrix.html    (⭐ FEATURED - interaktywny)
    ├── 09_timeline.png
    └── index.html                    (Galeria HTML)
```

---

## 🔧 Instalacja

### Wymagania:
- Python 3.8+
- pip

### Krok 1: Zainstaluj zależności

```bash
pip install -r requirements.txt
```

**Zawartość `requirements.txt`:**
```
streamlit
pandas
plotly
matplotlib
seaborn
numpy
```

*(sqlite3 jest wbudowane w Python)*

---

## 🚀 Uruchomienie

### Metoda 1: Aplikacja Streamlit (interaktywna)

```bash
streamlit run app.py
```

Aplikacja uruchomi się w przeglądarce (domyślnie: `http://localhost:8501`)

**Funkcje aplikacji:**
- ✅ Interaktywna nawigacja między 9 wykresami
- ✅ Sidebar z filtrowaniem
- ✅ Automatyczne generowanie bazy SQLite z 9 tabelami
- ✅ Eksport wykresów do `adyen_charts/`
- ✅ Adyen branding (kolory, fonty, watermarki)

### Metoda 2: Galeria HTML (statyczna)

Otwórz plik w przeglądarce:
```bash
open adyen_charts/index.html
```

lub (Linux):
```bash
xdg-open adyen_charts/index.html
```

**Funkcje galerii:**
- ✅ Responsywny design (desktop + mobile)
- ✅ Interaktywne wykresy Plotly (5, 7, 8) jako iframe
- ✅ Statyczne wykresy matplotlib (1, 2, 3, 4, 6, 9) jako PNG
- ✅ Tabela źródeł danych z linkami
- ✅ Alt-text dla accessibility

---

## 🗄️ Dane i tabele

Baza SQLite (`adyen_research.db`) zawiera **9 tabel**:

### 1. `platform_ratings`
Oceny z różnych platform (Blind, Glassdoor, Comparably, Indeed)
- **14 wierszy** × 6 kolumn
- Kolumny: `platform`, `category`, `score`, `max_score`, `review_count`, `date_range`

### 2. `rampup_data`
Dane o czasie wdrażania (ramp-up time)
- **8 wierszy** × 5 kolumn
- Kolumny: `metric`, `value_months`, `source`, `year`, `category`

### 3. `tech_academy_stats`
Statystyki Adyen Tech Academy
- **10 wierszy** × 3 kolumny
- Kolumny: `metric`, `value`, `category`

### 4. `sentiment_themes` *(z CSV)*
Analiza sentimentu z review platforms
- **13 wierszy** × 5 kolumn
- Kolumny: `theme`, `positive_mentions`, `negative_mentions`, `platform`, `year_range`

### 5. `key_quotes`
20 kluczowych cytatów z różnych źródeł
- **20 wierszy** × 6 kolumn
- Kolumny: `id`, `quote_text`, `sentiment`, `source`, `year`, `helpful_votes`

### 6. `revenue_per_fte`
Revenue per FTE w czasie (2021-2024)
- **7 wierszy** × 4 kolumny
- Kolumny: `period`, `revenue_eur_per_fte_monthly`, `fte_total`, `notes`

### 7. `headcount_growth`
Wzrost zatrudnienia (2019-2025E)
- **8 wierszy** × 5 kolumn
- Kolumny: `period`, `total_fte`, `engineers_approx`, `yoy_growth_pct`, `hiring_focus`

### 8. `industry_benchmarks`
Branżowe benchmarki (DORA, Atlassian, Cortex, SO)
- **13 wierszy** × 5 kolumn
- Kolumny: `metric`, `value`, `unit`, `source`, `year`

### 9. `competitive_landscape`
Rozwiązania konkurencji (Stripe, Klarna, Adyen)
- **7 wierszy** × 6 kolumn
- Kolumny: `company`, `solution_name`, `type`, `key_metric`, `year_launched`, `source`

---

## 📈 Wykresy

### ⭐ Featured Charts (interaktywne Plotly)

#### **Chart 5: The Financial Cost of Slow Onboarding**
- **Typ:** Dual-axis line chart
- **Dane:** `revenue_per_fte` + `headcount_growth`
- **Key Insight:** 24% spadek revenue/FTE w H1 2023 = €10M+ rocznej straty
- **Format:** HTML (interaktywny)

#### **Chart 7: Industry Benchmarks vs. Adyen Reality**
- **Typ:** Lollipop chart
- **Dane:** `industry_benchmarks`
- **Key Insight:** 69% devs traci 8+ hrs/tydzień, dokumentacja ma 12.8× multiplier
- **Format:** HTML (interaktywny)

#### **Chart 8: Competitive Landscape — FinTech Knowledge Management**
- **Typ:** Comparison matrix (Plotly Table)
- **Dane:** `competitive_landscape`
- **Key Insight:** Adyen ma DX + AI KB, ale brakuje structured onboarding layer
- **Format:** HTML (interaktywny)

### Pozostałe wykresy (statyczne matplotlib)

#### **Chart 1: Adyen Employee Ratings — Radar Chart**
- **Dane:** `platform_ratings` (Blind)
- **Key Insight:** Management najniżej (2.9/5.0)

#### **Chart 2: The Ramp-Up Gap**
- **Dane:** `rampup_data`
- **Key Insight:** 6-month gap = €10M+ annual loss

#### **Chart 3: Sentiment Analysis — What Engineers Talk About**
- **Dane:** `sentiment_themes`
- **Key Insight:** Documentation 21 negative vs 2 positive

#### **Chart 4: Platform Ratings Comparison — Heatmap**
- **Dane:** `platform_ratings`
- **Key Insight:** Comparably Manager Onboarding: 1.3/5.0 (D-)

#### **Chart 6: Knowledge Deficit Distribution**
- **Dane:** `sentiment_themes` (grouped)
- **Key Insight:** Context Deficit = 24% wszystkich negatywnych wzmianek

#### **Chart 9: Timeline of Evidence**
- **Dane:** Chronologia wydarzeń 2019-2025
- **Key Insight:** Problem dokumentacji nierozwiązany pomimo inwestycji

---

## 🔗 Źródła danych

### Primary Sources (employee feedback)
- **Blind** — 357 reviews (2024-2025)
- **Glassdoor** — 880 reviews (2022-2025), 57 SF office
- **Taro/Jointaro** — Senior Engineer posts
- **Indeed** — Employee ratings

### Industry Research
- **DORA State of DevOps 2024** — dora.dev
- **Atlassian/DX Report 2024** — Developer Experience research
- **Cortex State of Dev Prod 2024** — Productivity benchmarks
- **Stack Overflow Developer Survey 2024** — Global dev survey
- **Brandon Hall Group** — Onboarding research

### Company Sources
- **Adyen Tech Academy Blog** (2022) — Official targets
- **Adyen Annual Report 2024** — Revenue/FTE data
- **getdx.com case study** — DX Platform metrics
- **Andreu Mora SVP blog** (2025) — AI KB announcement

### Competitor Benchmarks
- **Stripe Sessions 2024** — /dev/start, Trailhead
- **Klarna press releases** — Kiki AI assistant
- **Wolf of Harcourt St** — FinTech analyst blog

---

## 🎨 Design Guidelines

### Kolory (Adyen Brand)
```python
ADYEN_GREEN = '#0ABF53'        # Primary brand color
ADYEN_DARK = '#1a1a2e'         # Text/headers
ADYEN_RED = '#E53935'          # Negative/problems
ADYEN_YELLOW = '#FFC107'       # Warnings/highlights
ADYEN_LIGHT_GREEN = '#E8F5E9'  # Backgrounds
ADYEN_GRAY = '#9E9E9E'         # Secondary text
```

### Watermark
Wszystkie wykresy matplotlib zawierają watermark:
```
Sources: Glassdoor/Blind/Taro/Indeed/Adyen Reports/DORA 2024 | Serafima, Feb 2026
```

### DPI
Wszystkie wykresy PNG generowane w **150 DPI** dla wysokiej jakości druku.

---

## 💡 Tips & Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'streamlit'`
**Rozwiązanie:**
```bash
pip install streamlit pandas plotly matplotlib seaborn numpy
```

### Problem: Wykresy nie generują się automatycznie
**Rozwiązanie:** Uruchom aplikację Streamlit i kliknij na każdy wykres w sidebar, aby wymusić generację.

### Problem: Baza SQLite jest pusta
**Rozwiązanie:** Usuń plik `adyen_research.db` i uruchom aplikację ponownie:
```bash
rm adyen_research.db
streamlit run app.py
```

### Problem: HTML gallery nie wyświetla wykresów Plotly
**Rozwiązanie:** Upewnij się, że pliki HTML (05, 07, 08) są w tym samym folderze co `index.html`.

---

## 📝 Changelog

### v2.0 (Luty 2026)
- ✅ Zastąpiono starą aplikację "Voice of the Learner"
- ✅ 9 nowych wykresów z danymi Adyen onboarding research
- ✅ Baza SQLite z 9 tabelami (auto-generowana)
- ✅ 3 interaktywne wykresy Plotly (Featured)
- ✅ Galeria HTML z responsywnym designem
- ✅ Pełna dokumentacja (README)

---

## 📧 Kontakt

**Autor:** Serafima
**Data:** Luty 2026
**Wersja:** 2.0

---

## 📄 Licencja

Projekt research/internal. Dane źródłowe są publicznie dostępne (Glassdoor, Blind, DORA, etc.).

---

**🚀 Powodzenia z prezentacją The Adyen Context Layer!**
