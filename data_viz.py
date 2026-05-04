import plotly.express as px
import pandas as pd

def create_trend_chart(df):
    # Agregasi data per tanggal
    df_trend = df.groupby('tanggal')['total_pendapatan'].sum().reset_index()
    
    fig = px.area(df_trend, x='tanggal', y='total_pendapatan', 
                  title='📈 Tren Omzet Real-Time (Interaktif)',
                  labels={'total_pendapatan': 'Omzet (Rp)', 'tanggal': 'Tanggal'},
                  template='plotly_white')

    # Desain garis dan area
    fig.update_traces(line_color='#007BFF', fillcolor='rgba(0, 123, 255, 0.1)')

    # Menambahkan Slider dan Tombol Navigasi Waktu agar fleksibel jika data banyak
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="7H", step="day", stepmode="backward"),
                dict(count=1, label="1B", step="month", stepmode="backward"),
                dict(count=3, label="3B", step="month", stepmode="backward"),
                dict(step="all", label="Semua")
            ])
        )
    )
    
    fig.update_layout(hovermode="x unified", yaxis_tickprefix="Rp ")
    return fig

def create_plots(df_produk, df_kategori):
    # Bar Chart Produk
    fig_produk = px.bar(df_produk.sort_values('total_pendapatan'), 
                        x='total_pendapatan', y='produk', orientation='h',
                        title="Performa per Komoditas",
                        color='total_pendapatan', color_continuous_scale='Blues')
    
    # Donut Chart Kategori
    fig_pie = px.pie(df_kategori, values='total_pendapatan', names='kategori', 
                      title="Distribusi Kategori", hole=0.4)
    return fig_produk, fig_pie

def create_monthly_comparison_chart(df, target_col, title_label):
    df_monthly = df.groupby(['produk', 'bulan_nama'])[target_col].sum().reset_index()
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December']
    df_monthly['bulan_nama'] = pd.Categorical(df_monthly['bulan_nama'], categories=months_order, ordered=True)
    df_monthly = df_monthly.sort_values('bulan_nama')

    fig = px.bar(df_monthly, x='bulan_nama', y=target_col, color='produk',
                 barmode='group', title=f"Komparasi {title_label} per Bulan",
                 text_auto='.2s' if target_col == 'total_pendapatan' else 'd')
    return fig