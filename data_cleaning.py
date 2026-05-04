import pandas as pd

def clean_process(df):
    df = df.dropna(how='all').fillna(0)
    # Memastikan teks dan angka konsisten
    df['produk'] = df['produk'].astype(str)
    df['kategori'] = df['kategori'].astype(str)
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df['harga'] = pd.to_numeric(df['harga'], errors='coerce').fillna(0)
    df['jumlah'] = pd.to_numeric(df['jumlah'], errors='coerce').fillna(0)
    df['total_pendapatan'] = df['harga'] * df['jumlah']
    return df