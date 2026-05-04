import streamlit as st
import pandas as pd
from data_cleaning import clean_process
from eda_analysis import run_analysis
from data_viz import create_plots, create_trend_chart, create_monthly_comparison_chart

# Helper functions untuk tampilan
def format_rp(val):
    return f"Rp {val:,.0f}".replace(",", ".")

def format_qty(val):
    return f"{int(val):,}".replace(",", ".")

def main():
    st.set_page_config(page_title="Business Intel Dashboard", layout="wide")
    st.title("🏦 Dashboard Analisis Penjualan")
    st.markdown("---")

    uploaded_file = st.sidebar.file_uploader("📂 Unggah File CSV", type="csv")

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_clean = clean_process(df_raw)
        
        # Ekstrak waktu
        df_clean['tahun'] = df_clean['tanggal'].dt.year
        df_clean['bulan_nama'] = df_clean['tanggal'].dt.month_name()

        # --- CASCADING FILTER (Berurutan) ---
        st.sidebar.header("🕹️ Filter Panel")
        
        # 1. Tahun
        list_thn = sorted(df_clean['tahun'].unique())
        sel_thn = st.sidebar.multiselect("Pilih Tahun", list_thn, default=list_thn)
        df_f1 = df_clean[df_clean['tahun'].isin(sel_thn)]

        # 2. Bulan
        list_bln = df_f1['bulan_nama'].unique().tolist()
        sel_bln = st.sidebar.multiselect("Pilih Bulan", list_bln, default=list_bln)
        df_f2 = df_f1[df_f1['bulan_nama'].isin(sel_bln)]

        # 3. Kategori
        list_kat = sorted(df_f2['kategori'].unique().tolist())
        sel_kat = st.sidebar.multiselect("Pilih Kategori", list_kat, default=list_kat)
        df_f3 = df_f2[df_f2['kategori'].isin(sel_kat)]

        # 4. Komoditas
        list_prod = sorted([str(x) for x in df_f3['produk'].unique()])
        sel_prod = st.sidebar.multiselect("Pilih Komoditas", list_prod, default=list_prod)
        
        df_final = df_f3[df_f3['produk'].isin(sel_prod)]

        if not df_final.empty:
            # --- METRICS ---
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Omzet", format_rp(df_final['total_pendapatan'].sum()))
            m2.metric("Total Terjual", format_qty(df_final['jumlah'].sum()))
            m3.metric("Rata-rata Penjualan", format_rp(df_final['total_pendapatan'].mean()))

            st.markdown("---")

            # --- TREND SECTION ---
            st.subheader("📈 Tren Omzet")
            st.plotly_chart(create_trend_chart(df_final), use_container_width=True)
            
            with st.expander("📄 Detail Data Tren"):
                df_trend_tab = df_final.groupby('tanggal')['total_pendapatan'].sum().reset_index()
                st.dataframe(df_trend_tab.style.format({'total_pendapatan': format_rp}), use_container_width=True)

            st.markdown("---")

            # --- PRODUCT & CATEGORY ---
            col_a, col_b = st.columns(2)
            df_p, df_k, _ = run_analysis(df_final)
            fig_p, fig_k = create_plots(df_p, df_k)
            
            with col_a:
                st.plotly_chart(fig_p, use_container_width=True)
                st.write("**Detail Data Komoditas:**")
                st.dataframe(df_p.sort_values('total_pendapatan', ascending=False).style.format({
                    'total_pendapatan': format_rp, 'jumlah': '{:,.0f}'
                }), use_container_width=True)
                
            with col_b:
                st.plotly_chart(fig_k, use_container_width=True)
                st.write("**Detail Data Kategori:**")
                st.table(df_k.assign(total_pendapatan=df_k['total_pendapatan'].apply(format_rp)))

            st.markdown("---")

            # --- MONTHLY COMPARISON ---
            st.subheader("📊 Komparasi Bulanan")
            tab1, tab2 = st.tabs(["💰 Omzet", "📦 Volume"])
            
            with tab1:
                st.plotly_chart(create_monthly_comparison_chart(df_final, 'total_pendapatan', 'Omzet (Rp)'), use_container_width=True)
                st.write("**Tabel Pendukung Omzet:**")
                pivot_omzet = df_final.pivot_table(index='produk', columns='bulan_nama', values='total_pendapatan', aggfunc='sum').fillna(0)
                st.dataframe(pivot_omzet.style.format(format_rp), use_container_width=True)

            with tab2:
                st.plotly_chart(create_monthly_comparison_chart(df_final, 'jumlah', 'Volume (Pcs)'), use_container_width=True)
                st.write("**Tabel Pendukung Volume:**")
                pivot_qty = df_final.pivot_table(index='produk', columns='bulan_nama', values='jumlah', aggfunc='sum').fillna(0)
                st.dataframe(pivot_qty.style.format("{:,.0f}"), use_container_width=True)

        else:
            st.warning("Data tidak tersedia untuk filter yang dipilih.")
    else:
        st.info("Silakan unggah file CSV data penjualan Anda di sidebar.")

if __name__ == "__main__":
    main()