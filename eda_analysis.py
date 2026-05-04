import pandas as pd

def run_analysis(df):
    summary_produk = df.groupby('produk').agg({
        'total_pendapatan': 'sum',
        'jumlah': 'sum'
    }).reset_index()
    
    summary_kategori = df.groupby('kategori').agg({
        'total_pendapatan': 'sum'
    }).reset_index()
    
    return summary_produk, summary_kategori, df['total_pendapatan'].sum()