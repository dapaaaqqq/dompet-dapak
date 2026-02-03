import matplotlib.pyplot as plt
from laporan import hitung_total
from util import pause
from data import transaksi

def grafik():
    if not transaksi:
        print("Belum ada transaksi untuk ditampilkan.")
        pause()
        return
    masuk, keluar = hitung_total()
    
    label = ['pemasukan', 'pengeluaran']
    nilai = [masuk, keluar]

    plt.figure()
    plt.bar(label, nilai)
    plt.title("Grafik keuangan by DompetDapak")
    plt.ylabel("Jumlah (Rp)")
    plt.xlabel("Jenis Transaksi")

    plt.show()