import json

saldo = 0
transaksi = []

def simpan_data():
    data = {
        "saldo": saldo,
        "transaksi": transaksi
    }
    with open("data.json", 'w') as file:
        json.dump(data, file, indent=4)

def muat_data():
    global saldo, transaksi
    try:
        with open("data.json", 'r') as file:
            data = json.load(file)
            saldo = data.get("saldo", 0)
            transaksi = data.get("transaksi", [])
    except FileNotFoundError:
        saldo = 0
        transaksi = []