import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("day_df.csv")
hour_df = pd.read_csv("hour_df.csv")

# Mapping season numbers to names
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_label'] = day_df['season'].map(season_mapping)

# Mengatur urutan musim sesuai dengan mapping
season_order = ["Spring", "Summer", "Fall", "Winter"]
day_df["season_label"] = pd.Categorical(day_df["season_label"], categories=season_order, ordered=True)

# Mapping workingday to categories
hour_df['day_type'] = hour_df['workingday'].map({0: 'Akhir Pekan / Libur', 1: 'Hari Kerja'})

# Streamlit UI Setup
st.set_page_config(page_title="Dashboard Analisis Penyewaan Sepeda", layout="wide")
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown("""
    **Bike Sharing System** adalah generasi baru dari sistem penyewaan sepeda tradisional yang memungkinkan pengguna
    menyewa dan mengembalikan sepeda secara otomatis. Saat ini, terdapat lebih dari **500 program bike-sharing di seluruh dunia**
    dengan lebih dari **500 ribu sepeda** yang tersedia. 
    
    Sistem ini tidak hanya membantu mengurangi kemacetan dan polusi, tetapi juga berfungsi sebagai jaringan sensor virtual
    yang dapat merekam pola mobilitas perkotaan. Dengan menganalisis data ini, kita dapat mengidentifikasi tren perjalanan,
    memahami pengaruh faktor lingkungan, serta mengoptimalkan penggunaan sepeda berbasis data.
""")

# Pertanyaan 1
st.subheader("💡 Musim dengan Peminjaman Sepeda Tertinggi")
hourly_sum = hour_df.groupby('hr')[['casual', 'registered', 'cnt']].mean()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hourly_sum, markers=True, linewidth=2, ax=ax)
ax.set_xticks(range(0, 24))  
ax.set_xlim(0, 23)  
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Jumlah Penyewaan")
ax.set_title("Tren Penyewaan Sepeda Sepanjang Hari")
ax.grid()
st.pyplot(fig)

# Perbandingan Peminjaman berdasarkan Hari Kerja dan Akhir Pekan
st.subheader("👥 Perbandingan Peminjaman Sepeda")
user_type_selection = st.radio("Pilih Tipe Pengguna:", ["casual", "registered"], index=0)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=hour_df.groupby(["hr", "day_type"])[user_type_selection].mean().unstack(),
    linewidth=2, marker="o", ax=ax
)
ax.set_xticks(range(0, 24, 1))  
ax.set_xlim(0, 23)  
ax.set_xlabel("Jam")
ax.set_ylabel(f"Rata-rata Peminjaman ({user_type_selection.capitalize()})")
ax.set_title(f"Perbandingan Peminjaman Sepeda ({user_type_selection.capitalize()})")
ax.grid()
st.pyplot(fig)



# Pertanyaan 2
st.subheader("💡 Tren Peminjaman Berdasarkan Musim")
seasonal_data = day_df.groupby('season', observed=False)[['casual', 'registered', 'cnt']].sum()
seasonal_data.index = seasonal_data.index.map(season_mapping)
seasonal_data_T = seasonal_data.T  

fig, ax = plt.subplots(figsize=(12, 6))
seasonal_data_T.plot(kind='bar', colormap="coolwarm", edgecolor='black', ax=ax)
ax.set_title("Total Pengguna Sepeda Berdasarkan Kategori Pengguna", fontsize=14)
ax.set_xlabel("Kategori Pengguna", fontsize=12)
ax.set_ylabel("Jumlah Pengguna", fontsize=12)
ax.set_xticklabels(seasonal_data_T.index, rotation=0)  
ax.legend(title="Musim")
st.pyplot(fig)

# Faktor Lingkungan per Musim
st.subheader("🌍 Faktor Lingkungan per Musim")
metrics = {
    "temp": "Rata-rata Temperatur per Musim",
    "atemp": "Rata-rata Feels-like Temperature per Musim",
    "hum": "Rata-rata Kelembapan per Musim",
    "windspeed": "Rata-rata Kecepatan Angin per Musim"
}

seasonal_avg = day_df.groupby("season_label", observed=False)[["temp", "atemp", "hum", "windspeed"]].mean().reset_index()

selected_metric = st.selectbox("📌 Pilih Faktor Lingkungan:", list(metrics.keys()), format_func=lambda x: metrics[x])

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=seasonal_avg, x="season_label", y=selected_metric, hue="season_label", palette="coolwarm", ax=ax, legend=False)
ax.set_title(metrics[selected_metric])
ax.set_xlabel("Musim")
ax.set_ylabel("")
ax.grid(axis="y")
st.pyplot(fig)

