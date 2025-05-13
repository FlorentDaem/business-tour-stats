import streamlit as st
import pandas as pd

# === CHARGEMENT DES NOMS DE CASES ===
# Remplace ce chemin par le bon si besoin
df_noms = pd.read_csv("noms.csv", encoding="latin1")
df_noms.columns = ["id", "nom"]
df_noms = df_noms.sort_values("id").reset_index(drop=True)

# === INITIALISATION DE LA SESSION ===
st.set_page_config(page_title="Stats Business Tour", layout="wide")
st.title("📊 Statistiques de passages - Business Tour")

if "passages" not in st.session_state:
    st.session_state.passages = [0] * len(df_noms)

# === BOUTON DE RÉINITIALISATION ===
if st.button("🔄 Réinitialiser les données"):
    st.session_state.passages = [0] * len(df_noms)

# === BOUTONS POUR INCRÉMENTER ===
st.markdown("### Cliquez sur une case pour enregistrer un passage :")
cols = st.columns(4)
for i, row in df_noms.iterrows():
    if cols[i % 4].button(row["nom"], key=f"btn_{row['id']}"):
        st.session_state.passages[i] += 1

# === CRÉATION DU TABLEAU DE STATISTIQUES ===
total = sum(st.session_state.passages)
frequences = [(p / total * 100) if total > 0 else 0.0 for p in st.session_state.passages]

df_stats = pd.DataFrame({
    "ID": df_noms["id"],
    "Nom de la case": df_noms["nom"],
    "Passages": st.session_state.passages,
    "Fréquence (%)": [round(f, 2) for f in frequences]
})

# === AFFICHAGE DU TABLEAU ===
st.markdown("### Résultats actuels :")
st.table(df_stats)

import plotly.express as px

# Créer un histogramme interactif
fig = px.bar(
    df_stats,
    x="Nom de la case",
    y="Passages",
    hover_data=["Fréquence (%)"],
    labels={"Passages": "Nombre de passages"},
    title="📈 Histogramme des passages par case"
)
fig.update_layout(xaxis_tickangle=-45)

# Affichage du graphe dans Streamlit
st.plotly_chart(fig, use_container_width=True)


# === BOUTON POUR TÉLÉCHARGER LES DONNÉES ===
st.download_button(
    label="💾 Télécharger les données (CSV)",
    data=df_stats.to_csv(index=False).encode("utf-8"),
    file_name="stats_business_tour.csv",
    mime="text/csv"
)
