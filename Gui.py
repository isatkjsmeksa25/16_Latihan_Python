import tkinter as tk
from tkinter import messagebox, font as tkfont
import mysql.connector
import gspread
import os
import sys
import time
import ctypes


# ============================================================
# PATH PROJECT
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BELAJAR_MODUL_DIR = os.path.join(BASE_DIR, "Belajar_Modul")
CREDENTIALS_FILE = os.path.join(
    BASE_DIR, "python_mysql", "Credentials.json"
)
FONT_FOLDER = os.path.join(BASE_DIR, "fonts")

if BELAJAR_MODUL_DIR not in sys.path:
    sys.path.insert(0, BELAJAR_MODUL_DIR)


# ============================================================
# IMPORT PROGRAM LAMA
# ============================================================

import Ganjil_Genap
import Modul_Kalkulasi_Geometri
import Modul_Operasi_Bilangan


# ============================================================
# KONFIGURASI MYSQL
# ============================================================
# Sengaja memakai konfigurasi MySQL yang sama dengan GUI lama
# agar tidak muncul lagi "using password: NO".
#
# Jika password MySQL root nanti diganti, ubah nilai di bawah.
# Jangan bagikan password tersebut ke orang lain.

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1$@16DtBAseKiWi"
MYSQL_DATABASE = "database_program"


# ============================================================
# GOOGLE SHEETS
# ============================================================

SPREADSHEET_NAME = "ISA_Database Program MySQL"
WORKSHEET_NAME = "Sheet1"


# ============================================================
# FONT
# ============================================================

CUSTOM_FONT_FAMILY = "BingBoss"


def load_custom_fonts():
    if os.name != "nt":
        return

    if not os.path.exists(FONT_FOLDER):
        print("Folder fonts tidak ditemukan:", FONT_FOLDER)
        return

    FR_PRIVATE = 0x10

    for filename in os.listdir(FONT_FOLDER):
        if filename.lower().endswith((".ttf", ".otf")):
            path = os.path.join(FONT_FOLDER, filename)

            try:
                result = ctypes.windll.gdi32.AddFontResourceExW(
                    path, FR_PRIVATE, 0
                )

                if result:
                    print("Berhasil memuat font:", filename)
                else:
                    print("Gagal memuat font:", filename)

            except Exception as e:
                print("Error font:", filename, e)


load_custom_fonts()


# ============================================================
# WINDOW
# ============================================================

window = tk.Tk()
window.title("Koleksi My Program Gweh")
window.geometry("900x600")
window.resizable(False, False)


def get_font(size=11, weight="normal"):
    try:
        return tkfont.Font(
            family=CUSTOM_FONT_FAMILY,
            size=size,
            weight=weight
        )
    except Exception:
        return tkfont.Font(
            family="Arial",
            size=size,
            weight=weight
        )


FONT_NORMAL = get_font(11)
FONT_BOLD = get_font(11, "bold")
FONT_TITLE = get_font(24, "bold")
FONT_SUBTITLE = get_font(12)
FONT_RESULT = get_font(13, "bold")


# ============================================================
# SESSION
# ============================================================

username_login = ""
nama_login = ""
kelas_login = ""

session_start_time = None
session_timer_job = None
session_saved = False

timer_label = None


# ============================================================
# ENTRY REFERENCES
# ============================================================

entry_username = None
entry_password_login = None
button_show_login = None

entry_username_daftar = None
entry_password_daftar = None
entry_konfirmasi = None
button_password = None
button_konfirmasi = None

entry_nama = None
entry_kelas = None

entry_angka_ganjil = None
entry_panjang = None
entry_lebar = None
entry_alas = None
entry_tinggi = None
entry_operasi_a = None
entry_operasi_b = None


# ============================================================
# PASSWORD VISIBILITY
# ============================================================

password_login_visible = False
password_daftar_visible = False
konfirmasi_visible = False


# ============================================================
# HELPER
# ============================================================

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def create_title(text):
    tk.Label(
        window,
        text=text,
        font=FONT_TITLE
    ).pack(pady=(30, 5))


def create_button(parent, text, command, width=25):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=FONT_BOLD,
        width=width,
        height=2,
        cursor="hand2"
    )


def get_mysql_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )


# ============================================================
# GOOGLE SHEETS
# ============================================================

def save_to_google_sheets(data):
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            raise FileNotFoundError(
                "Credentials.json tidak ditemukan:\n"
                + CREDENTIALS_FILE
            )

        gc = gspread.service_account(
            filename=CREDENTIALS_FILE
        )

        spreadsheet = gc.open(SPREADSHEET_NAME)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

        worksheet.append_row(
            data,
            value_input_option="USER_ENTERED"
        )

        print("Data berhasil dikirim ke Google Sheets.")
        return True

    except Exception as error:
        print("Google Sheets Error:", error)
        return False


# ============================================================
# LOGIN PASSWORD SHOW/HIDE
# ============================================================

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


# ============================================================
# LOGIN
# ============================================================

def login():
    global username_login
    global session_start_time
    global session_saved

    username = entry_username.get().strip()
    password = entry_password_login.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Peringatan",
            "Username dan password harus diisi!"
        )
        return

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username
            FROM users
            WHERE username = %s
            AND password = %s
            """,
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            username_login = username

            session_start_time = time.perf_counter()
            session_saved = False

            tampilkan_data_pengguna()

        else:
            messagebox.showerror(
                "Login Gagal",
                "Username atau password salah!"
            )

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            "Gagal terhubung ke MySQL.\n\n"
            f"{error}"
        )


# ============================================================
# REGISTER
# ============================================================

def daftar_akun():
    username = entry_username_daftar.get().strip()
    password = entry_password_daftar.get()
    konfirmasi = entry_konfirmasi.get()

    if username == "" or password == "" or konfirmasi == "":
        messagebox.showwarning(
            "Peringatan",
            "Semua kolom harus diisi!"
        )
        return

    if password != konfirmasi:
        messagebox.showerror(
            "Registrasi Gagal",
            "Password dan konfirmasi password tidak sama!"
        )
        return

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        if cursor.fetchone():
            cursor.close()
            conn.close()

            messagebox.showerror(
                "Registrasi Gagal",
                "Username tersebut sudah digunakan!"
            )
            return

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            """,
            (username, password)
        )

        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo(
            "Registrasi Berhasil",
            "Akun berhasil dibuat!\n\n"
            "Silakan login menggunakan akun tersebut."
        )

        tampilkan_login()

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Gagal menyimpan akun:\n{error}"
        )


# ============================================================
# HALAMAN LOGIN
# ============================================================

def tampilkan_login():
    global entry_username
    global entry_password_login
    global button_show_login
    global password_login_visible

    password_login_visible = False

    clear_window()

    create_title("LOGIN")

    tk.Label(
        window,
        text="Silakan login untuk menggunakan program.",
        font=FONT_SUBTITLE
    ).pack(pady=(0, 25))

    frame = tk.Frame(window)
    frame.pack()

    tk.Label(
        frame,
        text="Username",
        font=FONT_BOLD
    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

    entry_username = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=30
    )
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(
        frame,
        text="Password",
        font=FONT_BOLD
    ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

    password_frame = tk.Frame(frame)
    password_frame.grid(row=1, column=1, padx=10, pady=10)

    entry_password_login = tk.Entry(
        password_frame,
        font=FONT_NORMAL,
        width=25,
        show="*"
    )
    entry_password_login.pack(side="left")

    button_show_login = tk.Button(
        password_frame,
        text="👁",
        command=toggle_password_login,
        width=3,
        cursor="hand2"
    )
    button_show_login.pack(side="left", padx=(5, 0))

    create_button(
        window,
        "LOGIN",
        login,
        25
    ).pack(pady=(25, 10))

    create_button(
        window,
        "BUAT AKUN BARU",
        tampilkan_register,
        25
    ).pack()

    entry_username.focus()


# ============================================================
# HALAMAN REGISTER
# ============================================================

def tampilkan_register():
    global entry_username_daftar
    global entry_password_daftar
    global entry_konfirmasi
    global button_password
    global button_konfirmasi
    global password_daftar_visible
    global konfirmasi_visible

    password_daftar_visible = False
    konfirmasi_visible = False

    clear_window()

    create_title("BUAT AKUN")

    tk.Label(
        window,
        text="Buat akun baru untuk menggunakan program.",
        font=FONT_SUBTITLE
    ).pack(pady=(0, 25))

    frame = tk.Frame(window)
    frame.pack()

    tk.Label(
        frame,
        text="Username",
        font=FONT_BOLD
    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

    entry_username_daftar = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=30
    )
    entry_username_daftar.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(
        frame,
        text="Password",
        font=FONT_BOLD
    ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

    password_frame = tk.Frame(frame)
    password_frame.grid(row=1, column=1, padx=10, pady=10)

    entry_password_daftar = tk.Entry(
        password_frame,
        font=FONT_NORMAL,
        width=25,
        show="*"
    )
    entry_password_daftar.pack(side="left")

    button_password = tk.Button(
        password_frame,
        text="👁",
        command=toggle_password_daftar,
        width=3,
        cursor="hand2"
    )
    button_password.pack(side="left", padx=(5, 0))

    tk.Label(
        frame,
        text="Konfirmasi Password",
        font=FONT_BOLD
    ).grid(row=2, column=0, padx=10, pady=10, sticky="w")

    confirm_frame = tk.Frame(frame)
    confirm_frame.grid(row=2, column=1, padx=10, pady=10)

    entry_konfirmasi = tk.Entry(
        confirm_frame,
        font=FONT_NORMAL,
        width=25,
        show="*"
    )
    entry_konfirmasi.pack(side="left")

    button_konfirmasi = tk.Button(
        confirm_frame,
        text="👁",
        command=toggle_konfirmasi,
        width=3,
        cursor="hand2"
    )
    button_konfirmasi.pack(side="left", padx=(5, 0))

    create_button(
        window,
        "DAFTAR",
        daftar_akun,
        25
    ).pack(pady=(25, 10))

    create_button(
        window,
        "KEMBALI KE LOGIN",
        tampilkan_login,
        25
    ).pack()

    entry_username_daftar.focus()


# ============================================================
# DATA PENGGUNA
# ============================================================

def simpan_data_pengguna():
    global nama_login
    global kelas_login

    nama = entry_nama.get().strip()
    kelas = entry_kelas.get().strip()

    if nama == "" or kelas == "":
        messagebox.showwarning(
            "Peringatan",
            "Nama dan kelas harus diisi!"
        )
        return

    nama_login = nama
    kelas_login = kelas

    tampilkan_dashboard(username_login)


def tampilkan_data_pengguna():
    global entry_nama
    global entry_kelas

    clear_window()

    create_title("DATA PENGGUNA")

    tk.Label(
        window,
        text=f"Username: {username_login}",
        font=FONT_SUBTITLE
    ).pack(pady=(0, 20))

    frame = tk.Frame(window)
    frame.pack()

    tk.Label(
        frame,
        text="Nama",
        font=FONT_BOLD
    ).grid(row=0, column=0, padx=10, pady=10)

    entry_nama = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=30
    )
    entry_nama.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(
        frame,
        text="Kelas",
        font=FONT_BOLD
    ).grid(row=1, column=0, padx=10, pady=10)

    entry_kelas = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=30
    )
    entry_kelas.grid(row=1, column=1, padx=10, pady=10)

    create_button(
        window,
        "LANJUT KE DASHBOARD",
        simpan_data_pengguna,
        25
    ).pack(pady=30)

    entry_nama.focus()


# ============================================================
# TIMER
# ============================================================

def get_session_seconds():
    if session_start_time is None:
        return 0

    return int(time.perf_counter() - session_start_time)


def format_timer(seconds):
    jam = seconds // 3600
    menit = (seconds % 3600) // 60
    detik = seconds % 60

    return f"{jam:02d}:{menit:02d}:{detik:02d}"


def update_timer():
    global session_timer_job

    if session_start_time is None:
        return

    try:
        if timer_label is not None and timer_label.winfo_exists():
            timer_label.config(
                text=f"Durasi sesi: {format_timer(get_session_seconds())}"
            )

            session_timer_job = window.after(
                1000,
                update_timer
            )

    except tk.TclError:
        pass


# ============================================================
# SIMPAN SESSION
# ============================================================

def save_session(show_error=True):
    global session_saved

    if session_saved:
        return True

    if (
        session_start_time is None
        or username_login == ""
        or nama_login == ""
        or kelas_login == ""
    ):
        return False

    timer_seconds = get_session_seconds()

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO program
            (
                username,
                nama,
                kelas,
                timer
            )
            VALUES
            (%s, %s, %s, %s)
            """,
            (
                username_login,
                nama_login,
                kelas_login,
                timer_seconds
            )
        )

        conn.commit()

        program_id = cursor.lastrowid

        cursor.close()
        conn.close()

        print("Data sesi berhasil disimpan ke MySQL.")

        sheets_ok = save_to_google_sheets(
            [
                program_id,
                username_login,
                nama_login,
                kelas_login,
                timer_seconds
            ]
        )

        if sheets_ok:
            print("Data sesi berhasil disimpan ke Google Sheets.")
        else:
            print("MySQL berhasil, tetapi Google Sheets gagal.")

        session_saved = True
        return True

    except mysql.connector.Error as error:
        print("MySQL Error:", error)

        if show_error:
            messagebox.showerror(
                "Database Error",
                "Data sesi gagal disimpan ke MySQL.\n\n"
                f"{error}"
            )

        return False


# ============================================================
# LOGOUT
# ============================================================

def logout():
    global session_timer_job
    global session_start_time
    global username_login
    global nama_login
    global kelas_login

    if not messagebox.askyesno(
        "Logout",
        "Yakin ingin logout?\n\n"
        "Timer akan dihentikan dan data sesi disimpan."
    ):
        return

    if session_timer_job is not None:
        try:
            window.after_cancel(session_timer_job)
        except Exception:
            pass

        session_timer_job = None

    save_session()

    session_start_time = None
    username_login = ""
    nama_login = ""
    kelas_login = ""

    tampilkan_login()


# ============================================================
# DASHBOARD
# ============================================================

def tampilkan_dashboard(username=None):
    global timer_label

    clear_window()

    create_title("DASHBOARD")

    tk.Label(
        window,
        text=f"Selamat datang, {nama_login}!",
        font=get_font(14, "bold")
    ).pack()

    tk.Label(
        window,
        text=f"Username: {username_login} | Kelas: {kelas_login}",
        font=get_font(10)
    ).pack(pady=(2, 0))

    timer_label = tk.Label(
        window,
        text="Durasi sesi: 00:00:00",
        font=FONT_BOLD
    )
    timer_label.pack(pady=10)

    frame = tk.Frame(window)
    frame.pack(pady=10)

    buttons = [
        ("1. Ganjil / Genap", tampilkan_ganjil_genap),
        ("2. Luas Persegi Panjang", tampilkan_persegi_panjang),
        ("3. Luas Segitiga", tampilkan_segitiga),
        ("4. Tambah", tampilkan_tambah),
        ("5. Kurang", tampilkan_kurang),
        ("6. Kali", tampilkan_kali),
        ("7. Bagi", tampilkan_bagi),
    ]

    for index, (text, command) in enumerate(buttons):
        row = index // 2
        column = index % 2

        create_button(
            frame,
            text,
            command,
            28
        ).grid(
            row=row,
            column=column,
            padx=8,
            pady=6
        )

    create_button(
        frame,
        "LOGOUT",
        logout,
        28
    ).grid(
        row=4,
        column=0,
        columnspan=2,
        padx=8,
        pady=8
    )
    update_timer()


# ============================================================
# HALAMAN PROGRAM
# ============================================================

def program_page(title):
    clear_window()
    create_title(title)

    frame = tk.Frame(window)
    frame.pack(pady=20)

    return frame


def add_back_button():
    create_button(
        window,
        "KEMBALI KE DASHBOARD",
        tampilkan_dashboard,
        25
    ).pack(pady=20)


# ============================================================
# 1. GANJIL / GENAP
# ============================================================

def tampilkan_ganjil_genap():
    global entry_angka_ganjil

    frame = program_page("CEK GANJIL / GENAP")

    tk.Label(
        frame,
        text="Masukkan angka:",
        font=FONT_BOLD
    ).grid(row=0, column=0, padx=10, pady=10)

    entry_angka_ganjil = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=25
    )
    entry_angka_ganjil.grid(row=0, column=1, padx=10, pady=10)

    hasil = tk.Label(
        window,
        text="Hasil akan muncul di sini.",
        font=FONT_RESULT
    )
    hasil.pack(pady=10)

    def proses():
        try:
            angka = int(entry_angka_ganjil.get())

            # Memakai fungsi dari program lama
            hasil.config(
                text=Ganjil_Genap.cek_ganjil_genap(angka)
            )

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Masukkan bilangan bulat."
            )
        except AttributeError:
            messagebox.showerror(
                "Module Error",
                "Fungsi cek_ganjil_genap(x) belum ada "
                "di Ganjil_Genap.py."
            )

    create_button(
        window,
        "CEK",
        proses,
        25
    ).pack(pady=10)

    add_back_button()


# ============================================================
# 2. PERSEGI PANJANG
# ============================================================

def tampilkan_persegi_panjang():
    global entry_panjang
    global entry_lebar

    frame = program_page("LUAS PERSEGI PANJANG")

    tk.Label(
        frame,
        text="Panjang:",
        font=FONT_BOLD
    ).grid(row=0, column=0, padx=10, pady=10)

    entry_panjang = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=25
    )
    entry_panjang.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(
        frame,
        text="Lebar:",
        font=FONT_BOLD
    ).grid(row=1, column=0, padx=10, pady=10)

    entry_lebar = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=25
    )
    entry_lebar.grid(row=1, column=1, padx=10, pady=10)

    hasil = tk.Label(
        window,
        text="Hasil akan muncul di sini.",
        font=FONT_RESULT
    )
    hasil.pack(pady=10)

    def proses():
        try:
            panjang = float(entry_panjang.get())
            lebar = float(entry_lebar.get())

            nilai = Modul_Kalkulasi_Geometri.hitung_luas_persegi_panjang(
                panjang,
                lebar
            )

            hasil.config(text=f"Luas = {nilai}")

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Masukkan angka yang valid."
            )

    create_button(
        window,
        "HITUNG",
        proses,
        25
    ).pack(pady=10)

    add_back_button()


# ============================================================
# 3. SEGITIGA
# ============================================================

def tampilkan_segitiga():
    global entry_alas
    global entry_tinggi

    frame = program_page("LUAS SEGITIGA")

    tk.Label(
        frame,
        text="Alas:",
        font=FONT_BOLD
    ).grid(row=0, column=0, padx=10, pady=10)

    entry_alas = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=25
    )
    entry_alas.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(
        frame,
        text="Tinggi:",
        font=FONT_BOLD
    ).grid(row=1, column=0, padx=10, pady=10)

    entry_tinggi = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=25
    )
    entry_tinggi.grid(row=1, column=1, padx=10, pady=10)

    hasil = tk.Label(
        window,
        text="Hasil akan muncul di sini.",
        font=FONT_RESULT
    )
    hasil.pack(pady=10)

    def proses():
        try:
            alas = float(entry_alas.get())
            tinggi = float(entry_tinggi.get())

            nilai = Modul_Kalkulasi_Geometri.hitung_luas_segitiga(
                alas,
                tinggi
            )

            hasil.config(text=f"Luas = {nilai}")

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Masukkan angka yang valid."
            )

    create_button(
        window,
        "HITUNG",
        proses,
        25
    ).pack(pady=10)

    add_back_button()


# ============================================================
# 4-7. OPERASI BILANGAN
# ============================================================

def buat_halaman_operasi(judul, fungsi):
    global entry_operasi_a
    global entry_operasi_b

    frame = program_page(judul)

    tk.Label(
        frame,
        text="Bilangan pertama:",
        font=FONT_BOLD
    ).grid(row=0, column=0, padx=10, pady=10)

    entry_operasi_a = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=25
    )
    entry_operasi_a.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(
        frame,
        text="Bilangan kedua:",
        font=FONT_BOLD
    ).grid(row=1, column=0, padx=10, pady=10)

    entry_operasi_b = tk.Entry(
        frame,
        font=FONT_NORMAL,
        width=25
    )
    entry_operasi_b.grid(row=1, column=1, padx=10, pady=10)

    hasil = tk.Label(
        window,
        text="Hasil akan muncul di sini.",
        font=FONT_RESULT
    )
    hasil.pack(pady=10)

    def proses():
        try:
            a = float(entry_operasi_a.get())
            b = float(entry_operasi_b.get())

            nilai = fungsi(a, b)

            hasil.config(text=f"Hasil = {nilai}")

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Masukkan angka yang valid."
            )

    create_button(
        window,
        "HITUNG",
        proses,
        25
    ).pack(pady=10)

    add_back_button()


def tampilkan_tambah():
    buat_halaman_operasi(
        "PENJUMLAHAN",
        Modul_Operasi_Bilangan.tambah
    )


def tampilkan_kurang():
    buat_halaman_operasi(
        "PENGURANGAN",
        Modul_Operasi_Bilangan.kurang
    )


def tampilkan_kali():
    buat_halaman_operasi(
        "PERKALIAN",
        Modul_Operasi_Bilangan.kali
    )


def tampilkan_bagi():
    buat_halaman_operasi(
        "PEMBAGIAN",
        Modul_Operasi_Bilangan.bagi
    )


# ============================================================
# CLOSE WINDOW
# ============================================================

def on_closing():
    global session_timer_job

    if session_start_time is None:
        window.destroy()
        return

    if not messagebox.askyesno(
        "Keluar Program",
        "Sesi masih berjalan.\n\n"
        "Keluar dan simpan data sesi?"
    ):
        return

    if session_timer_job is not None:
        try:
            window.after_cancel(session_timer_job)
        except Exception:
            pass

        session_timer_job = None

    save_session(show_error=True)
    window.destroy()


window.protocol(
    "WM_DELETE_WINDOW",
    on_closing
)


# ============================================================
# START
# ============================================================

tampilkan_login()
window.mainloop()
