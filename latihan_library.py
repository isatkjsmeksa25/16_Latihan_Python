import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


print("=== PROGRAM ANALISIS NILAI SISWA ===")

# Meminta jumlah siswa
jumlah = int(input("Masukkan jumlah siswa: "))

nama = []
nilai = []

# Input data setiap siswa
for i in range(jumlah):
    print(f"\nData siswa ke-{i + 1}")

    nama_siswa = input("Nama: ")
    nilai_siswa = float(input("Nilai: "))

    nama.append(nama_siswa)
    nilai.append(nilai_siswa)


# =========================
# NUMPY
# =========================

data_nilai = np.array(nilai)

print("\n=== HASIL NUMPY ===")
print("Nilai tertinggi :", np.max(data_nilai))
print("Nilai terendah  :", np.min(data_nilai))
print("Nilai rata-rata  :", np.mean(data_nilai))


# =========================
# PANDAS
# =========================

data = {
    "Nama": nama,
    "Nilai": nilai
}

df = pd.DataFrame(data)

print("\n=== DATA SISWA ===")
print(df)


# =========================
# MATPLOTLIB
# =========================

plt.bar(df["Nama"], df["Nilai"])

plt.title("Grafik Nilai Siswa")
plt.xlabel("Nama Siswa")
plt.ylabel("Nilai")

plt.ylim(0, 100)
plt.grid(axis="y")

plt.show()