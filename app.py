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
    st.set_page_config(page_title="Dashboard Analisis Penjualan", layout="wide")
    st.title("🏦 Dashboard Analisis Penjualan")
    st.markdown("---")

    # ================= FITUR TEMPLATE =================
    template_data = pd.DataFrame({
        'tanggal': ['2024-01-01', '2024-01-02'],
        'produk': ['Ayam Goreng', 'Es Teh'],
        'kategori': ['Makanan', 'Minuman'],
        'harga': [10000, 2000],
        'jumlah': [15, 3]
    })
    csv_template = template_data.to_csv(index=False).encode('utf-8')

    st.sidebar.markdown("### 📋 Format Data")
    st.sidebar.caption("Pastikan file CSV yang diunggah memiliki nama kolom yang persis seperti template ini:")
    st.sidebar.download_button(
        label="⬇️ Unduh Template CSV",
        data=csv_template,
        file_name="template_data_penjualan.csv",
        mime="text/csv",
    )
    st.sidebar.markdown("---")

    uploaded_file = st.sidebar.file_uploader("📂 Unggah File CSV", type="csv")

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_clean = clean_process(df_raw)
        
        # Ekstrak waktu
        df_clean['tahun'] = df_clean['tanggal'].dt.year
        df_clean['bulan_nama'] = df_clean['tanggal'].dt.month_name()

        # Daftar urutan bulan yang baku
        months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                        'July', 'August', 'September', 'October', 'November', 'December']

        # --- CASCADING FILTER (Berurutan) ---
        st.sidebar.header("🕹️ Filter Panel")
        
        # 1. Tahun
        list_thn = sorted(df_clean['tahun'].unique())
        sel_thn = st.sidebar.multiselect("Pilih Tahun", list_thn, default=list_thn)
        df_f1 = df_clean[df_clean['tahun'].isin(sel_thn)]

        # 2. Bulan
        list_bln_raw = df_f1['bulan_nama'].unique().tolist()
        list_bln = [m for m in months_order if m in list_bln_raw]
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
                df_trend_tab = df_final.groupby(['tanggal', 'kategori', 'produk']).agg(
                    Omzet=('total_pendapatan', 'sum'),
                    Volume=('jumlah', 'sum')
                ).reset_index().sort_values(['tanggal', 'Omzet'], ascending=[False, False])
                
                df_trend_tab = df_trend_tab.rename(columns={
                    'tanggal': 'Tanggal', 
                    'kategori': 'Kategori', 
                    'produk': 'Komoditas'
                })
                
                st.dataframe(
                    df_trend_tab.style.format({'Omzet': format_rp, 'Volume': format_qty}),
                    use_container_width=True, hide_index=True
                )

            st.markdown("---")

            # --- PRODUCT & CATEGORY ---
            col_a, col_b = st.columns(2)
            df_p, df_k, _ = run_analysis(df_final)
            fig_p, fig_k = create_plots(df_p, df_k)
            
            with col_a:
                st.plotly_chart(fig_p, use_container_width=True)
                st.write("**Tabel Detail Komoditas:**")
                
                df_p = df_p.sort_values('total_pendapatan', ascending=False)
                df_p['Kontribusi (%)'] = (df_p['total_pendapatan'] / df_p['total_pendapatan'].sum()) * 100
                df_p_styled = df_p.rename(columns={'produk': 'Komoditas', 'total_pendapatan': 'Omzet', 'jumlah': 'Volume'})
                
                st.dataframe(
                    df_p_styled.style.format({'Omzet': format_rp, 'Volume': format_qty, 'Kontribusi (%)': '{:.2f}%'}),
                    use_container_width=True, hide_index=True
                )
                
            with col_b:
                st.plotly_chart(fig_k, use_container_width=True)
                st.write("**Tabel Detail Kategori:**")
                
                df_k = df_k.sort_values('total_pendapatan', ascending=False)
                df_k['Kontribusi (%)'] = (df_k['total_pendapatan'] / df_k['total_pendapatan'].sum()) * 100
                df_k_styled = df_k.rename(columns={'kategori': 'Kategori', 'total_pendapatan': 'Omzet', 'jumlah': 'Volume'})
                
                st.dataframe(
                    df_k_styled.style.format({'Omzet': format_rp, 'Volume': format_qty, 'Kontribusi (%)': '{:.2f}%'}),
                    use_container_width=True, hide_index=True
                )

            st.markdown("---")

            # --- MONTHLY COMPARISON ---
            st.subheader("📊 Komparasi Bulanan")
            
            df_pivot = df_final.copy()
            df_pivot['bulan_nama'] = pd.Categorical(df_pivot['bulan_nama'], categories=months_order, ordered=True)
            df_pivot = df_pivot.sort_values(['tahun', 'bulan_nama'])
            df_pivot['periode'] = df_pivot['bulan_nama'].astype(str) + " " + df_pivot['tahun'].astype(str)
            ordered_periods = df_pivot['periode'].unique()
            
            tab1, tab2 = st.tabs(["💰 Omzet", "📦 Volume"])
            
            with tab1:
                st.plotly_chart(create_monthly_comparison_chart(df_final, 'total_pendapatan', 'Omzet (Rp)'), use_container_width=True)
                st.write("**Rekapitulasi Omzet per Komoditas:**")
                
                pivot_omzet = df_pivot.pivot_table(index='produk', columns='periode', values='total_pendapatan', aggfunc='sum').fillna(0)
                pivot_omzet = pivot_omzet.reindex(columns=ordered_periods)
                pivot_omzet['Total Keseluruhan'] = pivot_omzet.sum(axis=1)
                pivot_omzet = pivot_omzet.sort_values('Total Keseluruhan', ascending=False)
                
                st.dataframe(
                    pivot_omzet.style.format(format_rp), 
                    use_container_width=True
                )

            with tab2:
                st.plotly_chart(create_monthly_comparison_chart(df_final, 'jumlah', 'Volume (Pcs)'), use_container_width=True)
                st.write("**Rekapitulasi Volume per Komoditas:**")
                
                pivot_qty = df_pivot.pivot_table(index='produk', columns='periode', values='jumlah', aggfunc='sum').fillna(0)
                pivot_qty = pivot_qty.reindex(columns=ordered_periods)
                pivot_qty['Total Keseluruhan'] = pivot_qty.sum(axis=1)
                pivot_qty = pivot_qty.sort_values('Total Keseluruhan', ascending=False)
                
                st.dataframe(
                    pivot_qty.style.format("{:,.0f}"), 
                    use_container_width=True
                )

        else:
            st.warning("Data tidak tersedia untuk filter yang dipilih.")
    else:
        st.info("👋 **Selamat Datang!** \n\nSilakan unggah file CSV data penjualan Anda di panel sebelah kiri (sidebar). Pastikan format dan nama kolom pada file Anda sesuai dengan **Template CSV** yang dapat diunduh di sidebar agar dashboard dapat berfungsi dengan baik.")

if __name__ == "__main__":
    main()