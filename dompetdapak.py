from datetime import datetime
import csv
from util import input_angka, pause, clear_screen, konfirmasi_keluar
from data import simpan_data, muat_data
from grafik import grafik
from laporan import total_beta
from data import saldo, transaksi
#FUNGSI HELPER

KATEGORI = ["makan", "transportasi", "topup", "jajan", "lainnya"]

def pilih_kategori():
    print("pilih kategori:")
    for i, k in enumerate(KATEGORI, start=1):
        print(f"{i}. {k}")

    pilihan = input_angka("Masukkan nomor kategori: ")
    if pilihan is None or pilihan < 1 or pilihan > len(KATEGORI):
        print("Ga Valid Boskuh, coba lagi yah.")
        return None
    return KATEGORI[pilihan - 1]    


def get_saldo():
    return saldo



#PENANDA MENU

def tampilkan_menu():
    clear_screen()
    print("=== Aplikasi Keuangan Sederhana ===")
    print("1. Tambah Pemasukan")
    print("2. Tambah Pengeluaran")
    print("3. Tampilkan Saldo")
    print("4. Tampilkan Riwayat Transaksi")
    print("5. Laporan Pengeluaran")
    print("6. Check per tanggal")
    print("7. Ekspor laporan")
    print("8. Cek total (beta)")
    print("9. Grafik Keuangan")
    print("10. Keluar Aplikasi")



def uang_masuk():
    global saldo
    jumlah = input_angka("Masukkan jumlah pemasukan: ")
    if jumlah is None:
        return
    
    kategori = pilih_kategori()
    if kategori is None:
        return

    catatan = input("Keterangan (opsional): ")
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transaksi_baru = {
        "tipe": "masuk",
        "jumlah": jumlah,
        "keterangan": catatan,
        "waktu" : waktu
    }


    saldo += jumlah
    transaksi.append(transaksi_baru)
    simpan_data()

    print("\n✅ Pemasukan berhasil ditambahkan!")
    print("📄 Detail Transaksi Terakhir:")
    print(f"Tipe       : Pemasukan")
    print(f"waktu : {waktu}")
    print(f"Jumlah     : Rp {jumlah}")
    print(f"Keterangan : {catatan if catatan else '-'}")
    pause()


def uang_keluar():
    global saldo
    jumlah = input_angka("Masukkan jumlah pengeluaran: ")
    if jumlah is None or jumlah > saldo:
        print("Maaf, saldo tidak mencukupi atau INPUTMU SALAH WOI")
        return

    kategori = pilih_kategori()
    if kategori is None:
        return
     
    catatan = input("Keterangan (opsional): ")
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    saldo -= jumlah
    transaksi.append({
        "tipe": "keluar",
        "jumlah": jumlah,
        "kategori": kategori,
        "keterangan": catatan,
        "waktu": waktu
    })

    simpan_data()
    print("Pengeluaran ditambahkan.")
    pause()

def lihat_saldo():
    print(f"Saldo saat ini: {saldo}")
    pause()

def lihat_riwayat():
    if not transaksi:
        print("Belum ada transaksi.")
        pause()
        return
    

    print("\n=== Riwayat Transaksi ===")
    for i, t in enumerate(transaksi, start=1):
        tipe = "Pemasukan" if t["tipe"] == "masuk" else "Pengeluaran"
        waktu = t.get("waktu", "-")
        keterangan = t.get("Keterangan", "-")
        print(
            f"{i}, [{waktu}] {tipe}: Rp {t['jumlah']} - {keterangan}"
        )
def laporan_pengeluaran():
    if not transaksi:
        print("Belum ada transaksi.")
        pause()
        return
    today = datetime.now().date()
    bulan_ini = datetime.now().month
    tahun_ini = datetime.now().year

    total_hari_ini = 0
    total_bulan_ini = 0

    for t in transaksi:
        if t["tipe"] == "keluar":
            waktu = datetime.strptime(t["waktu"], "%Y-%m-%d %H:%M:%S")

            if waktu.date() == today:
                total_hari_ini += t["jumlah"]
            if waktu.month == bulan_ini and waktu.year == tahun_ini:
                total_bulan_ini += t["jumlah"]

    print("\n=== Laporan Pengeluaran ===")
    print(f"Hari ini : Rp {total_hari_ini}")
    print(f"Bulan ini: Rp {total_bulan_ini}")
    pause()

def laporan_per_tanggal():
    if not transaksi:
            print("belum ada transaksi.")
            pause()
            return
        
    tanggal_input = input("Masukkan tanggal (Tahun - Bulan - Hari): ")

    total_masuk = 0
    total_keluar = 0

    for t in transaksi:
        tanggal_transaksi = t["waktu"][:10]

        if tanggal_transaksi == tanggal_input:
            if t["tipe"] == "masuk":
                total_masuk += t["jumlah"]
            elif t["tipe"] == "keluar":
                total_keluar += t["jumlah"]
        
    if total_masuk == 0 and total_keluar == 0:
        print(f"Tidak ada transaksi pada tanggal {tanggal_input}.")
    else:
        print(f"\nLaporan untuk tanggal {tanggal_input}:")
        print(f"Total Pemasukan : Rp {total_masuk}")
        print(f"Total Pengeluaran: Rp {total_keluar}")

    pause()

def import_ke_laporan():
    if not transaksi:
        print("Belum transaksi.")
        pause()
        return

    with open("transaksi.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tipe", "Jumlah", "Keterangan", "kategori", "Waktu"])
        
        for t in transaksi:
            writer.writerow([
                t.get("tipe", ""),
                t.get("jumlah", ""),
                t.get("kategori", ""),
                t.get("keterangan", ""),
                t.get("waktu", "")
            ])
    print("Data transaksi berhasil diimpor ke transaksi.csv")

def search_transaksi():
    keyword = input("masukkan keyword untuk mencari").lower()

    ditemukan = False
    for t in transaksi:
        if (
            t["tipe"] =="keluar"
            and keyword in t.get("keterangan","").lower()
        ):
            print(
                f"[{t['waktu']}] Rp {t['jumlah']} "f"({t.get('kategori','-')}) - {t.get('keterangan','-')}"
            )
            ditemukan = True
    if not ditemukan:
        print("tidak ada transaksi yang sesuai.")

#MUAT DATA SAAT PROGRAM DIMULAI
muat_data()

while True:
    tampilkan_menu()
    pilihan = input("Pilih menu: ")

    if pilihan == '1':
        uang_masuk()
    elif pilihan == '2':
        uang_keluar()
    elif pilihan == '3':
        lihat_saldo()
    elif pilihan == '4':
        lihat_riwayat()
    elif pilihan == '5':
        laporan_pengeluaran()
    elif pilihan == '6':
        laporan_per_tanggal()
    elif pilihan == '7':
        import_ke_laporan()
    elif pilihan == '8':
        total_beta()
    elif pilihan == '9':
        grafik()    
    elif pilihan == '10':
        if konfirmasi_keluar():
            print("Terima kasih telah menggunakan aplikasi ini.")
            break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")

