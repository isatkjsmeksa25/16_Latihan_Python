def cek_ganjil_genap(x):
    if x % 2 == 0:
        return f"Angka {x} adalah Bilangan Genap"
    else:
        return f"Angka {x} adalah Bilangan Ganjil"



def ganjil_genap():
    """Menentukan Apakah Angka Ganjil atau Genap"""
    while True:
        x = int(input("Silahkan Masukkan Angka: "))

        if x % 2 == 0:
            print("Angka", x, "adalah Bilangan Genap")
        else:
            print("Angka", x, "adalah Bilangan Ganjil")

        tombol = input("Tekan 'x' untuk keluar atau tekan tombol lain untuk melanjutkan:")
        if tombol == 'x':
            break
