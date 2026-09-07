import sys
import os
import time
import mysql.connector
import gspread
from google.oauth2.service_account import Credentials


# ============================================================
# LOKASI FOLDER
# ============================================================

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BELAJAR_MODUL = os.path.join(ROOT_FOLDER, "Belajar_Modul")

sys.path.insert(0, BELAJAR_MODUL)


# ============================================================
# IMPORT PROGRAM DARI FOLDER Belajar_Modul
# ============================================================

import Ganjil_Genap
import Modul_Kalkulasi_Geometri
import Modul_Operasi_Bilangan


# ============================================================
# KONEKSI KE MYSQL
# ============================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1$@16DtBAseKiWi",
    database="database_program"
)

cursor = db.cursor()


# ============================================================
# KONEKSI KE GOOGLE SHEETS
# ============================================================

CREDENTIALS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Credentials.json"
)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open("ISA_Database Program MySQL")
sheet = spreadsheet.get_worksheet(0)


# ============================================================
# LOGIN
# ============================================================

print("================================")
print("          LOGIN PROGRAM")
print("================================")

username = input("Username : ")
password = input("Password : ")


# ============================================================
# CEK USERNAME DAN PASSWORD
# ============================================================

sql_login = """
SELECT username
FROM users
WHERE username = %s AND password = %s
"""

cursor.execute(sql_login, (username, password))
user = cursor.fetchone()


# ============================================================
# JIKA LOGIN SALAH
# ============================================================

if user is None:
    print("\n❌ Username atau password salah!")
    print("Program tidak dapat dijalankan.")

    cursor.close()
    db.close()

    sys.exit()


# ============================================================
# JIKA LOGIN BERHASIL
# ============================================================

print("\n✅ Login berhasil!")
print("Selamat datang,", username)


# ============================================================
# INPUT NAMA DAN KELAS
# ============================================================

print("\n=== DATA PENGGUNA ===")

nama = input("Nama  : ")
kelas = input("Kelas : ")


# ============================================================
# TIMER DIMULAI
# ============================================================

waktu_mulai = time.perf_counter()

print("\n⏱️ Timer dimulai.")
print("Silakan gunakan program yang tersedia.")


# ============================================================
# MENU UTAMA
# ============================================================

while True:

    print("\n================================")
    print("           MENU UTAMA")
    print("================================")
    print("1. Cek Ganjil/Genap")
    print("2. Luas Persegi Panjang")
    print("3. Luas Segitiga")
    print("4. Tambah")
    print("5. Kurang")
    print("6. Kali")
    print("7. Bagi")
    print("8. Keluar")
    print("================================")

    pilihan = input("Pilih menu (1-8): ")


    # ========================================================
    # 1. GANJIL / GENAP
    # ========================================================

    if pilihan == "1":

        Ganjil_Genap.ganjil_genap()


    # ========================================================
    # 2. LUAS PERSEGI PANJANG
    # ========================================================

    elif pilihan == "2":

        try:
            Modul_Kalkulasi_Geometri.luas_persegi_panjang()

        except ValueError:
            print("❌ Input harus berupa angka.")


    # ========================================================
    # 3. LUAS SEGITIGA
    # ========================================================

    elif pilihan == "3":

        try:
            Modul_Kalkulasi_Geometri.luas_segitiga()

        except ValueError:
            print("❌ Input harus berupa angka.")


    # ========================================================
    # 4-7. OPERASI BILANGAN
    # ========================================================

    elif pilihan in {"4", "5", "6", "7"}:

        try:
            a = float(input("Masukkan bilangan pertama: "))
            b = float(input("Masukkan bilangan kedua: "))

        except ValueError:
            print("❌ Input harus berupa angka.")
            continue


        if pilihan == "4":

            hasil = Modul_Operasi_Bilangan.tambah(a, b)
            print(f"Hasil penjumlahan: {hasil}")


        elif pilihan == "5":

            hasil = Modul_Operasi_Bilangan.kurang(a, b)
            print(f"Hasil pengurangan: {hasil}")


        elif pilihan == "6":

            hasil = Modul_Operasi_Bilangan.kali(a, b)
            print(f"Hasil perkalian: {hasil}")


        elif pilihan == "7":

            hasil = Modul_Operasi_Bilangan.bagi(a, b)
            print(f"Hasil pembagian: {hasil}")


    # ========================================================
    # 8. KELUAR
    # ========================================================

    elif pilihan == "8":

        print("\nProgram selesai.")
        break


    # ========================================================
    # PILIHAN TIDAK VALID
    # ========================================================

    else:

        print("❌ Pilihan tidak valid, coba lagi.")


# ============================================================
# TIMER BERHENTI
# ============================================================

waktu_selesai = time.perf_counter()

durasi = waktu_selesai - waktu_mulai

timer = round(durasi)


# ============================================================
# KONVERSI TIMER
# ============================================================

jam = timer // 3600
menit = (timer % 3600) // 60
detik = timer % 60


# ============================================================
# TAMPILKAN HASIL TIMER
# ============================================================

print("\n================================")
print("        SESI SELESAI")
print("================================")
print(f"Nama       : {nama}")
print(f"Kelas      : {kelas}")
print(f"Username   : {username}")
print(f"Waktu      : {jam:02d}:{menit:02d}:{detik:02d}")
print(f"Timer      : {timer} detik")
print("================================")


# ============================================================
# SIMPAN DATA KE MYSQL
# ============================================================

sql_insert = """
INSERT INTO program (username, nama, kelas, timer)
VALUES (%s, %s, %s, %s)
"""

data = (username, nama, kelas, timer)

cursor.execute(sql_insert, data)

db.commit()


# ============================================================
# AMBIL ID DATA YANG BARU SAJA DISIMPAN
# ============================================================

id_program = cursor.lastrowid


# ============================================================
# KIRIM DATA KE GOOGLE SHEETS
# ============================================================

sheet.append_row([
    id_program,
    username,
    nama,
    kelas,
    timer
])


# ============================================================
# KONFIRMASI
# ============================================================

print("\n✅ Data berhasil disimpan ke MySQL!")
print("✅ Data berhasil dikirim ke Google Spreadsheet!")


# ============================================================
# TUTUP KONEKSI
# ============================================================

cursor.close()
db.close()