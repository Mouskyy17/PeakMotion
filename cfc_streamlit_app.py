import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# Configuration de la page
st.set_page_config(
    page_title="CFC Performance Insights",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour le style
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #034694, #1f5f99);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #034694;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("""
<div class="main-header">
    <h1>⚽ CFC PERFORMANCE INSIGHTS VIZATHON</h1>
    <p style="text-align: center; color: white; margin: 0;">SIMPLE | ILLUMINATING | ACTIONABLE</p>
</div>
""", unsafe_allow_html=True)

# Fonction pour générer des données GPS simulées
@st.cache_data
def generate_gps_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-07-01', end='2025-03-15', freq='D')
    
    # Filtrer pour avoir environ 3-4 sessions par semaine
    training_dates = []
    for date in dates:
        if np.random.random() < 0.5:  # 50% de chance d'avoir une session
            training_dates.append(date)
    
    n_sessions = len(training_dates)
    
    data = {
        'date': training_dates,
        'opposition_code': [f'OPP{np.random.randint(1, 20):02d}' if np.random.random() < 0.3 else 'TRAINING' for _ in range(n_sessions)],
        'opposition_full': ['Arsenal', 'Liverpool', 'Manchester City', 'Tottenham', 'Training Session'][np.random.choice(5, n_sessions)],
        'md_plus_code': [f'MD+{np.random.randint(1, 4)}' if np.random.random() < 0.3 else '' for _ in range(n_sessions)],
        'md_minus_code': [f'MD-{np.random.randint(1, 4)}' if np.random.random() < 0.3 else '' for _ in range(n_sessions)],
        'season': ['2023-24' if date < pd.Timestamp('2024-07-01') else '2024-25' for date in training_dates],
        'distance': np.random.normal(8500, 1500, n_sessions),
        'distance_over_21': np.random.normal(1200, 300, n_sessions),
        'distance_over_24': np.random.normal(800, 200, n_sessions),
        'distance_over_27': np.random.normal(400, 100, n_sessions),
        'accel_decel_over_2_5': np.random.randint(40, 120, n_sessions),
        'accel_decel_over_3_5': np.random.randint(20, 80, n_sessions),
        'accel_decel_over_4_5': np.random.randint(5, 40, n_sessions),
        'day_duration': np.random.randint(60, 120, n_sessions),
        'peak_speed': np.random.normal(32, 3, n_sessions),
        'hr_zone_1_hms': [f'{np.random.randint(5, 20):02d}:{np.random.randint(0, 59):02d}:{np.random.randint(0, 59):02d}' for _ in range(n_sessions)],
        'hr_zone_2_hms': [f'{np.random.randint(10, 30):02d}:{np.random.randint(0, 59):02d}:{np.random.randint(0, 59):02d}' for _ in range(n_sessions)],
        'hr_zone_3_hms': [f'{np.random.randint(15, 40):02d}:{np.random.randint(0, 59):02d}:{np.random.randint(0, 59):02d}' for _ in range(n_sessions)],
        'hr_zone_4_hms': [f'{np.random.randint(5, 25):02d}:{np.random.randint(0, 59):02d}:{np.random.randint(0, 59):02d}' for _ in range(n_sessions)],
        'hr_zone_5_hms': [f'{np.random.randint(0, 10):02d}:{np.random.randint(0, 59):02d}:{np.random.randint(0, 59):02d}' for _ in range(n_sessions)]
    }
    
    return pd.DataFrame(data)

# Fonction pour charger les données de capacité physique
@st.cache_data
def load_physical_capability_data():
    # Simuler le chargement du CSV
    data = """testDate,expression,movement,quality,benchmarkPct
12/11/2024,isometric,agility,rotate,0.6795
18/06/2024,isometric,agility,rotate,
19/12/2024,isometric,jump,take off,0.4
08/07/2023,isometric,jump,take off,
19/05/2024,isometric,jump,pre-load,0.49
11/02/2024,dynamic,agility,deceleration,0.89
28/03/2024,dynamic,upper body,push,0.4345
12/01/2024,dynamic,jump,take off,0.625
28/12/2024,isometric,upper body,pull,0.46
20/03/2024,dynamic,sprint,acceleration,0.4445
22/11/2024,isometric,agility,deceleration,0.86
29/10/2024,dynamic,sprint,max velocity,0.652
28/07/2024,isometric,agility,rotate,0.278
23/02/2024,isometric,agility,acceleration,0.52
08/01/2024,isometric,agility,rotate,
27/06/2024,dynamic,sprint,acceleration,0.436
10/11/2023,isometric,agility,deceleration,1.038
26/12/2023,dynamic,jump,pre-load,0.484
02/02/2025,dynamic,agility,acceleration,0.4965
30/01/2024,dynamic,upper body,push,0.4345"""
    
    return pd.read_csv(io.StringIO(data))

# Fonction pour générer des données de récupération simulées
@st.cache_data
def generate_recovery_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-07-01', end='2025-03-15', freq='D')
    
    n_days = len(dates)
    
    data = {
        'date': dates,
        'bio_completeness': np.random.uniform(0.7, 1.0, n_days),
        'bio_composite': np.random.normal(0, 0.2, n_days),
        'msk_joint_range_completeness': np.random.uniform(0.8, 1.0, n_days),
        'msk_joint_range_composite': np.random.normal(0, 0.15, n_days),
        'msk_load_tolerance_completeness': np.random.uniform(0.75, 1.0, n_days),
        'msk_load_tolerance_composite': np.random.normal(0, 0.18, n_days),
        'subjective_completeness': np.random.uniform(0.85, 1.0, n_days),
        'subjective_composite': np.random.normal(0, 0.25, n_days),
        'soreness_completeness': np.random.uniform(0.9, 1.0, n_days),
        'soreness_composite': np.random.normal(0, 0.2, n_days),
        'sleep_completeness': np.random.uniform(0.8, 1.0, n_days),
        'sleep_composite': np.random.normal(0, 0.3, n_days),
        'emboss_baseline_score': np.random.normal(0, 0.15, n_days)
    }
    
    return pd.DataFrame(data)

# Chargement des données
gps_data = generate_gps_data()
physical_data = load_physical_capability_data()
recovery_data = generate_recovery_data()

# Conversion des dates
gps_data['date'] = pd.to_datetime(gps_data['date'])
physical_data['testDate'] = pd.to_datetime(physical_data['testDate'])
recovery_data['date'] = pd.to_datetime(recovery_data['date'])

# Sidebar pour les filtres
st.sidebar.markdown("## 🎛️ Filtres et Contrôles")

# Filtre de date
date_range = st.sidebar.date_input(
    "Période d'analyse",
    value=(gps_data['date'].min().date(), gps_data['date'].max().date()),
    min_value=gps_data['date'].min().date(),
    max_value=gps_data['date'].max().date()
)

# Filtre de saison
seasons = st.sidebar.multiselect(
    "Saisons",
    options=gps_data['season'].unique(),
    default=gps_data['season'].unique()
)

# Onglets principaux
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'ensemble", 
    "🏃‍♂️ Données GPS", 
    "💪 Capacité Physique", 
    "😴 Statut de Récupération",
    "🎯 Zones Prioritaires"
])

# TAB 1: Vue d'ensemble
with tab1:
    st.markdown("### 📈 Tableau de Bord Performance")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_distance = gps_data['distance'].mean()
        st.metric(
            label="Distance Moyenne",
            value=f"{avg_distance:.0f} m",
            delta=f"{(avg_distance - 8000):.0f} vs objectif"
        )
    
    with col2:
        avg_peak_speed = gps_data['peak_speed'].mean()
        st.metric(
            label="Vitesse de Pointe Moy.",
            value=f"{avg_peak_speed:.1f} km/h",
            delta=f"{(avg_peak_speed - 30):.1f} vs référence"
        )
    
    with col3:
        recent_recovery = recovery_data['emboss_baseline_score'].tail(7).mean()
        recovery_status = "Excellent" if recent_recovery > 0.1 else "Bon" if recent_recovery > -0.1 else "Attention"
        st.metric(
            label="Score de Récupération",
            value=recovery_status,
            delta=f"{recent_recovery:.2f}"
        )
    
    with col4:
        physical_tests = physical_data['benchmarkPct'].dropna().count()
        st.metric(
            label="Tests Physiques",
            value=physical_tests,
            delta="Total effectués"
        )
    
    # Graphiques overview
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution de la charge d'entraînement
        fig_load = px.line(
            gps_data, 
            x='date', 
            y='distance',
            title="Évolution de la Distance Parcourue",
            color_discrete_sequence=['#034694']
        )
        fig_load.update_layout(
            xaxis_title="Date",
            yaxis_title="Distance (m)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_load, use_container_width=True)
    
    with col2:
        # Score de récupération
        fig_recovery = px.line(
            recovery_data.tail(30), 
            x='date', 
            y='emboss_baseline_score',
            title="Score de Récupération (30 derniers jours)",
            color_discrete_sequence=['#1f5f99']
        )
        fig_recovery.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_recovery.update_layout(
            xaxis_title="Date",
            yaxis_title="Score de Récupération",
            hovermode='x unified'
        )
        st.plotly_chart(fig_recovery, use_container_width=True)

# TAB 2: Données GPS
with tab2:
    st.markdown("### 🏃‍♂️ Analyse des Données GPS")
    
    # Filtrage des données GPS
    filtered_gps = gps_data[
        (gps_data['date'] >= pd.Timestamp(date_range[0])) & 
        (gps_data['date'] <= pd.Timestamp(date_range[1])) &
        (gps_data['season'].isin(seasons))
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des distances
        fig_dist = px.histogram(
            filtered_gps, 
            x='distance',
            nbins=20,
            title="Distribution des Distances Parcourues",
            color_discrete_sequence=['#034694']
        )
        fig_dist.update_layout(
            xaxis_title="Distance (m)",
            yaxis_title="Fréquence"
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        # Vitesses élevées par session
        fig_speed = px.scatter(
            filtered_gps,
            x='date',
            y='peak_speed',
            size='distance_over_27',
            color='opposition_code',
            title="Vitesse de Pointe vs Distance >27 km/h",
            hover_data=['distance', 'day_duration']
        )
        fig_speed.update_layout(
            xaxis_title="Date",
            yaxis_title="Vitesse de Pointe (km/h)"
        )
        st.plotly_chart(fig_speed, use_container_width=True)
    
    # Analyse des accélérations/décélérations
    st.markdown("#### Analyse des Accélérations/Décélérations")
    
    accel_data = filtered_gps[['date', 'accel_decel_over_2_5', 'accel_decel_over_3_5', 'accel_decel_over_4_5']].melt(
        id_vars=['date'], 
        var_name='threshold', 
        value_name='count'
    )
    
    fig_accel = px.line(
        accel_data,
        x='date',
        y='count',
        color='threshold',
        title="Évolution des Accélérations/Décélérations par Seuil"
    )
    fig_accel.update_layout(
        xaxis_title="Date",
        yaxis_title="Nombre d'Accélérations/Décélérations"
    )
    st.plotly_chart(fig_accel, use_container_width=True)
    
    # Zones de fréquence cardiaque
    st.markdown("#### Analyse des Zones de Fréquence Cardiaque")
    
    # Convertir les temps HMS en minutes pour l'analyse
    def hms_to_minutes(hms_str):
        try:
            h, m, s = map(int, hms_str.split(':'))
            return h * 60 + m + s / 60
        except:
            return 0
    
    hr_cols = ['hr_zone_1_hms', 'hr_zone_2_hms', 'hr_zone_3_hms', 'hr_zone_4_hms', 'hr_zone_5_hms']
    for col in hr_cols:
        filtered_gps[f'{col}_minutes'] = filtered_gps[col].apply(hms_to_minutes)
    
    hr_data = filtered_gps[['date'] + [f'{col}_minutes' for col in hr_cols]].melt(
        id_vars=['date'],
        var_name='zone',
        value_name='minutes'
    )
    hr_data['zone'] = hr_data['zone'].str.replace('_hms_minutes', '').str.replace('hr_zone_', 'Zone ')
    
    fig_hr = px.area(
        hr_data,
        x='date',
        y='minutes',
        color='zone',
        title="Temps Passé dans les Zones de Fréquence Cardiaque"
    )
    fig_hr.update_layout(
        xaxis_title="Date",
        yaxis_title="Temps (minutes)"
    )
    st.plotly_chart(fig_hr, use_container_width=True)

# TAB 3: Capacité Physique
with tab3:
    st.markdown("### 💪 Analyse de la Capacité Physique")
    
    # Filtrage des données physiques
    filtered_physical = physical_data[
        (physical_data['testDate'] >= pd.Timestamp(date_range[0])) & 
        (physical_data['testDate'] <= pd.Timestamp(date_range[1]))
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance par mouvement
        movement_perf = filtered_physical.groupby('movement')['benchmarkPct'].agg(['mean', 'count']).reset_index()
        movement_perf = movement_perf[movement_perf['count'] >= 3]  # Au moins 3 tests
        
        fig_movement = px.bar(
            movement_perf,
            x='movement',
            y='mean',
            title="Performance Moyenne par Type de Mouvement",
            color='mean',
            color_continuous_scale='RdYlGn'
        )
        fig_movement.add_hline(y=0.65, line_dash="dash", line_color="green", annotation_text="Objectif: 65%")
        fig_movement.update_layout(
            xaxis_title="Type de Mouvement",
            yaxis_title="Performance Moyenne (%)",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_movement, use_container_width=True)
    
    with col2:
        # Performance par expression
        expression_perf = filtered_physical.groupby('expression')['benchmarkPct'].agg(['mean', 'count']).reset_index()
        
        fig_expression = px.pie(
            expression_perf,
            values='count',
            names='expression',
            title="Répartition des Tests par Expression"
        )
        st.plotly_chart(fig_expression, use_container_width=True)
    
    # Évolution temporelle des performances
    st.markdown("#### Évolution Temporelle des Performances")
    
    # Sélection de la qualité à analyser
    available_qualities = filtered_physical['quality'].unique()
    selected_quality = st.selectbox("Sélectionnez une qualité à analyser:", available_qualities)
    
    quality_data = filtered_physical[filtered_physical['quality'] == selected_quality]
    
    if not quality_data.empty:
        fig_quality_trend = px.scatter(
            quality_data,
            x='testDate',
            y='benchmarkPct',
            color='movement',
            symbol='expression',
            title=f"Évolution de la Performance - {selected_quality.title()}",
            hover_data=['movement', 'expression']
        )
        
        # Ajouter une ligne de tendance
        if len(quality_data.dropna()) > 2:
            fig_quality_trend.add_traces(
                px.scatter(quality_data.dropna(), x='testDate', y='benchmarkPct', trendline='lowess').data[1]
            )
        
        fig_quality_trend.update_layout(
            xaxis_title="Date",
            yaxis_title="Performance (%)"
        )
        st.plotly_chart(fig_quality_trend, use_container_width=True)
    
    # Matrice de corrélation des performances
    st.markdown("#### Analyse Comparative des Qualités")
    
    pivot_data = filtered_physical.pivot_table(
        values='benchmarkPct',
        index='testDate',
        columns='quality',
        aggfunc='mean'
    )
    
    if not pivot_data.empty:
        correlation_matrix = pivot_data.corr()
        
        fig_corr = px.imshow(
            correlation_matrix,
            title="Matrice de Corrélation entre les Qualités Physiques",
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        st.plotly_chart(fig_corr, use_container_width=True)

# TAB 4: Statut de Récupération
with tab4:
    st.markdown("### 😴 Analyse du Statut de Récupération")
    
    # Filtrage des données de récupération
    filtered_recovery = recovery_data[
        (recovery_data['date'] >= pd.Timestamp(date_range[0])) & 
        (recovery_data['date'] <= pd.Timestamp(date_range[1]))
    ]
    
    # Score global de récupération
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_global_recovery = px.line(
            filtered_recovery,
            x='date',
            y='emboss_baseline_score',
            title="Score Global de Récupération",
            color_discrete_sequence=['#034694']
        )
        fig_global_recovery.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_global_recovery.add_hline(y=0.2, line_dash="dash", line_color="green", annotation_text="Excellent")
        fig_global_recovery.add_hline(y=-0.2, line_dash="dash", line_color="red", annotation_text="Attention")
        fig_global_recovery.update_layout(
            xaxis_title="Date",
            yaxis_title="Score de Récupération"
        )
        st.plotly_chart(fig_global_recovery, use_container_width=True)
    
    with col2:
        # Statut actuel
        current_score = filtered_recovery['emboss_baseline_score'].iloc[-1]
        if current_score > 0.1:
            status = "🟢 Excellent"
            color = "green"
        elif current_score > -0.1:
            status = "🟡 Bon"
            color = "orange"
        else:
            status = "🔴 Attention"
            color = "red"
        
        st.markdown(f"""
        <div style="background-color: {color}20; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>Statut Actuel</h3>
            <h2>{status}</h2>
            <p>Score: {current_score:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Analyse détaillée par catégorie
    st.markdown("#### Analyse Détaillée par Catégorie de Récupération")
    
    categories = ['bio', 'msk_joint_range', 'msk_load_tolerance', 'subjective', 'soreness', 'sleep']
    
    # Créer un graphique en radar pour les dernières valeurs
    latest_recovery = filtered_recovery.iloc[-1]
    
    radar_data = []
    for cat in categories:
        composite_col = f'{cat}_composite'
        completeness_col = f'{cat}_completeness'
        
        radar_data.append({
            'category': cat.replace('_', ' ').title(),
            'composite': latest_recovery[composite_col],
            'completeness': latest_recovery[completeness_col]
        })
    
    radar_df = pd.DataFrame(radar_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique en barres pour les scores composites
        fig_composite = px.bar(
            radar_df,
            x='category',
            y='composite',
            title="Scores Composites par Catégorie (Dernière Mesure)",
            color='composite',
            color_continuous_scale='RdYlGn'
        )
        fig_composite.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_composite.update_layout(
            xaxis_title="Catégorie",
            yaxis_title="Score Composite",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_composite, use_container_width=True)
    
    with col2:
        # Graphique en barres pour la complétude
        fig_completeness = px.bar(
            radar_df,
            x='category',
            y='completeness',
            title="Complétude des Tests par Catégorie",
            color_discrete_sequence=['#1f5f99']
        )
        fig_completeness.update_layout(
            xaxis_title="Catégorie",
            yaxis_title="Complétude (%)",
            xaxis_tickangle=-45,
            yaxis=dict(range=[0, 1])
        )
        st.plotly_chart(fig_completeness, use_container_width=True)
    
    # Évolution des catégories importantes
    st.markdown("#### Évolution des Catégories Clés")
    
    key_categories = st.multiselect(
        "Sélectionnez les catégories à analyser:",
        options=[f'{cat}_composite' for cat in categories],
        default=['sleep_composite', 'subjective_composite', 'soreness_composite'],
        format_func=lambda x: x.replace('_composite', '').replace('_', ' ').title()
    )
    
    if key_categories:
        recovery_evolution = filtered_recovery[['date'] + key_categories].melt(
            id_vars=['date'],
            var_name='category',
            value_name='score'
        )
        recovery_evolution['category'] = recovery_evolution['category'].str.replace('_composite', '').str.replace('_', ' ').str.title()
        
        fig_evolution = px.line(
            recovery_evolution,
            x='date',
            y='score',
            color='category',
            title="Évolution des Scores de Récupération par Catégorie"
        )
        fig_evolution.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_evolution.update_layout(
            xaxis_title="Date",
            yaxis_title="Score Composite"
        )
        st.plotly_chart(fig_evolution, use_container_width=True)

# TAB 5: Zones Prioritaires
with tab5:
    st.markdown("### 🎯 Zones Prioritaires Individuelles")
    
    # Données des priorités (simulées basées sur le document)
    priorities_data = [
        {
            'Priority': 1,
            'Category': 'Recovery',
            'Area': 'Sleep',
            'Target': 'Increase average sleep by 1hr per night',
            'Performance Type': 'Habit',
            'Target Set': '07/03/2025',
            'Review Date': '07/05/2025',
            'Tracking': 'On Track',
            'Progress': 75,
            'Status': '🟡'
        },
        {
            'Priority': 2,
            'Category': 'Recovery',
            'Area': 'Nutrition',
            'Target': '45g of carbohydrate every half time',
            'Performance Type': 'Habit',
            'Target Set': '07/03/2025',
            'Review Date': '07/05/2025',
            'Tracking': 'On Track',
            'Progress': 80,
            'Status': '🟢'
        },
        {
            'Priority': 3,
            'Category': 'Performance',
            'Area': 'Sprint',
            'Target': '>65% in max velocity score',
            'Performance Type': 'Outcome',
            'Target Set': '07/03/2025',
            'Review Date': '07/05/2025',
            'Tracking': 'Achieved',
            'Progress': 100,
            'Status': '🟢'
        }
    ]
    
    priorities_df = pd.DataFrame(priorities_data)
    
    # Affichage des priorités sous forme de cartes
    st.markdown("#### Priorités Actuelles")
    
    for _, priority in priorities_df.iterrows():
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center;">
                <h2>{priority['Status']}</h2>
                <p><strong>Priorité {priority['Priority']}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background-color: #034694; color: white; padding: 15px; border-radius: 10px;">
                <h4>{priority['Category']} - {priority['Area']}</h4>
                <p><strong>Objectif:</strong> {priority['Target']}</p>
                <p><strong>Type:</strong> {priority['Performance Type']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background-color: #1f5f99; color: white; padding: 15px; border-radius: 10px;">
                <p><strong>Statut:</strong> {priority['Tracking']}</p>
                <p><strong>Défini le:</strong> {priority['Target Set']}</p>
                <p><strong>Révision:</strong> {priority['Review Date']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Barre de progression
            progress_color = "#4CAF50" if priority['Progress'] == 100 else "#FF9800" if priority['Progress'] > 50 else "#F44336"
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center;">
                <p><strong>Progrès</strong></p>
                <div style="background-color: #e0e0e0; border-radius: 10px; padding: 3px;">
                    <div style="background-color: {progress_color}; width: {priority['Progress']}%; height: 20px; border-radius: 7px;"></div>
                </div>
                <p>{priority['Progress']}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Graphique de suivi des priorités
    st.markdown("#### Suivi des Progrès")
    
    fig_priorities = px.bar(
        priorities_df,
        x='Area',
        y='Progress',
        color='Category',
        title="Progression des Zones Prioritaires",
        color_discrete_map={'Recovery': '#034694', 'Performance': '#1f5f99'}
    )
    fig_priorities.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="Objectif")
    fig_priorities.update_layout(
        xaxis_title="Zone Prioritaire",
        yaxis_title="Progression (%)",
        yaxis=dict(range=[0, 110])
    )
    st.plotly_chart(fig_priorities, use_container_width=True)
    
    # Recommandations basées sur les données
    st.markdown("#### 💡 Recommandations Basées sur les Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #e8f5e8; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;">
            <h4>🎯 Points Forts</h4>
            <ul>
                <li>Excellente performance en vitesse maximale (objectif atteint)</li>
                <li>Bonne progression nutritionnelle</li>
                <li>Stabilité des métriques de charge d'entraînement</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #FF9800;">
            <h4>⚠️ Points d'Attention</h4>
            <ul>
                <li>Améliorer la régularité du sommeil</li>
                <li>Surveiller les scores de récupération</li>
                <li>Maintenir la performance en accélérations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Section d'ajout de nouvelles priorités
    st.markdown("#### ➕ Ajouter une Nouvelle Priorité")
    
    with st.expander("Définir une nouvelle zone prioritaire"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_category = st.selectbox("Catégorie", ["Performance", "Recovery", "Technique", "Tactique"])
            new_area = st.text_input("Zone spécifique", placeholder="ex: Endurance")
        
        with col2:
            new_target = st.text_area("Objectif", placeholder="Décrivez l'objectif à atteindre")
            new_type = st.selectbox("Type de Performance", ["Outcome", "Habit", "Process"])
        
        with col3:
            new_review_date = st.date_input("Date de révision")
            
        if st.button("Ajouter la Priorité"):
            st.success("Nouvelle priorité ajoutée avec succès!")
            st.info("Cette fonctionnalité serait intégrée à la base de données en production.")

# Footer avec informations de contact
st.markdown("---")
st.markdown("""
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;">
    <h4>📞 Contact CFC Performance Insights Team</h4>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div>
            <strong>Richard Akenhead</strong><br>
            Head of Performance Insights<br>
            📧 richard.akenhead@chelseafc.com
        </div>
        <div>
            <strong>Emmanuel (Manny) Fajemilua</strong><br>
            Performance Insights Analyst<br>
            📧 emmanuel.fajemilua@chelseafc.com
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Instructions d'utilisation
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📋 Guide d'Utilisation")
    st.markdown("""
    **Navigation:**
    - 📊 **Vue d'ensemble**: Tableau de bord principal
    - 🏃‍♂️ **GPS**: Analyse des données de mouvement
    - 💪 **Capacité**: Tests de force et puissance
    - 😴 **Récupération**: Monitoring du statut de récupération
    - 🎯 **Priorités**: Zones d'amélioration ciblées
    
    **Filtres:**
    - Utilisez les filtres de date et saison
    - Les graphiques se mettent à jour automatiquement
    - Explorez les différentes métriques
    """)
    
    st.markdown("### 🔧 Paramètres")
    show_raw_data = st.checkbox("Afficher les données brutes", False)
    
    if show_raw_data:
        st.markdown("### 📊 Données Brutes")
        dataset_choice = st.selectbox("Choisir le dataset", ["GPS", "Capacité Physique", "Récupération"])
        
        if dataset_choice == "GPS":
            st.dataframe(gps_data.head(10))
        elif dataset_choice == "Capacité Physique":
            st.dataframe(physical_data.head(10))
        else:
            st.dataframe(recovery_data.head(10))

# Message de bienvenue au démarrage
if 'welcome_shown' not in st.session_state:
    st.session_state.welcome_shown = True
    st.balloons()
    st.success("🎉 Bienvenue dans l'application CFC Performance Insights! Explorez les différents onglets pour analyser les données de performance.")