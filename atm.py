import datetime
import os
import tkinter as tk
from tkinter import messagebox, ttk


NOMINAL_PILIHAN = (50000, 100000, 200000, 500000)


def format_rupiah(amount):
    return f"Rp{amount:,}".replace(",", ".")


class BankATM:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Kelompok 1 😎")
        self.root.geometry("820x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#f3f8ff")

        # Akun hanya tersimpan di memori selama aplikasi berjalan.
        self.akun = {}
        self.username = ""
        self.jenis_kelamin = ""

        self.saldo = 0
        self.transaksi = []
        self.gambar_atm = None
        self.mode_halaman = "login"

        self.tampilkan_halaman_pertama()
        self.root.protocol("WM_DELETE_WINDOW", self.keluar)

    def bersihkan_halaman(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tampilkan_halaman_pertama(self, mode="login"):
        self.bersihkan_halaman()
        self.mode_halaman = mode

        halaman = tk.Frame(self.root, bg="#f3f8ff")
        halaman.pack(fill="both", expand=True)

        tk.Label(
            halaman,
            text="ATM Kelompok 1 😎",
            bg="#f3f8ff",
            fg="#1677b8",
            font=("Arial", 25, "bold")
        ).pack(pady=(40, 8))

        tk.Label(
            halaman,
            text="Ayo isi data dirinya, Mas/Mbak!",
            bg="#f3f8ff",
            fg="#52616b",
            font=("Arial", 12)
        ).pack(pady=(0, 20))

        formulir = tk.Frame(
            halaman,
            bg="white",
            padx=30,
            pady=22,
            highlightbackground="#c5dff0",
            highlightthickness=1
        )
        formulir.pack()

        tk.Label(
            formulir,
            text="Username",
            bg="white",
            fg="#29353d",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        entri_username = tk.Entry(formulir, width=32, font=("Arial", 11))
        entri_username.grid(row=1, column=0, pady=(0, 12))

        tk.Label(
            formulir,
            text="Kata sandi",
            bg="white",
            fg="#29353d",
            font=("Arial", 10, "bold")
        ).grid(row=2, column=0, sticky="w", pady=(0, 5))

        entri_password = tk.Entry(
            formulir,
            width=32,
            font=("Arial", 11),
            show="*"
        )
        entri_password.grid(row=3, column=0, pady=(0, 12))

        tk.Label(
            formulir,
            text="Kamu Mas atau Mbak?",
            bg="white",
            fg="#29353d",
            font=("Arial", 10, "bold")
        ).grid(row=4, column=0, sticky="w", pady=(0, 5))

        pilihan_gender = tk.StringVar(value="")

        pilihan_frame = tk.Frame(formulir, bg="white")
        pilihan_frame.grid(row=5, column=0, sticky="w", pady=(0, 16))

        tk.Radiobutton(
            pilihan_frame,
            text="Mas",
            variable=pilihan_gender,
            value="Mas",
            bg="white",
            activebackground="white",
            font=("Arial", 10)
        ).pack(side="left", padx=(0, 18))

        tk.Radiobutton(
            pilihan_frame,
            text="Mbak",
            variable=pilihan_gender,
            value="Mbak",
            bg="white",
            activebackground="white",
            font=("Arial", 10)
        ).pack(side="left")

        def ambil_data():
            username = entri_username.get().strip()
            password = entri_password.get()
            gender = pilihan_gender.get()

            if not username or not password or gender not in ("Mas", "Mbak"):
                messagebox.showwarning(
                    "Data belum lengkap",
                    "Isi username, kata sandi, dan pilih Mas atau Mbak.",
                    parent=self.root
                )
                return None

            return username, password, gender

        def daftar():
            data = ambil_data()
            if data is None:
                return

            username, password, gender = data

            if username in self.akun:
                messagebox.showerror(
                    "Usernamenya udah terdaftar",
                    "Usernamenya udah terdaftar. Silakan masuk.",
                    parent=self.root
                )
                return

            self.akun[username] = {
                "password": password,
                "jenis_kelamin": gender
            }

            messagebox.showinfo(
                "Pendaftaran berhasil",
                f"Akunnya berhasil dibikin, {gender} {username}. Silakan masuk.",
                parent=self.root
            )

            entri_password.delete(0, tk.END)
            pilihan_gender.set("")
            entri_username.focus_set()

        def masuk():
            data = ambil_data()
            if data is None:
                return

            username, password, gender = data
            akun = self.akun.get(username)

            if (
                akun is None
                or akun["password"] != password
                or akun["jenis_kelamin"] != gender
            ):
                pesan = (
                    "Maaf, username atau kata sandi atau jenis "
                    "kelaminnya salah Mas/Mbak."
                )
                print(pesan)
                messagebox.showerror(
                    "Login gagal",
                    pesan,
                    parent=self.root
                )
                return

            self.username = username
            self.jenis_kelamin = gender
            self.tampilkan_halaman_transaksi()

        tombol = tk.Frame(formulir, bg="white")
        tombol.grid(row=6, column=0, pady=(0, 8))

        tk.Button(
            tombol,
            text="Daftar",
            command=daftar,
            bg="#20a36a",
            fg="white",
            activebackground="#188655",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=12,
            height=2
        ).pack(side="left", padx=5)

        tk.Button(
            tombol,
            text="Masuk",
            command=masuk,
            bg="#1677b8",
            fg="white",
            activebackground="#125f92",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=12,
            height=2
        ).pack(side="left", padx=5)

        tk.Button(
            formulir,
            text="Keluar",
            command=self.keluar,
            bg="#6c757d",
            fg="white",
            activebackground="#5c636a",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=26,
            height=2
        ).grid(row=7, column=0, pady=(5, 0))

        entri_username.bind("<Return>", lambda event: entri_password.focus_set())
        entri_password.bind("<Return>", lambda event: masuk())
        entri_username.focus_set()

    def tampilkan_halaman_transaksi(self):
        self.bersihkan_halaman()

        halaman = tk.Frame(self.root, bg="#f3f8ff")
        halaman.pack(fill="both", expand=True)

        header = tk.Frame(halaman, bg="#1677b8", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="ATM Kelompok 1 😎",
            bg="#1677b8",
            fg="white",
            font=("Arial", 22, "bold")
        ).pack(pady=(8, 0))

        tk.Label(
            header,
            text=(
                f"Selamat datang di ATM kelompok 1, "
                f"{self.jenis_kelamin} {self.username} 🙏🏻"
            ),
            bg="#1677b8",
            fg="#e7f6ff",
            font=("Arial", 11)
        ).pack()

        konten = tk.Frame(halaman, bg="#f3f8ff")
        konten.pack(fill="both", expand=True, padx=18, pady=14)

        area_atas = tk.Frame(konten, bg="#f3f8ff")
        area_atas.pack(fill="x")

        self.panel_gambar = tk.Frame(
            area_atas,
            bg="white",
            width=320,
            height=230,
            highlightbackground="#c5dff0",
            highlightthickness=1
        )
        self.panel_gambar.pack(side="left", padx=(0, 14))
        self.panel_gambar.pack_propagate(False)
        self.tampilkan_gambar_atm()

        panel_aksi = tk.Frame(area_atas, bg="#f3f8ff")
        panel_aksi.pack(side="left", fill="both", expand=True)

        kartu_saldo = tk.Frame(
            panel_aksi,
            bg="white",
            highlightbackground="#c5dff0",
            highlightthickness=1
        )
        kartu_saldo.pack(fill="x", pady=(0, 12))

        tk.Label(
            kartu_saldo,
            text=(
                f"Saldo {self.jenis_kelamin} {self.username} "
                "sekarang segini"
            ),
            bg="white",
            fg="#52616b",
            font=("Arial", 10),
            wraplength=420,
            justify="left"
        ).pack(anchor="w", padx=16, pady=(12, 0))

        self.label_saldo = tk.Label(
            kartu_saldo,
            text=format_rupiah(self.saldo),
            bg="white",
            fg="#1677b8",
            font=("Arial", 24, "bold")
        )
        self.label_saldo.pack(anchor="w", padx=16, pady=(2, 12))

        tk.Label(
            panel_aksi,
            text=f"Mau ngapain sekarang {self.jenis_kelamin}?",
            bg="#f3f8ff",
            fg="#29353d",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 7))

        tombol_transaksi = tk.Frame(panel_aksi, bg="#f3f8ff")
        tombol_transaksi.pack(fill="x")

        tk.Button(
            tombol_transaksi,
            text="Deposit",
            command=lambda: self.pilih_nominal("Deposit"),
            bg="#20a36a",
            fg="white",
            activebackground="#188655",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=15,
            height=2
        ).pack(side="left", padx=(0, 7))

        tk.Button(
            tombol_transaksi,
            text="Tarik",
            command=lambda: self.pilih_nominal("Tarik"),
            bg="#e4575b",
            fg="white",
            activebackground="#bd4044",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=15,
            height=2
        ).pack(side="left", padx=7)

        tk.Button(
            panel_aksi,
            text="Balik ke halaman pertama",
            command=self.tampilkan_halaman_pertama,
            bg="#ffc857",
            fg="#29353d",
            activebackground="#f0b83f",
            activeforeground="#29353d",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(anchor="e", pady=(12, 0))

        riwayat_frame = tk.LabelFrame(
            konten,
            text=f"Tadi {self.jenis_kelamin} udah ngapain aja:",
            bg="#f3f8ff",
            fg="#29353d",
            font=("Arial", 11, "bold"),
            padx=8,
            pady=8
        )
        riwayat_frame.pack(fill="both", expand=True, pady=(14, 0))

        kolom = ("waktu", "tipe", "nominal", "saldo")
        self.tabel = ttk.Treeview(
            riwayat_frame,
            columns=kolom,
            show="headings",
            height=7
        )

        self.tabel.heading("waktu", text="When ya?")
        self.tabel.heading("tipe", text="Ngapain")
        self.tabel.heading("nominal", text="Berapaan")
        self.tabel.heading("saldo", text="Sisanya tinggal segini loh ya 😂")

        self.tabel.column("waktu", width=170, anchor="w")
        self.tabel.column("tipe", width=110, anchor="w")
        self.tabel.column("nominal", width=150, anchor="w")
        self.tabel.column("saldo", width=250, anchor="w")

        scrollbar = ttk.Scrollbar(
            riwayat_frame,
            orient="vertical",
            command=self.tabel.yview
        )
        self.tabel.configure(yscrollcommand=scrollbar.set)

        self.tabel.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for transaksi in self.transaksi:
            self.tabel.insert(
                "",
                "end",
                values=(
                    transaksi["waktu"],
                    transaksi["tipe"],
                    format_rupiah(transaksi["nominal"]),
                    format_rupiah(transaksi["saldo_setelah"])
                )
            )

    def tampilkan_gambar_atm(self):
        path_gambar = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "atm.png"
        )

        if os.path.isfile(path_gambar):
            try:
                gambar = tk.PhotoImage(file=path_gambar)
                faktor = max(
                    1,
                    (gambar.width() + 299) // 300,
                    (gambar.height() + 209) // 210
                )
                if faktor > 1:
                    gambar = gambar.subsample(faktor, faktor)

                self.gambar_atm = gambar
                tk.Label(
                    self.panel_gambar,
                    image=self.gambar_atm,
                    bg="white"
                ).pack(expand=True)
                return
            except tk.TclError:
                pass

        self.gambar_atm_sederhana()

    def gambar_atm_sederhana(self):
        kanvas = tk.Canvas(
            self.panel_gambar,
            width=300,
            height=210,
            bg="#dff3ff",
            highlightthickness=0
        )
        kanvas.pack(expand=True)

        kanvas.create_rectangle(
            85, 15, 215, 198,
            fill="#aeb8c4",
            outline="#596675",
            width=3
        )
        kanvas.create_rectangle(
            101, 34, 199, 85,
            fill="#91d5f2",
            outline="#34495e",
            width=3
        )
        kanvas.create_text(
            150, 59,
            text="ATM",
            fill="#123d59",
            font=("Arial", 20, "bold")
        )
        kanvas.create_rectangle(
            111, 101, 189, 111,
            fill="#273746",
            outline="#1c2833"
        )

        for y in (126, 142, 158):
            kanvas.create_oval(
                113, y, 122, y + 9,
                fill="#1677b8",
                outline=""
            )
            kanvas.create_line(
                133, y + 4, 185, y + 4,
                fill="#596675",
                width=2
            )

        kanvas.create_rectangle(
            119, 174, 181, 184,
            fill="#273746",
            outline="#1c2833"
        )

    def pilih_nominal(self, jenis):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{jenis.capitalize()} - ATM Kelompok 1 😎")
        dialog.geometry("420x270")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text=f"Mau {jenis} berapa {self.jenis_kelamin}?",
            font=("Arial", 12, "bold")
        ).pack(pady=(18, 12))

        area_tombol = tk.Frame(dialog)
        area_tombol.pack()

        warna = "#20a36a" if jenis == "Deposit" else "#e4575b"

        for i, nominal in enumerate(NOMINAL_PILIHAN):
            tk.Button(
                area_tombol,
                text=format_rupiah(nominal),
                command=lambda n=nominal: self.proses_transaksi(
                    jenis, n, dialog
                ),
                bg=warna,
                fg="white",
                activebackground="#1677b8",
                activeforeground="white",
                font=("Arial", 11, "bold"),
                relief="flat",
                cursor="hand2",
                width=14,
                height=2
            ).grid(
                row=i // 2,
                column=i % 2,
                padx=8,
                pady=8
            )

        tk.Button(
            dialog,
            text="Gajadi ah",
            command=dialog.destroy,
            width=12
        ).pack(pady=(8, 0))

    def proses_transaksi(self, jenis, nominal, dialog):
        if jenis == "Tarik" and nominal > self.saldo:
            messagebox.showerror(
                "Saldo tidak cukup",
                f"Saldo {self.jenis_kelamin} {self.username} "
                f"{format_rupiah(self.saldo)}.\n"
                f"Nominal yang {self.jenis_kelamin} {self.username} pilih {format_rupiah(nominal)}, mana cukup {self.jenis_kelamin} 😭.",
                parent=dialog
            )
            return

        dialog.destroy()

        if jenis == "Deposit":
            self.saldo += nominal
            jenis_riwayat = "Deposit"
            judul_pesan = "Deposit berhasil"
        else:
            self.saldo -= nominal
            jenis_riwayat = "Tarik"
            judul_pesan = "Berhasil ditarik"

        self.label_saldo.config(text=format_rupiah(self.saldo))
        self.tambah_riwayat(jenis_riwayat, nominal)

        messagebox.showinfo(
            judul_pesan,
            f"Saldo sekarang: {format_rupiah(self.saldo)}",
            parent=self.root
        )

    def tambah_riwayat(self, jenis, nominal):
        waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data_transaksi = {
            "tipe": jenis,
            "nominal": nominal,
            "saldo_setelah": self.saldo,
            "waktu": waktu
        }
        self.transaksi.append(data_transaksi)

        self.tabel.insert(
            "",
            "end",
            values=(
                waktu,
                jenis,
                format_rupiah(nominal),
                format_rupiah(self.saldo)
            )
        )

    def keluar(self):
        gender = self.jenis_kelamin or "Mas/Mbak"
        messagebox.showinfo(
            "ATM Kelompok 1 😎",
            f"Makasih {gender}, jangan lupa datang lagi...😭",
            parent=self.root
        )
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankATM(root)
    root.mainloop()
