import Ganjil_Genap
import Modul_Kalkulasi_Geometri
import Modul_Operasi_Bilangan

while True:
    print("\n=== Menu Utama ===")
    print("1. Cek Ganjil/Genap")
    print("2. Luas Persegi Panjang")
    print("3. Luas Segitiga")
    print("4. Tambah")
    print("5. Kurang")
    print("6. Kali")
    print("7. Bagi")
    print("8. Keluar")

    pilihan = input("Pilih menu (1-8): ")

    if pilihan == "1":
        Ganjil_Genap.ganjil_genap()
    elif pilihan == "2":
        Modul_Kalkulasi_Geometri.luas_persegi_panjang()
    elif pilihan == "3":
        Modul_Kalkulasi_Geometri.luas_segitiga()
    elif pilihan in {"4", "5", "6", "7"}:
        try:
            a = float(input("Masukkan bilangan pertama: "))
            b = float(input("Masukkan bilangan kedua: "))
        except ValueError:
            print("Input harus berupa angka.")
            continue

        if pilihan == "4":
            print(f"Hasil penjumlahan: {Modul_Operasi_Bilangan.tambah(a, b)}")
        elif pilihan == "5":
            print(f"Hasil pengurangan: {Modul_Operasi_Bilangan.kurang(a, b)}")
        elif pilihan == "6":
            print(f"Hasil perkalian: {Modul_Operasi_Bilangan.kali(a, b)}")
        elif pilihan == "7":
            try:
                print(f"Hasil pembagian: {Modul_Operasi_Bilangan.bagi(a, b)}")
            except ValueError as e:
                print(e)
    elif pilihan == "8":
        print("Program selesai.")
        break
    else:
        print("Pilihan tidak valid, coba lagi.")
