def hitung_luas_segitiga(alas, tinggi):
    luas = (alas * tinggi) / 2
    return luas

# Input dari user
def buka_menu_luas_segitiga():

    print("=== Kalkulator Luas Segitiga ===")
    
    alas = float(input("Masukkan panjang alas segitiga: "))
    tinggi = float(input("Masukkan tinggi segitiga: "))

    # Hitung luas
    luas = hitung_luas_segitiga(alas, tinggi)

    # Tampilkan hasil
    print(f"\nAlas segitiga: {alas}")
    print(f"Tinggi segitiga: {tinggi}")
    print(f"Luas segitiga: {luas}")
