import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
import ctypes


# ==========================================================
# FORCE LOAD FONT MENGGUNAKAN WINDOWS API
# ==========================================================

folder_sekarang = os.path.dirname(os.path.abspath(__file__))
folder_font = os.path.join(folder_sekarang, "fonts")

if os.path.exists(folder_font):
    FR_PRIVATE = 0x10

    for nama_file in os.listdir(folder_font):
        if nama_file.lower().endswith(('.otf', '.ttf')):
            jalur_font_penuh = os.path.join(folder_font, nama_file)

            ctypes.windll.gdi32.AddFontResourceExW(
                jalur_font_penuh,
                FR_PRIVATE,
                0
            )

            print(f"Berhasil memuat font: {nama_file}")

else:
    print(
        f"Peringatan: Folder 'fonts' tidak ditemukan "
        f"di {folder_font}!"
    )


# ==========================================================
# KONEKSI DATABASE MYSQL
# ==========================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1$@16DtBAseKiWi",
    database="database_program"
)

cursor = db.cursor()


# ==========================================================
# WINDOW UTAMA
# ==========================================================

window = tk.Tk()

window.title("Koleksi My Program Gweh")
window.geometry("900x600")
window.resizable(False, False)


# ==========================================================
# VARIABEL PASSWORD
# ==========================================================

password_login_visible = False
password_daftar_visible = False
konfirmasi_visible = False


# ==========================================================
# HAPUS SEMUA WIDGET DI WINDOW
# ==========================================================

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


# ==========================================================
# TOGGLE PASSWORD LOGIN
# ==========================================================

def toggle_password_login():
    global password_login_visible

    if password_login_visible:
        entry_password_login.config(show="*")
        button_show_login.config(text="👁")
        password_login_visible = False

    else:
        entry_password_login.config(show="")
        button_show_login.config(text="🙈")
        password_login_visible = True


# ==========================================================
# TOGGLE PASSWORD REGISTRASI
# ==========================================================

def toggle_password_daftar():
    global password_daftar_visible

    if password_daftar_visible:
        entry_password_daftar.config(show="*")
        button_password.config(text="👁")
        password_daftar_visible = False

    else:
        entry_password_daftar.config(show="")
        button_password.config(text="🙈")
        password_daftar_visible = True


# ==========================================================
# TOGGLE KONFIRMASI PASSWORD
# ==========================================================

def toggle_konfirmasi():
    global konfirmasi_visible

    if konfirmasi_visible:
        entry_konfirmasi.config(show="*")
        button_konfirmasi.config(text="👁")
        konfirmasi_visible = False

    else:
        entry_konfirmasi.config(show="")
        button_konfirmasi.config(text="🙈")
        konfirmasi_visible = True


# ==========================================================
# PROSES LOGIN
# ==========================================================

def login():

    global username_login

    username = entry_username.get().strip()
    password = entry_password_login.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Peringatan",
            "Username dan password harus diisi!"
        )
        return

    try:
        cursor.execute(
            """
            SELECT id, username
            FROM users
            WHERE username = %s AND password = %s
            """,
            (username, password)
        )

        user = cursor.fetchone()

        if user:

            username_login = username

            tampilkan_dashboard(username_login)

        else:
            messagebox.showerror(
                "Login Gagal",
                "Username atau password salah!"
            )

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Gagal mengakses database:\n{error}"
        )


# ==========================================================
# PROSES REGISTRASI
# ==========================================================

def daftar_akun():
    username = entry_username_daftar.get().strip()
    password = entry_password_daftar.get()
    konfirmasi = entry_konfirmasi.get()

    # ------------------------------
    # CEK INPUT KOSONG
    # ------------------------------

    if username == "" or password == "" or konfirmasi == "":
        messagebox.showwarning(
            "Peringatan",
            "Semua kolom harus diisi!"
        )
        return

    # ------------------------------
    # CEK PASSWORD
    # ------------------------------

    if password != konfirmasi:
        messagebox.showerror(
            "Registrasi Gagal",
            "Password dan konfirmasi password tidak sama!"
        )
        return

    try:
        # ------------------------------
        # CEK USERNAME SUDAH ADA
        # ------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        if user:
            messagebox.showerror(
                "Registrasi Gagal",
                "Username tersebut sudah digunakan!"
            )
            return

        # ------------------------------
        # MASUKKAN USER BARU
        # ------------------------------

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            """,
            (username, password)
        )

        db.commit()

        messagebox.showinfo(
            "Registrasi Berhasil",
            f"Akun '{username}' berhasil dibuat!"
        )

        # Setelah berhasil daftar,
        # kembali ke halaman login.
        tampilkan_login()

    except mysql.connector.Error as error:
        db.rollback()

        messagebox.showerror(
            "Database Error",
            f"Gagal membuat akun:\n{error}"
        )


# ==========================================================
# HALAMAN LOGIN
# ==========================================================

def tampilkan_login():

    global entry_username
    global entry_password_login
    global button_show_login
    global password_login_visible

    password_login_visible = False

    clear_window()

    # ------------------------------
    # JUDUL
    # ------------------------------

    judul = tk.Label(
        window,
        text="Koleksi My Program Gweh",
        font=("BingBoss", 24)
    )

    judul.pack(pady=(70, 10))

    subjudul = tk.Label(
        window,
        text="Login untuk melanjutkan",
        font=("BingBoss", 12)
    )

    subjudul.pack(pady=(0, 35))

    # ------------------------------
    # USERNAME
    # ------------------------------

    label_username = tk.Label(
        window,
        text="Username",
        font=("BingBoss", 11)
    )

    label_username.pack()

    entry_username = tk.Entry(
        window,
        width=35,
        font=("BingBoss", 12)
    )

    entry_username.pack(pady=(5, 20))

    # ------------------------------
    # PASSWORD
    # ------------------------------

    label_password = tk.Label(
        window,
        text="Password",
        font=("BingBoss", 11)
    )

    label_password.pack()

    password_frame = tk.Frame(window)
    password_frame.pack(pady=(5, 25))

    entry_password_login = tk.Entry(
        password_frame,
        width=30,
        font=("BingBoss", 12),
        show="*"
    )

    entry_password_login.pack(side="left")

    button_show_login = tk.Button(
        password_frame,
        text="👁",
        font=("Arial", 10),
        width=3,
        command=toggle_password_login
    )

    button_show_login.pack(
        side="left",
        padx=(5, 0)
    )

    # ------------------------------
    # TOMBOL LOGIN
    # ------------------------------

    button_login = tk.Button(
        window,
        text="LOGIN",
        width=20,
        font=("BingBoss", 11),
        command=login
    )

    button_login.pack(pady=(0, 15))

    # ------------------------------
    # DAFTAR
    # ------------------------------

    label_daftar = tk.Label(
        window,
        text="Belum punya akun?",
        font=("BingBoss", 10)
    )

    label_daftar.pack()

    button_daftar = tk.Button(
        window,
        text="DAFTAR AKUN",
        width=20,
        font=("BingBoss", 10),
        command=tampilkan_registrasi
    )

    button_daftar.pack(pady=(5, 0))


# ==========================================================
# HALAMAN REGISTRASI
# ==========================================================

def tampilkan_registrasi():

    global entry_username_daftar
    global entry_password_daftar
    global entry_konfirmasi

    global button_password
    global button_konfirmasi

    global password_daftar_visible
    global konfirmasi_visible

    password_daftar_visible = False
    konfirmasi_visible = False

    username_login = ""
    clear_window()

    # ------------------------------
    # JUDUL
    # ------------------------------

    judul = tk.Label(
        window,
        text="Buat Akun Baru",
        font=("BingBoss", 24)
    )

    judul.pack(pady=(55, 10))

    subjudul = tk.Label(
        window,
        text="Daftarkan akun ke database",
        font=("BingBoss", 12)
    )

    subjudul.pack(pady=(0, 30))

    # ------------------------------
    # USERNAME
    # ------------------------------

    label_username = tk.Label(
        window,
        text="Username",
        font=("BingBoss", 11)
    )

    label_username.pack()

    entry_username_daftar = tk.Entry(
        window,
        width=35,
        font=("BingBoss", 12)
    )

    entry_username_daftar.pack(pady=(5, 15))

    # ------------------------------
    # PASSWORD
    # ------------------------------

    label_password = tk.Label(
        window,
        text="Password",
        font=("BingBoss", 11)
    )

    label_password.pack()

    password_frame = tk.Frame(window)
    password_frame.pack(pady=(5, 15))

    entry_password_daftar = tk.Entry(
        password_frame,
        width=30,
        font=("BingBoss", 12),
        show="*"
    )

    entry_password_daftar.pack(side="left")

    button_password = tk.Button(
        password_frame,
        text="👁",
        font=("Arial", 10),
        width=3,
        command=toggle_password_daftar
    )

    button_password.pack(
        side="left",
        padx=(5, 0)
    )

    # ------------------------------
    # KONFIRMASI PASSWORD
    # ------------------------------

    label_konfirmasi = tk.Label(
        window,
        text="Konfirmasi Password",
        font=("BingBoss", 11)
    )

    label_konfirmasi.pack()

    konfirmasi_frame = tk.Frame(window)
    konfirmasi_frame.pack(pady=(5, 25))

    entry_konfirmasi = tk.Entry(
        konfirmasi_frame,
        width=30,
        font=("BingBoss", 12),
        show="*"
    )

    entry_konfirmasi.pack(side="left")

    button_konfirmasi = tk.Button(
        konfirmasi_frame,
        text="👁",
        font=("Arial", 10),
        width=3,
        command=toggle_konfirmasi
    )

    button_konfirmasi.pack(
        side="left",
        padx=(5, 0)
    )

    # ------------------------------
    # TOMBOL DAFTAR
    # ------------------------------

    button_daftar = tk.Button(
        window,
        text="DAFTAR",
        width=20,
        font=("BingBoss", 11),
        command=daftar_akun
    )

    button_daftar.pack(pady=(0, 10))

    # ------------------------------
    # TOMBOL KEMBALI
    # ------------------------------

    button_kembali = tk.Button(
        window,
        text="KEMBALI",
        width=20,
        font=("BingBoss", 10),
        command=tampilkan_login
    )

    button_kembali.pack()

# ==========================================================
# PROGRAM GANJIL / GENAP
# ==========================================================

def tampilkan_ganjil_genap():

    clear_window()

    # ------------------------------
    # JUDUL
    # ------------------------------

    judul = tk.Label(
        window,
        text="Ganjil / Genap",
        font=("BingBoss", 24)
    )

    judul.pack(pady=(80, 10))


    # ------------------------------
    # PETUNJUK
    # ------------------------------

    petunjuk = tk.Label(
        window,
        text="Masukkan sebuah angka",
        font=("BingBoss", 12)
    )

    petunjuk.pack(pady=(0, 25))


    # ------------------------------
    # INPUT ANGKA
    # ------------------------------

    entry_angka = tk.Entry(
        window,
        width=30,
        font=("BingBoss", 14),
        justify="center"
    )

    entry_angka.pack(pady=(0, 20))


    # ------------------------------
    # HASIL
    # ------------------------------

    label_hasil = tk.Label(
        window,
        text="",
        font=("BingBoss", 12)
    )

    label_hasil.pack(pady=(10, 25))


    # ------------------------------
    # FUNGSI CEK
    # ------------------------------

    def cek_ganjil_genap():

        angka = entry_angka.get().strip()

        if angka == "":
            messagebox.showwarning(
                "Peringatan",
                "Masukkan angka terlebih dahulu!"
            )
            return

        try:
            angka = int(angka)

        except ValueError:
            messagebox.showerror(
                "Input Tidak Valid",
                "Input harus berupa angka!"
            )
            return

        if angka % 2 == 0:
            label_hasil.config(
                text=f"Angka {angka} adalah Bilangan Genap"
            )

        else:
            label_hasil.config(
                text=f"Angka {angka} adalah Bilangan Ganjil"
            )


    # ------------------------------
    # TOMBOL CEK
    # ------------------------------

    button_cek = tk.Button(
        window,
        text="CEK",
        width=20,
        font=("BingBoss", 11),
        command=cek_ganjil_genap
    )

    button_cek.pack()


    # ------------------------------
    # TOMBOL KEMBALI
    # ------------------------------

    button_kembali = tk.Button(
        window,
        text="KEMBALI",
        width=20,
        font=("BingBoss", 10),
        command=lambda: tampilkan_dashboard(username_login)
    )

    button_kembali.pack(pady=(30, 0))

# ==========================================================
# DASHBOARD
# ==========================================================

def tampilkan_dashboard(username):

    clear_window()

    # ------------------------------
    # HEADER
    # ------------------------------

    header = tk.Frame(window)
    header.pack(fill="x", padx=30, pady=(25, 10))

    judul = tk.Label(
        header,
        text="Koleksi My Program Gweh",
        font=("BingBoss", 22)
    )

    judul.pack(side="left")

    label_user = tk.Label(
        header,
        text=f"👤 {username}",
        font=("BingBoss", 11)
    )

    label_user.pack(side="right")


    # ------------------------------
    # JUDUL PROGRAM
    # ------------------------------

    label_program = tk.Label(
        window,
        text="Daftar Program",
        font=("BingBoss", 16)
    )

    label_program.pack(pady=(20, 20))


    # ------------------------------
    # FRAME PROGRAM
    # ------------------------------

    frame_program = tk.Frame(window)
    frame_program.pack()


    # ------------------------------
    # FUNGSI SEMENTARA TOMBOL
    # ------------------------------

    def program_belum_dihubungkan(nama_program):
        messagebox.showinfo(
            "Program",
            f"{nama_program}\n\n"
            "Program akan dihubungkan pada tahap berikutnya."
        )


    # ------------------------------
    # PROGRAM 1
    # ------------------------------

    frame1 = tk.Frame(
        frame_program,
        width=300,
        height=100,
        relief="solid",
        borderwidth=1
    )

    frame1.grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    frame1.pack_propagate(False)

    tk.Label(
        frame1,
        text="Ganjil / Genap",
        font=("BingBoss", 12)
    ).pack(pady=(12, 5))

    tk.Button(
        frame1,
        text="BUKA",
        width=15,
        font=("BingBoss", 9),
        command=tampilkan_ganjil_genap
    ).pack()


    # ------------------------------
    # PROGRAM 2
    # ------------------------------

    frame2 = tk.Frame(
        frame_program,
        width=300,
        height=100,
        relief="solid",
        borderwidth=1
    )

    frame2.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    frame2.pack_propagate(False)

    tk.Label(
        frame2,
        text="Luas Persegi Panjang",
        font=("BingBoss", 12)
    ).pack(pady=(12, 5))

    tk.Button(
        frame2,
        text="BUKA",
        width=15,
        font=("BingBoss", 9),
        command=lambda: program_belum_dihubungkan(
            "Luas Persegi Panjang"
        )
    ).pack()


    # ------------------------------
    # PROGRAM 3
    # ------------------------------

    frame3 = tk.Frame(
        frame_program,
        width=300,
        height=100,
        relief="solid",
        borderwidth=1
    )

    frame3.grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    frame3.pack_propagate(False)

    tk.Label(
        frame3,
        text="Luas Segitiga",
        font=("BingBoss", 12)
    ).pack(pady=(12, 5))

    tk.Button(
        frame3,
        text="BUKA",
        width=15,
        font=("BingBoss", 9),
        command=lambda: program_belum_dihubungkan(
            "Luas Segitiga"
        )
    ).pack()


    # ------------------------------
    # PROGRAM 4
    # ------------------------------

    frame4 = tk.Frame(
        frame_program,
        width=300,
        height=100,
        relief="solid",
        borderwidth=1
    )

    frame4.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    frame4.pack_propagate(False)

    tk.Label(
        frame4,
        text="Penjumlahan",
        font=("BingBoss", 12)
    ).pack(pady=(12, 5))

    tk.Button(
        frame4,
        text="BUKA",
        width=15,
        font=("BingBoss", 9),
        command=lambda: program_belum_dihubungkan(
            "Penjumlahan"
        )
    ).pack()


    # ------------------------------
    # PROGRAM 5
    # ------------------------------

    frame5 = tk.Frame(
        frame_program,
        width=300,
        height=100,
        relief="solid",
        borderwidth=1
    )

    frame5.grid(
        row=2,
        column=0,
        padx=10,
        pady=10
    )

    frame5.pack_propagate(False)

    tk.Label(
        frame5,
        text="Pengurangan",
        font=("BingBoss", 12)
    ).pack(pady=(12, 5))

    tk.Button(
        frame5,
        text="BUKA",
        width=15,
        font=("BingBoss", 9),
        command=lambda: program_belum_dihubungkan(
            "Pengurangan"
        )
    ).pack()


    # ------------------------------
    # PROGRAM 6
    # ------------------------------

    frame6 = tk.Frame(
        frame_program,
        width=300,
        height=100,
        relief="solid",
        borderwidth=1
    )

    frame6.grid(
        row=2,
        column=1,
        padx=10,
        pady=10
    )

    frame6.pack_propagate(False)

    tk.Label(
        frame6,
        text="Perkalian",
        font=("BingBoss", 12)
    ).pack(pady=(12, 5))

    tk.Button(
        frame6,
        text="BUKA",
        width=15,
        font=("BingBoss", 9),
        command=lambda: program_belum_dihubungkan(
            "Perkalian"
        )
    ).pack()


    # ------------------------------
    # PROGRAM 7
    # ------------------------------

    frame7 = tk.Frame(
        frame_program,
        width=300,
        height=100,
        relief="solid",
        borderwidth=1
    )

    frame7.grid(
        row=3,
        column=0,
        padx=10,
        pady=10
    )

    frame7.pack_propagate(False)

    tk.Label(
        frame7,
        text="Pembagian",
        font=("BingBoss", 12)
    ).pack(pady=(12, 5))

    tk.Button(
        frame7,
        text="BUKA",
        width=15,
        font=("BingBoss", 9),
        command=lambda: program_belum_dihubungkan(
            "Pembagian"
        )
    ).pack()


    # ------------------------------
    # LOGOUT
    # ------------------------------

    button_logout = tk.Button(
        window,
        text="LOGOUT",
        width=20,
        font=("BingBoss", 10),
        command=tampilkan_login
    )

    button_logout.pack(pady=(5, 10))
    
# ==========================================================
# MULAI DARI HALAMAN LOGIN
# ==========================================================

tampilkan_login()


# ==========================================================
# JALANKAN APLIKASI
# ==========================================================

window.mainloop()