"""
Adyen Onboarding Research — Evidence Dashboard v2.0
Focus: 2024-2026 Data Only
Streamlit Application with Adyen Brand Identity (Dutch Design)
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sqlite3
import os

# ============================================
# ADYEN BRAND COLORS (Official Dutch Design)
# ============================================
ADYEN_MIDNIGHT = '#00112c'    # Primary text
ADYEN_SECONDARY = '#5c687c'   # Labels and secondary text
ADYEN_GREEN = '#0abf53'       # Brand accent, positive sentiment
ADYEN_BLUE = '#0070f5'        # Links and highlights
ADYEN_RED = '#e22d2d'         # Error states, negative sentiment
ADYEN_BG = '#f7f7f8'          # App background (light gray)
ADYEN_WHITE = '#ffffff'       # Card and container backgrounds
ADYEN_BORDER = '#e6e8eb'      # Subtle borders

DPI = 150  # High-quality chart export

# ============================================
# DATABASE INITIALIZATION (2024-2026 FOCUS)
# ============================================
@st.cache_resource
def init_database():
    """Initialize SQLite database with filtered data (2024-2026 only)"""
    conn = sqlite3.connect('adyen_research.db', check_same_thread=False)
    cursor = conn.cursor()

    # TABLE 1: platform_ratings (2024-2025 data)
    cursor.execute('DROP TABLE IF EXISTS platform_ratings')
    cursor.execute('''
        CREATE TABLE platform_ratings (
            platform TEXT,
            category TEXT,
            score REAL,
            max_score INTEGER,
            review_count INTEGER,
            date_range TEXT
        )
    ''')

    platform_ratings_data = [
        ('Blind', 'Overall', 3.5, 5, 357, '2024-2025'),
        ('Blind', 'Work Life Balance', 4.3, 5, 357, '2024-2025'),
        ('Blind', 'Management', 2.9, 5, 357, '2024-2025'),
        ('Blind', 'Career Growth', 3.0, 5, 357, '2024-2025'),
        ('Blind', 'Compensation', 3.8, 5, 357, '2024-2025'),
        ('Glassdoor_SF', 'Overall', 3.8, 5, 57, '2024-2025'),
        ('Glassdoor_SF', 'Work Life Balance', 4.1, 5, 57, '2024-2025'),
        ('Glassdoor_SF', 'Career Opportunities', 3.3, 5, 57, '2024-2025'),
        ('Comparably', 'Manager Onboarding', 1.3, 5, None, '2023-2024'),
        ('Glassdoor_PM', 'Overall', 3.3, 5, None, '2024-2025'),
        ('Indeed', 'Overall', 3.9, 5, None, '2024-2025')
    ]
    cursor.executemany('INSERT INTO platform_ratings VALUES (?,?,?,?,?,?)', platform_ratings_data)

    # TABLE 2: sentiment_themes (loaded from CSV, filtered to 2024-2026)
    cursor.execute('DROP TABLE IF EXISTS sentiment_themes')
    cursor.execute('''
        CREATE TABLE sentiment_themes (
            theme TEXT,
            positive_mentions INTEGER,
            negative_mentions INTEGER,
            platform TEXT,
            year_range TEXT
        )
    ''')

    # Load and filter CSV data for 2024-2026
    try:
        df_sentiment = pd.read_csv('feedback_data.csv')
        # Filter for recent data: keep rows where year_range contains 2024, 2025, or 2026
        df_sentiment_filtered = df_sentiment[
            df_sentiment['year_range'].str.contains('2024|2025|2026', na=False)
        ].copy()
        df_sentiment_filtered.to_sql('sentiment_themes', conn, if_exists='replace', index=False)
    except FileNotFoundError:
        st.error("feedback_data.csv not found. Please ensure the file exists.")
    except Exception as e:
        st.error(f"Error loading sentiment data: {str(e)}")

    conn.commit()
    return conn

# Initialize database
conn = init_database()

# ============================================
# CHART GENERATION FUNCTIONS
# ============================================

def create_chart_01_radar():
    """Chart 1: Radar Ratings - Blind Employee Reviews"""
    df = pd.read_sql_query("SELECT * FROM platform_ratings WHERE platform = 'Blind' AND category != 'Overall'", conn)

    if df.empty:
        st.warning("No Blind platform data available.")
        return None

    categories = df['category'].tolist()
    scores = df['score'].tolist()
    max_scores = df['max_score'].tolist()

    # Close the polygon
    categories_closed = categories + [categories[0]]
    scores_closed = scores + [scores[0]]

    # Create radar chart
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'}, dpi=DPI)

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles_closed = angles + [angles[0]]

    ax.plot(angles_closed, scores_closed, 'o-', linewidth=2, color=ADYEN_GREEN, label='Adyen Score')
    ax.fill(angles_closed, scores_closed, alpha=0.15, color=ADYEN_GREEN)

    ax.set_xticks(angles)
    ax.set_xticklabels(categories, fontsize=11, color=ADYEN_MIDNIGHT)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=9, color=ADYEN_SECONDARY)
    ax.grid(True, linestyle='--', alpha=0.3, color=ADYEN_SECONDARY)
    ax.set_facecolor(ADYEN_WHITE)
    ax.set_title('Chart 1: Adyen Employee Ratings (Blind, 2024-2025)',
                 fontsize=14, weight='600', pad=20, color=ADYEN_MIDNIGHT)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)

    plt.figtext(0.5, 0.02,
                'Data: Blind employee reviews (n=357) | Dashboard by Serafima, Feb 2026',
                ha='center', fontsize=8, color=ADYEN_SECONDARY)

    fig.patch.set_facecolor(ADYEN_WHITE)
    plt.tight_layout()

    # Save chart
    os.makedirs('adyen_charts', exist_ok=True)
    plt.savefig('adyen_charts/01_radar_ratings.png', dpi=DPI, bbox_inches='tight',
                facecolor=ADYEN_WHITE, edgecolor='none')

    return fig


def create_chart_02_sentiment():
    """Chart 2: Sentiment Butterfly - sorted best (top) to worst (bottom)"""
    # Read directly from CSV to avoid SQLite cache ordering issues
    try:
        df = pd.read_csv('feedback_data.csv')
    except FileNotFoundError:
        df = pd.read_sql_query("SELECT * FROM sentiment_themes", conn)

    if df.empty:
        st.warning("No sentiment data available.")
        return None

    # Compute sentiment ratio: higher = more positive, lower = more negative
    df['total'] = df['positive_mentions'] + df['negative_mentions']
    df['sentiment_ratio'] = df['positive_mentions'] / df['total'].replace(0, 1)

    # Sort: WORST (most negative) at index 0 → renders at BOTTOM of chart
    # BEST (most positive) at last index → renders at TOP
    df = df.sort_values('sentiment_ratio', ascending=True).reset_index(drop=True)

    themes = df['theme'].tolist()
    positive = df['positive_mentions'].tolist()
    negative = [-x for x in df['negative_mentions'].tolist()]  # Negative values for left side

    y_pos = np.arange(len(themes))

    fig, ax = plt.subplots(figsize=(14, 8), dpi=DPI)

    # Create butterfly chart
    ax.barh(y_pos, positive, color=ADYEN_GREEN, alpha=0.8, label='Positive Mentions', height=0.7)
    ax.barh(y_pos, negative, color=ADYEN_RED, alpha=0.8, label='Negative Mentions', height=0.7)

    # Add value labels
    for i, (pos, neg) in enumerate(zip(positive, negative)):
        if pos > 0:
            ax.text(pos + max(positive)*0.01, i, str(int(pos)),
                   va='center', ha='left', fontsize=9, color=ADYEN_MIDNIGHT, weight='500')
        if neg < 0:
            ax.text(neg - abs(min(negative))*0.01, i, str(int(abs(neg))),
                   va='center', ha='right', fontsize=9, color=ADYEN_MIDNIGHT, weight='500')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(themes, fontsize=10, color=ADYEN_MIDNIGHT)
    ax.set_xlabel('Mentions (Negative ← | → Positive)', fontsize=11, weight='500', color=ADYEN_MIDNIGHT)
    ax.set_title('Chart 2: Sentiment Analysis - What Engineers Talk About',
                 fontsize=14, weight='600', pad=15, color=ADYEN_MIDNIGHT)
    ax.axvline(x=0, color=ADYEN_MIDNIGHT, linewidth=1.5, linestyle='-')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='x', alpha=0.15, color=ADYEN_SECONDARY)
    ax.set_facecolor(ADYEN_WHITE)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(ADYEN_BORDER)
    ax.spines['bottom'].set_color(ADYEN_BORDER)

    plt.figtext(0.5, 0.02,
                'Data: Sentiment themes from Blind/Glassdoor/Taro/Indeed (2024-2026) | Dashboard by Serafima, Feb 2026',
                ha='center', fontsize=8, color=ADYEN_SECONDARY)

    fig.patch.set_facecolor(ADYEN_WHITE)
    plt.tight_layout()

    # Save chart
    os.makedirs('adyen_charts', exist_ok=True)
    plt.savefig('adyen_charts/02_sentiment_butterfly.png', dpi=DPI, bbox_inches='tight',
                facecolor=ADYEN_WHITE, edgecolor='none')

    return fig


def create_chart_03_heatmap():
    """Chart 3: Platform Heatmap - Normalized Ratings Comparison"""
    df = pd.read_sql_query("SELECT * FROM platform_ratings", conn)

    if df.empty:
        st.warning("No platform ratings data available.")
        return None

    # Normalize scores to 0-100 scale
    df['normalized_score'] = (df['score'] / df['max_score']) * 100

    # Create pivot table
    pivot_table = df.pivot_table(values='normalized_score', index='platform', columns='category', aggfunc='first')
    pivot_table = pivot_table.fillna(0)

    fig, ax = plt.subplots(figsize=(14, 6), dpi=DPI)

    sns.heatmap(pivot_table, annot=True, fmt='.1f', cmap='RdYlGn',
                cbar_kws={'label': 'Normalized Score (%)'},
                linewidths=1, linecolor=ADYEN_BORDER, ax=ax,
                vmin=0, vmax=100,
                annot_kws={'fontsize': 10, 'weight': '500', 'color': ADYEN_MIDNIGHT})

    ax.set_title('Chart 3: Platform Ratings Comparison - Normalized Scores',
                 fontsize=14, weight='600', pad=15, color=ADYEN_MIDNIGHT)
    ax.set_xlabel('Category', fontsize=11, weight='500', color=ADYEN_MIDNIGHT)
    ax.set_ylabel('Platform', fontsize=11, weight='500', color=ADYEN_MIDNIGHT)
    ax.tick_params(axis='both', colors=ADYEN_MIDNIGHT, labelsize=10)

    plt.figtext(0.5, 0.02,
                'Data: Aggregated platform ratings normalized to 0-100 scale | Dashboard by Serafima, Feb 2026',
                ha='center', fontsize=8, color=ADYEN_SECONDARY)

    fig.patch.set_facecolor(ADYEN_WHITE)
    plt.tight_layout()

    # Save chart
    os.makedirs('adyen_charts', exist_ok=True)
    plt.savefig('adyen_charts/03_platform_heatmap.png', dpi=DPI, bbox_inches='tight',
                facecolor=ADYEN_WHITE, edgecolor='none')

    return fig


def create_chart_04_keywords():
    """Chart 4: Tag Cloud - clean 3-row grid, no overlaps, Adyen branded"""

    onboarding_data = {
        "Thrown into the deep end": 48,
        "Tribal knowledge hoarding": 45,
        "Lack of structured training": 42,
        "Zero guidance for new joiners": 40,
        "Outdated documentation": 38,
        "No feedback loop": 35,
        "Office politics over skill": 32,
        "Figure it out yourself": 30,
        "Overwhelmed by context switching": 28,
        "Lack of technical context": 25,
        "Fake politeness culture": 22,
        "Trial by fire onboarding": 20,
        "No dedicated mentorship": 18,
        "Chaotic onboarding process": 15,
        "Generic / Irrelevant training": 12,
    }

    min_c = min(onboarding_data.values())
    max_c = max(onboarding_data.values())

    def lerp_color(c):
        """Light mint #a8e6c1 → Adyen green #0abf53"""
        t = (c - min_c) / (max_c - min_c)
        r = int(0xa8 + t * (0x0a - 0xa8))
        g = int(0xe6 + t * (0xbf - 0xe6))
        b = int(0xc1 + t * (0x53 - 0xc1))
        return f'#{r:02x}{g:02x}{b:02x}'

    def lerp_size(c):
        t = (c - min_c) / (max_c - min_c)
        return 11 + t * 14   # 11pt → 25pt

    # Sort largest first
    sorted_items = sorted(onboarding_data.items(), key=lambda x: x[1], reverse=True)

    # 3-row layout: row 0 (top) = 4 items, row 1 (mid) = 6, row 2 (bot) = 5
    row_groups = [sorted_items[0:4], sorted_items[4:10], sorted_items[10:15]]
    y_centers  = [0.78, 0.50, 0.22]   # paper coords

    fig, ax = plt.subplots(figsize=(14, 6), dpi=DPI)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    for group, y_c in zip(row_groups, y_centers):
        n = len(group)
        xs = [(j + 1) / (n + 1) for j in range(n)]
        for (phrase, count), x in zip(group, xs):
            ax.text(x, y_c, phrase,
                    fontsize=lerp_size(count),
                    color=lerp_color(count),
                    fontweight='bold' if count >= 38 else ('semibold' if count >= 28 else 'normal'),
                    ha='center', va='center',
                    transform=ax.transAxes,
                    wrap=False)

    # Title (via fig.text so it doesn't shift axes)
    fig.text(0.5, 0.94,
             'Chart 4: Top Onboarding Issues — Tag Cloud',
             ha='center', va='top',
             fontsize=14, fontweight='600', color=ADYEN_MIDNIGHT)

    fig.text(0.5, 0.03,
             'Tag size & colour intensity = mention frequency  |  Darker green = mentioned more often\n'
             'Data: Employee feedback 2024-2026 | Dashboard by Serafima, Feb 2026',
             ha='center', va='bottom', fontsize=7.5, color=ADYEN_SECONDARY, linespacing=1.5)

    plt.subplots_adjust(left=0, right=1, top=0.90, bottom=0.10)

    os.makedirs('adyen_charts', exist_ok=True)
    plt.savefig('adyen_charts/04_top_keywords.png', dpi=DPI, bbox_inches='tight',
                facecolor='#ffffff', edgecolor='none')

    # Also try to produce an interactive Plotly version if plotly available
    try:
        import plotly.graph_objects as go

        annotations = []
        for group, y_c in zip(row_groups, y_centers):
            n = len(group)
            xs = [(j + 1) / (n + 1) for j in range(n)]
            for (phrase, count), x in zip(group, xs):
                t = (count - min_c) / (max_c - min_c)
                ri = int(0xa8 + t * (0x0a - 0xa8))
                gi = int(0xe6 + t * (0xbf - 0xe6))
                bi = int(0xc1 + t * (0x53 - 0xc1))
                annotations.append(dict(
                    x=x, y=y_c,
                    text=f"<b>{phrase}</b>" if count >= 38 else phrase,
                    showarrow=False,
                    font=dict(size=int(14 + t * 22), color=f'rgb({ri},{gi},{bi})',
                              family='Inter, Arial, sans-serif'),
                    xanchor='center', yanchor='middle',
                    xref='paper', yref='paper'
                ))

        pfig = go.Figure()
        pfig.update_layout(
            annotations=annotations,
            xaxis=dict(visible=False, range=[0, 1]),
            yaxis=dict(visible=False, range=[0, 1]),
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=20, r=20, t=60, b=50), height=460,
            title=dict(text='Chart 4: Top Onboarding Issues — Tag Cloud',
                       font=dict(size=16, color='#00112c', family='Inter, Arial, sans-serif'),
                       x=0.5, xanchor='center')
        )
        pfig.write_html('adyen_charts/04_top_keywords.html',
                        include_plotlyjs='cdn', full_html=True)
    except ImportError:
        pass  # plotly optional – PNG already saved above

    return fig


# ============================================
# STREAMLIT APP CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Adyen Onboarding Research Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CRITICAL: FORCE LIGHT THEME (Fix Invisible Text)
# ============================================
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
    /* ── App background ── */
    .stApp {
        background-color: #f7f7f8 !important;
    }
    h1, h2, h3, p, span, li, div, label, .stMarkdown {
        color: #00112c !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stPlotlyChart, .stPyplot {
        background-color: #ffffff !important;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e6e8eb !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label {
        color: #00112c !important;
    }

    /* ── Fix: hide "keyboard_double_arrow" text in sidebar collapse button ── */
    /* Streamlit renders Material Icon names as raw text when font fails to load.
       We replace the broken text with a CSS arrow using ::before pseudo-element. */
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"] button,
    button[data-testid="baseButton-header"] {
        font-size: 0 !important;          /* hide the raw icon text */
        color: transparent !important;
        background: transparent !important;
        border: none !important;
        width: 2rem !important;
        height: 2rem !important;
        padding: 0 !important;
        cursor: pointer !important;
        position: relative !important;
    }
    [data-testid="stSidebarCollapseButton"] button::before,
    [data-testid="collapsedControl"] button::before,
    button[data-testid="baseButton-header"]::before {
        content: "‹" !important;         /* clean HTML arrow instead */
        font-size: 1.4rem !important;
        color: #5c687c !important;
        font-family: 'Inter', sans-serif !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        line-height: 1 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #0abf53 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton > button:hover {
        background-color: #089944 !important;
        box-shadow: 0 4px 8px rgba(10, 191, 83, 0.2) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #e6e8eb !important;
        color: #00112c !important;
    }

    /* ── Metrics ── */
    [data-testid="stMetricValue"] {
        color: #00112c !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #5c687c !important;
        font-size: 0.9rem !important;
    }

    /* ── Containers & alerts ── */
    .element-container {
        color: #00112c !important;
    }
    .stAlert {
        background-color: #ffffff !important;
        color: #00112c !important;
        border-left: 4px solid #0abf53 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR NAVIGATION
# ============================================
with st.sidebar:
    st.markdown(f"""
        <h1 style='color: {ADYEN_MIDNIGHT}; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;'>
            Adyen Onboarding Research
        </h1>
        <p style='color: {ADYEN_SECONDARY}; font-size: 0.9rem; margin-bottom: 2rem;'>
            Evidence Dashboard v2.0<br>
            Focus: 2024-2026 Data
        </p>
    """, unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: {ADYEN_MIDNIGHT}; font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem;'>Navigation</h3>",
                unsafe_allow_html=True)

    selected_chart = st.selectbox(
        "Select Chart",
        [
            "Chart 1: Radar Ratings",
            "Chart 2: Sentiment Butterfly",
            "Chart 3: Platform Heatmap",
            "Chart 4: Top Onboarding Issues"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Data sources info
    st.markdown(f"""
        <div style='padding: 1rem; background-color: {ADYEN_BG}; border-radius: 8px; margin-top: 1rem;'>
            <h4 style='color: {ADYEN_MIDNIGHT}; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;'>
                Data Sources
            </h4>
            <ul style='color: {ADYEN_SECONDARY}; font-size: 0.8rem; line-height: 1.6; margin: 0; padding-left: 1.2rem;'>
                <li>Blind (n=357 reviews)</li>
                <li>Glassdoor (n=880 reviews)</li>
                <li>Indeed (n=195 reviews)</li>
                <li>Comparably (n=450 ratings)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(f"""
        <p style='color: {ADYEN_SECONDARY}; font-size: 0.75rem; text-align: center; margin-top: 2rem;'>
            Dashboard by Serafima<br>
            February 2026
        </p>
    """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT AREA
# ============================================

# Header
st.markdown(f"""
    <h1 style='color: {ADYEN_MIDNIGHT}; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;'>
        Adyen Onboarding Research Dashboard
    </h1>
    <p style='color: {ADYEN_SECONDARY}; font-size: 1.1rem; margin-bottom: 2rem;'>
        Evidence-based analysis of employee feedback (2024-2026 focus)
    </p>
""", unsafe_allow_html=True)

# Display selected chart
if selected_chart == "Chart 1: Radar Ratings":
    st.markdown(f"""
        <h2 style='color: {ADYEN_MIDNIGHT}; font-size: 1.8rem; font-weight: 600; margin-bottom: 1rem;'>
            Chart 1: Employee Ratings (Blind Platform)
        </h2>
        <p style='color: {ADYEN_SECONDARY}; font-size: 1rem; margin-bottom: 1.5rem;'>
            Radar chart showing Adyen employee ratings across key categories from Blind platform reviews (n=357, 2024-2025).
        </p>
    """, unsafe_allow_html=True)

    with st.spinner("Generating radar chart..."):
        fig = create_chart_01_radar()
        if fig:
            st.pyplot(fig)
            plt.close()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Work Life Balance", "4.3/5", "Highest Rated")
    with col2:
        st.metric("Management", "2.9/5", "Lowest Rated")
    with col3:
        st.metric("Compensation", "3.8/5", "Above Average")
    with col4:
        st.metric("Career Growth", "3.0/5", "Below Average")

elif selected_chart == "Chart 2: Sentiment Butterfly":
    st.markdown(f"""
        <h2 style='color: {ADYEN_MIDNIGHT}; font-size: 1.8rem; font-weight: 600; margin-bottom: 1rem;'>
            Chart 2: Sentiment Analysis
        </h2>
        <p style='color: {ADYEN_SECONDARY}; font-size: 1rem; margin-bottom: 1.5rem;'>
            Butterfly chart comparing positive vs. negative mentions across key themes (2024-2026 data).
        </p>
    """, unsafe_allow_html=True)

    with st.spinner("Generating sentiment analysis..."):
        fig = create_chart_02_sentiment()
        if fig:
            st.pyplot(fig)
            plt.close()

    st.info("Green bars = positive mentions, red bars = negative. Sorted from best-rated (top) to worst-rated (bottom). Bar length = frequency.")

elif selected_chart == "Chart 3: Platform Heatmap":
    st.markdown(f"""
        <h2 style='color: {ADYEN_MIDNIGHT}; font-size: 1.8rem; font-weight: 600; margin-bottom: 1rem;'>
            Chart 3: Platform Ratings Comparison
        </h2>
        <p style='color: {ADYEN_SECONDARY}; font-size: 1rem; margin-bottom: 1.5rem;'>
            Heatmap showing normalized scores (0-100%) across different review platforms and categories.
        </p>
    """, unsafe_allow_html=True)

    with st.spinner("Generating platform comparison heatmap..."):
        fig = create_chart_03_heatmap()
        if fig:
            st.pyplot(fig)
            plt.close()

    st.info("All scores normalized to 0-100% scale for fair comparison across platforms. Green = higher scores, Red = lower scores.")

elif selected_chart == "Chart 4: Top Onboarding Issues":
    st.markdown(f"""
        <h2 style='color: {ADYEN_MIDNIGHT}; font-size: 1.8rem; font-weight: 600; margin-bottom: 1rem;'>
            Chart 4: Top Onboarding Issues
        </h2>
        <p style='color: {ADYEN_SECONDARY}; font-size: 1rem; margin-bottom: 1.5rem;'>
            Tag cloud showing onboarding and learning challenges from employee feedback (2024-2026). Larger and darker tags = mentioned more frequently.
        </p>
    """, unsafe_allow_html=True)

    with st.spinner("Generating onboarding issues tag cloud..."):
        fig = create_chart_04_keywords()
        if fig:
            st.pyplot(fig)
            plt.close()

    # Key insights
    st.markdown(f"""
        <div style='padding: 1.5rem; background-color: {ADYEN_WHITE}; border-radius: 8px; border-left: 4px solid {ADYEN_GREEN}; margin-top: 1.5rem;'>
            <h3 style='color: {ADYEN_MIDNIGHT}; font-size: 1.2rem; font-weight: 600; margin-bottom: 0.8rem;'>
                Key Insights
            </h3>
            <ul style='color: {ADYEN_SECONDARY}; font-size: 1rem; line-height: 1.8; margin: 0; padding-left: 1.5rem;'>
                <li><strong>Top Issue:</strong> "Thrown into the deep end (Sink or Swim)" - mentioned 48 times</li>
                <li><strong>Second Issue:</strong> "Tribal knowledge hoarding" - mentioned 45 times</li>
                <li><strong>Third Issue:</strong> "Lack of structured training" - mentioned 42 times</li>
                <li><strong>Pattern:</strong> Clear gap in structured onboarding and knowledge sharing processes</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; color: {ADYEN_SECONDARY}; font-size: 0.85rem; padding: 2rem 0 1rem 0;'>
        <p style='margin-bottom: 0.5rem;'>
            <strong>Adyen Onboarding Research Dashboard v2.0</strong>
        </p>
        <p style='margin: 0;'>
            Data sources: Blind, Glassdoor, Indeed, Comparably | Focus: 2024-2026 | Dashboard by Serafima, February 2026
        </p>
    </div>
""", unsafe_allow_html=True)
