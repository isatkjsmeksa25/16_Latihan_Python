
def hitung_luas_persegi_panjang(panjang, lebar):
    luas = panjang * lebar
    return luas

def luas_persegi_panjang():

    print("\n=== Kalkulator Luas Persegi Panjang ===")
    
    panjang = float(input("Masukkan panjang: "))
    lebar = float(input("Masukkan lebar: "))
    
    luas = hitung_luas_persegi_panjang(panjang, lebar)

    print(f"\nPanjang: {panjang}")
    print(f"Lebar: {lebar}")
    print(f"Luas persegi panjang: {luas}")

def hitung_luas_segitiga(alas, tinggi):
    luas = (alas * tinggi) / 2
    return luas

# Input dari user
def luas_segitiga():

    print("=== Kalkulator Luas Segitiga ===")
    
    alas = float(input("Masukkan panjang alas segitiga: "))
    tinggi = float(input("Masukkan tinggi segitiga: "))

    # Hitung luas
    luas = hitung_luas_segitiga(alas, tinggi)

    # Tampilkan hasil
    print(f"\nAlas segitiga: {alas}")
    print(f"Tinggi segitiga: {tinggi}")
    print(f"Luas segitiga: {luas}")
