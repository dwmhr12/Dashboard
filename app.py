import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .reportview-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        h1, h2, h3 {
            color: #2a3d57;
        }
        .css-1v3fvcr {
            color: #607d8b;
        }
        .stButton>button {
            background-color: #3e8e41;
            color: white;
            font-weight: bold;
        }
        .stRadio>label {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
Day_df = pd.read_csv("Bike_Sharing_Cleaned.csv")

# Streamlit dashboard
st.title("Dashboard Bike Sharing")
st.write("Dashboard ini menyajikan eksplorasi data penyewaan sepeda berdasarkan musim dan suhu.")

# Tambahkan label musim untuk filter
Day_df['season_label'] = Day_df['season'].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

# Buat kategori suhu
Day_df['temp_bins'] = pd.cut(
    Day_df['temp'],
    bins=5,
    labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High']
)

# Pilihan mode filter
filter_mode = st.radio(
    "Pilih mode filter:",
    options=["Musim", "Suhu", "Musim dan Suhu"],
    index=2,  # Default: Musim dan Suhu
    key="filter_mode"
)

# Filter data berdasarkan pilihan
if filter_mode == "Musim":
    # Filter musim saja
    season_filter = st.multiselect(
        "Pilih Musim",
        options=Day_df['season_label'].unique(),
        default=Day_df['season_label'].unique()
    )
    filtered_data = Day_df[Day_df['season_label'].isin(season_filter)]

elif filter_mode == "Suhu":
    # Filter suhu saja
    temp_filter = st.multiselect(
        "Pilih Kategori Suhu",
        options=Day_df['temp_bins'].unique(),
        default=Day_df['temp_bins'].unique()
    )
    filtered_data = Day_df[Day_df['temp_bins'].isin(temp_filter)]

else:
    # Filter musim dan suhu
    season_filter = st.multiselect(
        "Pilih Musim",
        options=Day_df['season_label'].unique(),
        default=Day_df['season_label'].unique()
    )
    temp_filter = st.multiselect(
        "Pilih Kategori Suhu",
        options=Day_df['temp_bins'].unique(),
        default=Day_df['temp_bins'].unique()
    )
    filtered_data = Day_df.loc[
        Day_df['season_label'].isin(season_filter) &
        Day_df['temp_bins'].isin(temp_filter)
    ]

# Validasi jika data kosong
if filtered_data.empty:
    st.warning("Data tidak ditemukan dengan filter yang dipilih.")
else:
    # Eksplorasi Data
    st.subheader("Eksplorasi Data")
    st.write("Statistik deskriptif data yang telah difilter:")
    st.write(filtered_data.describe(include='all'))

    # Pivot berdasarkan musim
    st.write("Pivot Tabel Berdasarkan Musim:")
    pivot_season = filtered_data.pivot_table(index='season_label', values='cnt', aggfunc=['mean', 'median', 'max', 'min'])
    st.dataframe(pivot_season)

    # Pivot berdasarkan kategori suhu
    st.write("Pivot Tabel Berdasarkan Kategori Suhu:")
    pivot_temp = filtered_data.pivot_table(index='temp_bins', values='cnt', aggfunc=['mean', 'median', 'count'])
    st.dataframe(pivot_temp)

    # Visualisasi 1: Distribusi jumlah penyewaan berdasarkan musim
    st.subheader("Distribusi Jumlah Penyewaan Berdasarkan Musim")
    fig1 = plt.figure(figsize=(8, 6))
    sns.boxplot(data=filtered_data, x='season_label', y='cnt', palette="coolwarm")
    plt.title('Distribusi Jumlah Penyewaan Berdasarkan Musim', fontsize=14)
    plt.xlabel('Musim', fontsize=12)
    plt.ylabel('Jumlah Penyewaan (cnt)', fontsize=12)
    st.pyplot(fig1)

    # Visualisasi 2: Distribusi jumlah penyewaan berdasarkan kategori suhu
    st.subheader("Distribusi Jumlah Penyewaan Berdasarkan Kategori Suhu")
    fig2 = plt.figure(figsize=(8, 6))
    sns.boxplot(data=filtered_data, x='temp_bins', y='cnt', palette="coolwarm")
    plt.title('Distribusi Jumlah Penyewaan Berdasarkan Kategori Suhu', fontsize=14)
    plt.xlabel('Kategori Suhu', fontsize=12)
    plt.ylabel('Jumlah Penyewaan (cnt)', fontsize=12)
    st.pyplot(fig2)

