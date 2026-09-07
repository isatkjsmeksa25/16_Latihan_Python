import gspread
from google.oauth2.service_account import Credentials

# ==============================
# KONEKSI GOOGLE SHEETS
# ==============================

CREDENTIALS_FILE = "Credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open("ISA_Database Program MySQL")
sheet = spreadsheet.get_worksheet(0)


# ==============================
# TES MENULIS DATA
# ==============================

data = [
    ["ID", "USERNAME", "NAMA", "KELAS", "TIMER"],
    [1, "isa", "Isa Fadhil Lufthansa Zhuliand", "XI TKJ 1", 15]
]

# Menulis data ke spreadsheet
sheet.clear()
sheet.update("A1", data)

print("================================")
print("   DATA BERHASIL DIKIRIM")
print("================================")
print("Spreadsheet :", spreadsheet.title)
print("Worksheet   :", sheet.title)
print("================================")