def buka_menu_perulangan():
    while True:
        try:
            number = int(input("Masukkan angka (0 untuk keluar): "))
            
            if number == 0:
                print("Program selesai. Terima kasih!")
                break
            
            print(f"Anda memasukkan: {number}")
            
        except ValueError:
            print("Error: Masukkan angka yang valid, bukan huruf atau karakter lain!")
