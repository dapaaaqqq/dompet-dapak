from data import transaksi

def hitung_total():
    total_masuk = 0
    total_keluar= 0

    for t in transaksi:
        if t["tipe"] == "masuk":
            total_masuk += t["jumlah"]
        elif t["tipe"] == "keluar":
            total_keluar += t["jumlah"]
    return total_masuk, total_keluar

def total_beta():
    masuk, keluar = hitung_total()
    print(f"Total Pemasukan : Rp {masuk}")
    print(f"Total Pengeluaran: Rp {keluar}")