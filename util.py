import time
import os

def input_angka(pesan):
    try:
        return int(input(pesan))
    except ValueError:
        print("Input tidak valid, harus berupa angka yah).")
        return None

def pause():
    time.sleep(3)
    input("\ntekan Enter untuk melanjutkan...")
    clear_screen()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def konfirmasi_keluar():
    clear_screen()
    print("=== Konfirmasi Keluar ===")
    while True:
        jawab = input("Yakin ingin keluar? (y/n): ").lower()
        if jawab == 'y':
            return True
        elif jawab == 'n':
            return False
        else:
            print("Input ngga valid, masukin y/n aja yah.")