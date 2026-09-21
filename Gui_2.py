import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont

import mysql.connector
import gspread

import os
import sys
import ctypes
import time

from pathlib import Path
from google.oauth2.service_account import Credentials


# ============================================================
# PATH PROJECT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

BELAJAR_MODUL_DIR = BASE_DIR / "Belajar_Modul"
PYTHON_MYSQL_DIR = BASE_DIR / "python_mysql"
FONT_DIR = BASE_DIR / "fonts"

# Tambahkan folder Belajar_Modul ke sys.path
if str(BELAJAR_MODUL_DIR) not in sys.path:
    sys.path.insert(0, str(BELAJAR_MODUL_DIR))


# ============================================================
# IMPORT PROGRAM LAMA
# ============================================================

import Ganjil_Genap
import Modul_Kalkulasi_Geometri
import Modul_Operasi_Bilangan


# ============================================================
# KONFIGURASI MYSQL
# ============================================================

from dotenv import load_dotenv

load_dotenv(BASE_DIR / ".env")

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "1$@16DtBAseKiWi")
MYSQL_DATABASE = os.getenv(
    "MYSQL_DATABASE",
    "database_program"
)


# ============================================================
# KONEKSI MYSQL
# ============================================================

def get_mysql_connection():

    if not MYSQL_PASSWORD:
        raise RuntimeError(
            "MYSQL_PASSWORD tidak ditemukan di file .env"
        )

    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# ============================================================
# KONFIGURASI GOOGLE SHEETS
# ============================================================

GOOGLE_CREDENTIALS = PYTHON_MYSQL_DIR / "Credentials.json"

SPREADSHEET_NAME = "ISA_Database Program MySQL"
WORKSHEET_NAME = "Sheet1"


# ============================================================
# KONFIGURASI FONT
# ============================================================

FONT_FILES = {
    "bingboss": "Bing Boss.otf",
    "chernobyl": "Chernobyl.otf",
    "jai": "JAi_____.TTF",
}


# Nama internal font yang sudah terdeteksi
FONT_FAMILY = {
    "bingboss": "Bing Boss",
    "chernobyl": "Chernobyl",
    "jai": "JAi",
}


# ============================================================
# LOAD FONT WINDOWS
# ============================================================

def load_font_windows(font_path):

    if not font_path.exists():

        print(
            f"Font tidak ditemukan: {font_path}"
        )

        return False

    FR_PRIVATE = 0x10

    result = ctypes.windll.gdi32.AddFontResourceExW(
        str(font_path),
        FR_PRIVATE,
        0
    )

    if result > 0:

        print(
            f"Berhasil memuat font: {font_path.name}"
        )

        return True

    print(
        f"Gagal memuat font: {font_path.name}"
    )

    return False


# ============================================================
# LOAD SEMUA FONT
# ============================================================

def load_all_fonts():

    for filename in FONT_FILES.values():

        font_path = FONT_DIR / filename

        load_font_windows(font_path)


# ============================================================
# CARI FAMILY FONT
# ============================================================

def find_font_family(root, keyword, fallback):

    families = tkfont.families(root)

    keyword = keyword.lower()

    for family in families:

        if keyword in family.lower():

            return family

    return fallback


# ============================================================
# GOOGLE SHEETS
# ============================================================

def save_to_google_sheets(
    username,
    nama,
    kelas,
    timer
):

    try:

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = Credentials.from_service_account_file(
            str(GOOGLE_CREDENTIALS),
            scopes=scopes
        )

        client = gspread.authorize(
            credentials
        )

        spreadsheet = client.open(
            SPREADSHEET_NAME
        )

        worksheet = spreadsheet.worksheet(
            WORKSHEET_NAME
        )

        values = worksheet.get_all_values()

        if len(values) <= 1:

            next_id = 1

        else:

            next_id = len(values)

        worksheet.append_row(
            [
                next_id,
                username,
                nama,
                kelas,
                timer
            ],
            value_input_option="USER_ENTERED"
        )

        print(
            "Data berhasil dikirim ke Google Sheets."
        )

    except Exception as e:

        print(
            "Gagal menyimpan ke Google Sheets:"
        )

        print(e)


# ============================================================
# CLASS PROGRAM GUI
# ============================================================

class ProgramGUI:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.root.title(
            "Koleksi My Prrogram Gweh"
        )

        self.root.geometry(
            "900x600"
        )

        self.root.resizable(
            False,
            False
        )


        # ----------------------------------------------------
        # LOAD FONT
        # ----------------------------------------------------

        load_all_fonts()


        self.font_bingboss = find_font_family(
            root,
            "bing boss",
            "Bing Boss"
        )

        self.font_chernobyl = find_font_family(
            root,
            "chernobyl",
            "Chernobyl"
        )

        self.font_jai = find_font_family(
            root,
            "jai",
            "JAi"
        )


        print()

        print(
            "Font yang digunakan:"
        )

        print(
            "Bing Boss :",
            self.font_bingboss
        )

        print(
            "Chernobyl :",
            self.font_chernobyl
        )

        print(
            "JAi       :",
            self.font_jai
        )

        print()


        # ----------------------------------------------------
        # SESSION
        # ----------------------------------------------------

        self.username = None

        self.nama = ""

        self.kelas = ""

        self.session_start = None

        self.session_saved = False


        # ----------------------------------------------------
        # CLOSE WINDOW
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )


        # ----------------------------------------------------
        # START LOGIN
        # ----------------------------------------------------

        self.show_login()


    # ========================================================
    # CLEAR WINDOW
    # ========================================================

    def clear_window(self):

        for widget in self.root.winfo_children():

            widget.destroy()


    # ========================================================
    # LABEL
    # ========================================================

    def make_label(
        self,
        parent,
        text,
        font_type="jai",
        size=18,
        **kwargs
    ):

        if font_type == "bingboss":

            family = self.font_bingboss

        elif font_type == "chernobyl":

            family = self.font_chernobyl

        else:

            family = self.font_jai


        return tk.Label(
            parent,
            text=text,
            font=(family, size),
            **kwargs
        )


    # ========================================================
    # BUTTON
    # ========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        size=18,
        **kwargs
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=(self.font_bingboss, size),
            cursor="hand2",
            **kwargs
        )


    # ========================================================
    # LOGIN PAGE
    # ========================================================

    def show_login(self):

        self.clear_window()


        frame = tk.Frame(
            self.root
        )

        frame.pack(
            expand=True
        )


        # ----------------------------------------------------
        # JUDUL
        # ----------------------------------------------------

        self.make_label(
            frame,
            "Koleksi My Prrogram Gweh",
            "bingboss",
            34
        ).pack(
            pady=(0, 5)
        )


        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

        self.make_label(
            frame,
            "LOGIN",
            "chernobyl",
            48
        ).pack(
            pady=(0, 30)
        )


        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        self.make_label(
            frame,
            "Username",
            "jai",
            18
        ).pack()


        self.login_username = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=25
        )

        self.login_username.pack(
            pady=(5, 15)
        )


        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        self.make_label(
            frame,
            "Password",
            "jai",
            18
        ).pack()


        password_frame = tk.Frame(
            frame
        )

        password_frame.pack(
            pady=(5, 20)
        )


        self.login_password = tk.Entry(
            password_frame,
            font=(self.font_jai, 18),
            width=20,
            show="*"
        )

        self.login_password.pack(
            side="left"
        )


        self.login_password_visible = False


        self.login_password_button = tk.Button(
            password_frame,
            text="SHOW",
            font=(self.font_bingboss, 12),
            command=self.toggle_login_password
        )

        self.login_password_button.pack(
            side="left",
            padx=(8, 0)
        )


        # ----------------------------------------------------
        # LOGIN BUTTON
        # ----------------------------------------------------

        self.make_button(
            frame,
            "[ LOGIN ]",
            self.login,
            20,
            width=18
        ).pack(
            pady=5
        )


        # ----------------------------------------------------
        # REGISTER BUTTON
        # ----------------------------------------------------

        self.make_button(
            frame,
            "[ BUAT AKUN BARU ]",
            self.show_register,
            18,
            width=22
        ).pack(
            pady=5
        )


        self.login_username.focus_set()


    # ========================================================
    # TOGGLE LOGIN PASSWORD
    # ========================================================

    def toggle_login_password(self):

        self.login_password_visible = (
            not self.login_password_visible
        )


        if self.login_password_visible:

            self.login_password.config(
                show=""
            )

            self.login_password_button.config(
                text="HIDE"
            )

        else:

            self.login_password.config(
                show="*"
            )

            self.login_password_button.config(
                text="SHOW"
            )


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        username = (
            self.login_username
            .get()
            .strip()
        )

        password = (
            self.login_password
            .get()
        )


        if not username or not password:

            messagebox.showwarning(
                "Login",
                "Username dan password wajib diisi."
            )

            return


        try:

            conn = get_mysql_connection()

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE username = %s
                AND password = %s
                """,
                (
                    username,
                    password
                )
            )


            result = cursor.fetchone()


            cursor.close()

            conn.close()


            if result is None:

                messagebox.showerror(
                    "Login Gagal",
                    "Username atau password salah."
                )

                return


            # ------------------------------------------------
            # LOGIN BERHASIL
            # ------------------------------------------------

            self.username = username

            self.session_start = (
                time.perf_counter()
            )

            self.session_saved = False


            self.ask_identity()


        except mysql.connector.Error as e:

            messagebox.showerror(
                "MySQL Error",
                str(e)
            )


    # ========================================================
    # DATA NAMA + KELAS
    # ========================================================

    def ask_identity(self):

        self.clear_window()


        frame = tk.Frame(
            self.root
        )

        frame.pack(
            expand=True
        )


        self.make_label(
            frame,
            "DATA PENGGUNA",
            "chernobyl",
            38
        ).pack(
            pady=(0, 30)
        )


        # ----------------------------------------------------
        # NAMA
        # ----------------------------------------------------

        self.make_label(
            frame,
            "Nama",
            "jai",
            18
        ).pack()


        self.nama_entry = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=25
        )

        self.nama_entry.pack(
            pady=(5, 15)
        )


        # ----------------------------------------------------
        # KELAS
        # ----------------------------------------------------

        self.make_label(
            frame,
            "Kelas",
            "jai",
            18
        ).pack()


        self.kelas_entry = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=25
        )

        self.kelas_entry.pack(
            pady=(5, 20)
        )


        # ----------------------------------------------------
        # LANJUT
        # ----------------------------------------------------

        self.make_button(
            frame,
            "[ LANJUT ]",
            self.save_identity,
            20,
            width=18
        ).pack()


        self.nama_entry.focus_set()


    # ========================================================
    # SAVE IDENTITY
    # ========================================================

    def save_identity(self):

        self.nama = (
            self.nama_entry
            .get()
            .strip()
        )

        self.kelas = (
            self.kelas_entry
            .get()
            .strip()
        )


        if not self.nama or not self.kelas:

            messagebox.showwarning(
                "Data",
                "Nama dan kelas wajib diisi."
            )

            return


        self.show_dashboard()


    # ========================================================
    # REGISTER PAGE
    # ========================================================

    def show_register(self):

        self.clear_window()


        frame = tk.Frame(
            self.root
        )

        frame.pack(
            expand=True
        )


        self.make_label(
            frame,
            "BUAT AKUN BARU",
            "chernobyl",
            38
        ).pack(
            pady=(0, 25)
        )


        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        self.make_label(
            frame,
            "Username",
            "jai",
            18
        ).pack()


        self.register_username = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=25
        )

        self.register_username.pack(
            pady=(5, 15)
        )


        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        self.make_label(
            frame,
            "Password",
            "jai",
            18
        ).pack()


        password_frame = tk.Frame(
            frame
        )

        password_frame.pack(
            pady=(5, 15)
        )


        self.register_password = tk.Entry(
            password_frame,
            font=(self.font_jai, 18),
            width=20,
            show="*"
        )

        self.register_password.pack(
            side="left"
        )


        self.register_password_visible = False


        self.register_password_button = tk.Button(
            password_frame,
            text="SHOW",
            font=(self.font_bingboss, 12),
            command=self.toggle_register_password
        )

        self.register_password_button.pack(
            side="left",
            padx=(8, 0)
        )


        # ----------------------------------------------------
        # CONFIRM PASSWORD
        # ----------------------------------------------------

        self.make_label(
            frame,
            "Konfirmasi Password",
            "jai",
            18
        ).pack()


        self.register_confirm = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=25,
            show="*"
        )

        self.register_confirm.pack(
            pady=(5, 20)
        )


        # ----------------------------------------------------
        # BUTTON
        # ----------------------------------------------------

        self.make_button(
            frame,
            "[ BUAT AKUN ]",
            self.register,
            20,
            width=18
        ).pack(
            pady=5
        )


        self.make_button(
            frame,
            "[ KEMBALI ]",
            self.show_login,
            18,
            width=18
        ).pack(
            pady=5
        )


        self.register_username.focus_set()


    # ========================================================
    # TOGGLE REGISTER PASSWORD
    # ========================================================

    def toggle_register_password(self):

        self.register_password_visible = (
            not self.register_password_visible
        )


        if self.register_password_visible:

            self.register_password.config(
                show=""
            )

            self.register_confirm.config(
                show=""
            )

            self.register_password_button.config(
                text="HIDE"
            )

        else:

            self.register_password.config(
                show="*"
            )

            self.register_confirm.config(
                show="*"
            )

            self.register_password_button.config(
                text="SHOW"
            )


    # ========================================================
    # REGISTER
    # ========================================================

    def register(self):

        username = (
            self.register_username
            .get()
            .strip()
        )

        password = (
            self.register_password
            .get()
        )

        confirm = (
            self.register_confirm
            .get()
        )


        if not username or not password or not confirm:

            messagebox.showwarning(
                "Register",
                "Semua data wajib diisi."
            )

            return


        if password != confirm:

            messagebox.showerror(
                "Register",
                "Konfirmasi password tidak sama."
            )

            return


        try:

            conn = get_mysql_connection()

            cursor = conn.cursor()


            # ------------------------------------------------
            # CEK USERNAME
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE username = %s
                """,
                (username,)
            )


            if cursor.fetchone():

                cursor.close()

                conn.close()

                messagebox.showerror(
                    "Register",
                    "Username sudah digunakan."
                )

                return


            # ------------------------------------------------
            # INSERT USER
            # ------------------------------------------------

            cursor.execute(
                """
                INSERT INTO users
                (username, password)
                VALUES (%s, %s)
                """,
                (
                    username,
                    password
                )
            )


            conn.commit()


            cursor.close()

            conn.close()


            messagebox.showinfo(
                "Berhasil",
                "Akun berhasil dibuat."
            )


            self.show_login()


        except mysql.connector.Error as e:

            messagebox.showerror(
                "MySQL Error",
                str(e)
            )


    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_window()


        frame = tk.Frame(
            self.root
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.make_label(
            frame,
            "KOLEKSI PROGRAM",
            "chernobyl",
            38
        ).pack(
            pady=(0, 5)
        )


        self.make_label(
            frame,
            f"Username : {self.username}",
            "jai",
            16
        ).pack()


        self.make_label(
            frame,
            f"Nama : {self.nama}",
            "jai",
            16
        ).pack()


        self.make_label(
            frame,
            f"Kelas : {self.kelas}",
            "jai",
            16
        ).pack(
            pady=(0, 20)
        )


        # ----------------------------------------------------
        # PROGRAM BUTTON
        # ----------------------------------------------------

        button_frame = tk.Frame(
            frame
        )

        button_frame.pack()


        programs = [

            (
                "1. GANJIL / GENAP",
                self.program_ganjil_genap
            ),

            (
                "2. LUAS PERSEGI PANJANG",
                self.program_persegi_panjang
            ),

            (
                "3. LUAS SEGITIGA",
                self.program_segitiga
            ),

            (
                "4. TAMBAH",
                self.program_tambah
            ),

            (
                "5. KURANG",
                self.program_kurang
            ),

            (
                "6. KALI",
                self.program_kali
            ),

            (
                "7. BAGI",
                self.program_bagi
            ),

        ]


        for index, (text, command) in enumerate(programs):

            row = index // 2

            column = index % 2


            self.make_button(
                button_frame,
                text,
                command,
                16,
                width=25,
                height=2
            ).grid(
                row=row,
                column=column,
                padx=10,
                pady=10
            )


        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        self.make_button(
            frame,
            "[ LOGOUT ]",
            self.logout,
            18,
            width=18
        ).pack(
            pady=(20, 5)
        )


    # ========================================================
    # PROGRAM WINDOW
    # ========================================================

    def program_window(self, title):

        self.clear_window()


        frame = tk.Frame(
            self.root
        )

        frame.pack(
            expand=True
        )


        self.make_label(
            frame,
            title,
            "chernobyl",
            36
        ).pack(
            pady=(0, 30)
        )


        return frame


    # ========================================================
    # PROGRAM 1
    # GANJIL / GENAP
    # ========================================================

    def program_ganjil_genap(self):

        frame = self.program_window(
            "GANJIL / GENAP"
        )


        self.make_label(
            frame,
            "Masukkan angka",
            "jai",
            18
        ).pack()


        entry = tk.Entry(
            frame,
            font=(self.font_jai, 20),
            width=20
        )

        entry.pack(
            pady=10
        )


        result_label = self.make_label(
            frame,
            "",
            "jai",
            18
        )

        result_label.pack(
            pady=10
        )


        def hitung():

            try:

                x = int(
                    entry.get()
                )


                hasil = (
                    Ganjil_Genap
                    .cek_ganjil_genap(x)
                )


                result_label.config(
                    text=hasil
                )


            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Masukkan angka yang valid."
                )


        self.make_button(
            frame,
            "[ HITUNG ]",
            hitung,
            20,
            width=18
        ).pack(
            pady=10
        )


        self.make_button(
            frame,
            "[ KEMBALI KE DASHBOARD ]",
            self.show_dashboard,
            18,
            width=24
        ).pack(
            pady=10
        )


        entry.focus_set()


    # ========================================================
    # PROGRAM 2
    # LUAS PERSEGI PANJANG
    # ========================================================

    def program_persegi_panjang(self):

        frame = self.program_window(
            "LUAS PERSEGI PANJANG"
        )


        self.make_label(
            frame,
            "Panjang",
            "jai",
            18
        ).pack()


        panjang_entry = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=20
        )

        panjang_entry.pack(
            pady=5
        )


        self.make_label(
            frame,
            "Lebar",
            "jai",
            18
        ).pack()


        lebar_entry = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=20
        )

        lebar_entry.pack(
            pady=5
        )


        result = self.make_label(
            frame,
            "",
            "jai",
            18
        )

        result.pack(
            pady=15
        )


        def hitung():

            try:

                panjang = float(
                    panjang_entry.get()
                )

                lebar = float(
                    lebar_entry.get()
                )


                luas = (
                    Modul_Kalkulasi_Geometri
                    .hitung_luas_persegi_panjang(
                        panjang,
                        lebar
                    )
                )


                result.config(
                    text=f"Luas = {luas}"
                )


            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Input harus berupa angka."
                )


        self.make_button(
            frame,
            "[ HITUNG ]",
            hitung,
            20,
            width=18
        ).pack(
            pady=10
        )


        self.make_button(
            frame,
            "[ KEMBALI KE DASHBOARD ]",
            self.show_dashboard,
            18,
            width=24
        ).pack(
            pady=10
        )


    # ========================================================
    # PROGRAM 3
    # LUAS SEGITIGA
    # ========================================================

    def program_segitiga(self):

        frame = self.program_window(
            "LUAS SEGITIGA"
        )


        self.make_label(
            frame,
            "Alas",
            "jai",
            18
        ).pack()


        alas_entry = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=20
        )

        alas_entry.pack(
            pady=5
        )


        self.make_label(
            frame,
            "Tinggi",
            "jai",
            18
        ).pack()


        tinggi_entry = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=20
        )

        tinggi_entry.pack(
            pady=5
        )


        result = self.make_label(
            frame,
            "",
            "jai",
            18
        )

        result.pack(
            pady=15
        )


        def hitung():

            try:

                alas = float(
                    alas_entry.get()
                )

                tinggi = float(
                    tinggi_entry.get()
                )


                luas = (
                    Modul_Kalkulasi_Geometri
                    .hitung_luas_segitiga(
                        alas,
                        tinggi
                    )
                )


                result.config(
                    text=f"Luas = {luas}"
                )


            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Input harus berupa angka."
                )


        self.make_button(
            frame,
            "[ HITUNG ]",
            hitung,
            20,
            width=18
        ).pack(
            pady=10
        )


        self.make_button(
            frame,
            "[ KEMBALI KE DASHBOARD ]",
            self.show_dashboard,
            18,
            width=24
        ).pack(
            pady=10
        )


    # ========================================================
    # OPERATION WINDOW
    # ========================================================

    def operation_window(
        self,
        title,
        operation
    ):

        frame = self.program_window(
            title
        )


        self.make_label(
            frame,
            "Bilangan pertama",
            "jai",
            18
        ).pack()


        a_entry = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=20
        )

        a_entry.pack(
            pady=5
        )


        self.make_label(
            frame,
            "Bilangan kedua",
            "jai",
            18
        ).pack()


        b_entry = tk.Entry(
            frame,
            font=(self.font_jai, 18),
            width=20
        )

        b_entry.pack(
            pady=5
        )


        result = self.make_label(
            frame,
            "",
            "jai",
            18
        )

        result.pack(
            pady=15
        )


        def hitung():

            try:

                a = float(
                    a_entry.get()
                )

                b = float(
                    b_entry.get()
                )


                hasil = operation(
                    a,
                    b
                )


                result.config(
                    text=f"Hasil = {hasil}"
                )


            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Input harus berupa angka."
                )


        self.make_button(
            frame,
            "[ HITUNG ]",
            hitung,
            20,
            width=18
        ).pack(
            pady=10
        )


        self.make_button(
            frame,
            "[ KEMBALI KE DASHBOARD ]",
            self.show_dashboard,
            18,
            width=24
        ).pack(
            pady=10
        )


    # ========================================================
    # PROGRAM 4
    # TAMBAH
    # ========================================================

    def program_tambah(self):

        self.operation_window(
            "PERTAMBAHAN",
            Modul_Operasi_Bilangan.tambah
        )


    # ========================================================
    # PROGRAM 5
    # KURANG
    # ========================================================

    def program_kurang(self):

        self.operation_window(
            "PENGURANGAN",
            Modul_Operasi_Bilangan.kurang
        )


    # ========================================================
    # PROGRAM 6
    # KALI
    # ========================================================

    def program_kali(self):

        self.operation_window(
            "PERKALIAN",
            Modul_Operasi_Bilangan.kali
        )


    # ========================================================
    # PROGRAM 7
    # BAGI
    # ========================================================

    def program_bagi(self):

        self.operation_window(
            "PEMBAGIAN",
            Modul_Operasi_Bilangan.bagi
        )


    # ========================================================
    # HITUNG TIMER
    # ========================================================

    def get_session_timer(self):

        if self.session_start is None:

            return 0


        elapsed = (
            time.perf_counter()
            - self.session_start
        )


        return int(elapsed)


    # ========================================================
    # SIMPAN SESSION
    # ========================================================

    def save_session(self):

        if self.session_saved:

            return


        if self.username is None:

            return


        if self.session_start is None:

            return


        timer = self.get_session_timer()


        try:

            conn = get_mysql_connection()

            cursor = conn.cursor()


            # ------------------------------------------------
            # MYSQL
            # ------------------------------------------------

            cursor.execute(
                """
                INSERT INTO program
                (username, nama, kelas, timer)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    self.username,
                    self.nama,
                    self.kelas,
                    timer
                )
            )


            conn.commit()


            cursor.close()

            conn.close()


            # ------------------------------------------------
            # GOOGLE SHEETS
            # ------------------------------------------------

            save_to_google_sheets(
                self.username,
                self.nama,
                self.kelas,
                timer
            )


            self.session_saved = True


            print(
                f"Session disimpan. "
                f"Timer: {timer} detik"
            )


        except mysql.connector.Error as e:

            print(
                "Gagal menyimpan session ke MySQL:"
            )

            print(e)


    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        self.save_session()


        self.username = None

        self.nama = ""

        self.kelas = ""

        self.session_start = None

        self.session_saved = False


        self.show_login()


    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        self.save_session()

        self.root.destroy()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ProgramGUI(
        root
    )

    root.mainloop()