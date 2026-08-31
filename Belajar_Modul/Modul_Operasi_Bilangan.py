def tambah(a, b):
    return a + b

def kurang(a, b):
    return a - b

def kali(a, b):
    return a * b

def bagi(a, b):
    if b == 0:
        return "Error: Pembagi tidak boleh 0"
    return a / b

if __name__ == "__main__":
    print("=== Kalkulator Operasi Bilangan ===\n")
    
    try:
        angka1 = float(input("Masukkan angka pertama: "))
        angka2 = float(input("Masukkan angka kedua: "))
        
        print(f"\nPertambahan {angka1} + {angka2} = {tambah(angka1, angka2)}")
        print(f"Pengurangan {angka1} - {angka2} = {kurang(angka1, angka2)}")
        print(f"Perkalian {angka1} * {angka2} = {kali(angka1, angka2)}")
        print(f"Pembagian {angka1} / {angka2} = {bagi(angka1, angka2)}")
    except ValueError:
        print("Error: Masukkan input berupa angka!")

