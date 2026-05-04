import plotly.express as px
import pandas as pd

def create_trend_chart(df):
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df = df.sort_values('tanggal')
    
    # Agregasi data per tanggal
    df_trend = df.groupby('tanggal')['total_pendapatan'].sum().reset_index()
    
    fig = px.area(df_trend, x='tanggal', y='total_pendapatan', 
                  title='📈 Tren Omzet Real-Time (Interaktif)',
                  labels={'total_pendapatan': 'Omzet (Rp)', 'tanggal': 'Tanggal'},
                  template='plotly_white')

    # Desain garis dan area
    fig.update_traces(line_color='#007BFF', fillcolor='rgba(0, 123, 255, 0.1)')

    # Slider dan Tombol Navigasi Waktu agar fleksibel jika data banyak
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
    if 'tanggal' in df.columns:
        df['tanggal'] = pd.to_datetime(df['tanggal'])
        df['tahun'] = df['tanggal'].dt.year
    else:
        df['tahun'] = ""

    df_monthly = df.groupby(['produk', 'tahun', 'bulan_nama'])[target_col].sum().reset_index()

    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December']
    df_monthly['bulan_nama'] = pd.Categorical(df_monthly['bulan_nama'], categories=months_order, ordered=True)
    
    df_monthly = df_monthly.sort_values(['tahun', 'bulan_nama'])
    if df['tahun'].iloc[0] != "":
        df_monthly['periode'] = df_monthly['bulan_nama'].astype(str) + " " + df_monthly['tahun'].astype(str)
    else:
        df_monthly['periode'] = df_monthly['bulan_nama']

    # Plotting bar chart
    fig = px.bar(df_monthly, x='periode', y=target_col, color='produk',
                 barmode='group', title=f"Komparasi {title_label} per Bulan",
                 text_auto='.2s' if target_col == 'total_pendapatan' else 'd')
    
    fig.update_layout(
        xaxis=dict(categoryorder='array', categoryarray=df_monthly['periode'].unique()),
        xaxis_title="Bulan & Tahun"
    )
    
    return fig

def create_yearly_comparison_chart(df, target_col, title_label):
    df_yearly = df.groupby(['produk', 'tahun'])[target_col].sum().reset_index()

    df_yearly['tahun'] = df_yearly['tahun'].astype(str)
    df_yearly = df_yearly.sort_values('tahun')

    fig = px.bar(df_yearly, x='tahun', y=target_col, color='produk',
                 barmode='group', title=f"Komparasi {title_label} per Tahun",
                 text_auto='.2s' if target_col == 'total_pendapatan' else 'd')
    
    fig.update_layout(
        xaxis=dict(categoryorder='category ascending'),
        xaxis_title="Tahun"
    )
    
    return fig