
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
