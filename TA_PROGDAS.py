import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar


class Buku:
    def __init__(self, judul, penulis):
        self.judul = judul
        self.penulis = penulis
        self.dipinjam = False


class Perpustakaan:
    def __init__(self):
        self.buku_list = []

    def tambah_buku(self, judul, penulis):
        if not any(buku.judul.lower() == judul.lower() and buku.penulis.lower() == penulis.lower() for buku in self.buku_list):
            self.buku_list.append(Buku(judul, penulis))
            return True
        return False

    def pinjam_buku(self, judul, penulis):
        if self.hitung_buku_dipinjam() >= 4:
            return "limit"
        for buku in self.buku_list:
            if buku.judul.lower() == judul.lower() and buku.penulis.lower() == penulis.lower() and not buku.dipinjam:
                buku.dipinjam = True
                return True
        return False

    def kembalikan_buku(self, judul, penulis):
        for buku in self.buku_list:
            if buku.judul.lower() == judul.lower() and buku.penulis.lower() == penulis.lower() and buku.dipinjam:
                buku.dipinjam = False
                return True
        return False

    def cari_buku(self, query=None):
        if query:
            return [buku for buku in self.buku_list if query.lower() in buku.judul.lower()]
        return self.buku_list

    def hitung_buku_dipinjam(self):
        return sum(1 for buku in self.buku_list if buku.dipinjam)


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class AplikasiPerpustakaan:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Perpustakaan")
        self.root.geometry("600x400")
        self.perpustakaan = Perpustakaan()
        self.users = []  # List untuk menyimpan pengguna yang terdaftar
        self.current_user = None  # Menyimpan pengguna yang sedang login

        self.frame_login = tk.Frame(self.root, padx=10, pady=10)
        self.frame_signup = tk.Frame(self.root, padx=10, pady=10)
        self.frame_utama = tk.Frame(self.root, padx=10, pady=10)
        self.frame_pencarian = tk.Frame(self.root, padx=10, pady=10)

        self.setup_login_frame()
        self.setup_signup_frame()
        self.setup_main_frame()
        self.setup_search_frame()

        self.frame_login.pack(pady=20)

    def setup_login_frame(self):
        tk.Label(self.frame_login, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.entri_username_login = tk.Entry(self.frame_login)
        self.entri_username_login.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_login, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.entri_password_login = tk.Entry(self.frame_login, show="*")
        self.entri_password_login.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.frame_login, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(self.frame_login, text="Sign Up", command=self.show_signup_frame).grid(row=3, column=0, columnspan=2, pady=5)

    def setup_signup_frame(self):
        tk.Label(self.frame_signup, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.entri_username_signup = tk.Entry(self.frame_signup)
        self.entri_username_signup.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_signup, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.entri_password_signup = tk.Entry(self.frame_signup, show="*")
        self.entri_password_signup.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.frame_signup, text="Sign Up", command=self.signup).grid(row=2, column=0, columnspan=2)
        tk.Button(self.frame_signup, text="Kembali", command=self.show_login_frame).grid(row=3, column=0, columnspan=2, pady=5)

    def setup_main_frame(self):
        self.label_judul = tk.Label(self.frame_utama, text="Judul Buku:")
        self.label_judul.grid(row=0, column=0, padx=5, pady=5)
        self.entri_judul = tk.Entry(self.frame_utama, width=30)
        self.entri_judul.grid(row=0, column=1, padx=5, pady=5)

        self.label_penulis = tk.Label(self.frame_utama, text="Penulis Buku:")
        self.label_penulis.grid(row=1, column=0, padx=5, pady=5)
        self.entri_penulis = tk.Entry(self.frame_utama, width=30)
        self.entri_penulis.grid(row=1, column=1, padx=5, pady=5)

        self.tombol_tambah = tk.Button(self.frame_utama, text="Tambah Buku", command=self.tambah_buku)
        self.tombol_tambah.grid(row=2, column=0, columnspan=2, pady=5)

        self.tombol_pinjam = tk.Button(self.frame_utama, text="Pinjam Buku", command=self.pinjam_buku)
        self.tombol_pinjam.grid(row=3, column=0, columnspan=2, pady=5)

        self.tombol_kembali = tk.Button(self.frame_utama, text="Kembalikan Buku", command=self.kembalikan_buku)
        self.tombol_kembali.grid(row=4, column=0, columnspan=2, pady=5)

        self.tombol_cari = tk.Button(self.frame_utama, text="Cari Buku", command=self.tampilkan_pencarian)
        self.tombol_cari.grid(row=5, column=0, columnspan=2, pady=5)

        self.label_jumlah_dipinjam = tk.Label(self.frame_utama, text="0/4 buku untuk dipinjam")
        self.label_jumlah_dipinjam.grid(row=6, column=0, columnspan=2, pady=5)

    def setup_search_frame(self):
        label_pencarian = tk.Label(self.frame_pencarian, text="Masukkan judul buku yang dicari:")
        label_pencarian.pack(pady=10)

        self.entri_pencarian = tk.Entry(self.frame_pencarian, width=40)
        self.entri_pencarian.pack(pady=5)

        self.tombol_cari_pencarian = tk.Button(self.frame_pencarian, text="Cari", command=self.lakukan_pencarian)
        self.tombol_cari_pencarian.pack(pady=5)

        self.listbox_hasil = Listbox(self.frame_pencarian, width=50, height=10)
        self.listbox_hasil.pack(pady=10)

        self.scrollbar = Scrollbar(self.frame_pencarian)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_hasil.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox_hasil.yview)

        self.tombol_pinjam_pencarian = tk.Button(self.frame_pencarian, text="Pinjam Buku", command=self.pinjam_dari_pencarian)
        self.tombol_pinjam_pencarian.pack(pady=5)

        self.tombol_kembali = tk.Button(self.frame_pencarian, text="Kembali", command=self.tampilkan_utama)
        self.tombol_kembali.pack(pady=5)

    def show_login_frame(self):
        self.frame_signup.pack_forget()
        self.frame_login.pack(pady=20)

    def show_signup_frame(self):
        self.frame_login.pack_forget()
        self.frame_signup.pack(pady=20)

    def login(self):
        username = self.entri_username_login.get()
        password = self.entri_password_login.get()
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                messagebox.showinfo("Info", "Login berhasil!")
                self.frame_login.pack_forget()
                self.frame_utama.pack(pady=20)
                return
        messagebox.showwarning("Peringatan", "Username atau password salah!")

    def signup(self):
        username = self.entri_username_signup.get()
        password = self.entri_password_signup.get()
        if username and password:
            if any(user.username == username for user in self.users):
                messagebox.showwarning("Peringatan", "Username sudah terdaftar!")
            else:
                self.users.append(User(username, password))
                messagebox.showinfo("Info", "Registrasi berhasil!")
                self.entri_username_signup.delete(0, tk.END)
                self.entri_password_signup.delete(0, tk.END)
                self.show_login_frame()
        else:
            messagebox.showwarning("Peringatan", "Username dan Password harus diisi!")

    def tambah_buku(self):
        judul = self.entri_judul.get()
        penulis = self.entri_penulis.get()
        if judul and penulis:
            if self.perpustakaan.tambah_buku(judul, penulis):
                messagebox.showinfo("Info", "Buku berhasil ditambahkan!")
                self.entri_judul.delete(0, tk.END)
                self.entri_penulis.delete(0, tk.END)
            else:
                messagebox.showwarning("Peringatan", "Buku sudah ada!")
        else:
            messagebox.showwarning("Peringatan", "Judul dan Penulis harus diisi!")

    def pinjam_buku(self):
        judul = self.entri_judul.get()
        penulis = self.entri_penulis.get()
        if judul and penulis:
            hasil = self.perpustakaan.pinjam_buku(judul, penulis)
            if hasil == "limit":
                messagebox.showwarning("Peringatan", "Anda hanya dapat meminjam maksimal 4 buku!")
            elif hasil:
                messagebox.showinfo("Info", "Buku berhasil dipinjam!")
                self.perbarui_jumlah_dipinjam()
                self.entri_judul.delete(0, tk.END)
                self.entri_penulis.delete(0, tk.END)
            else:
                messagebox.showwarning("Peringatan", "Buku tidak tersedia!")
        else:
            messagebox.showwarning("Peringatan", "Judul dan Penulis harus diisi!")

    def kembalikan_buku(self):
        judul = self.entri_judul.get()
        penulis = self.entri_penulis.get()
        if judul and penulis:
            if self.perpustakaan.kembalikan_buku(judul, penulis):
                messagebox.showinfo("Info", "Buku berhasil dikembalikan!")
                self.perbarui_jumlah_dipinjam()
                self.entri_judul.delete(0, tk.END)
                self.entri_penulis.delete(0, tk.END)
            else:
                messagebox.showwarning("Peringatan", "Buku tidak ditemukan atau belum dipinjam!")
        else:
            messagebox.showwarning("Peringatan", "Judul dan Penulis harus diisi!")

    def lakukan_pencarian(self):
        query = self.entri_pencarian.get()
        self.listbox_hasil.delete(0, tk.END)
        hasil = self.perpustakaan.cari_buku(query)
        if hasil:
            for buku in hasil:
                status = "Dipinjam" if buku.dipinjam else "Tersedia"
                self.listbox_hasil.insert(tk.END, f"{buku.judul} - {buku.penulis} ({status})")
        else:
            self.listbox_hasil.insert(tk.END, "Tidak ada buku yang ditemukan!")

    def pinjam_dari_pencarian(self):
        selected = self.listbox_hasil.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu!")
            return
        data = self.listbox_hasil.get(selected[0])
        judul, info = data.split(" - ", 1)
        penulis = info.split(" (")[0]
        hasil = self.perpustakaan.pinjam_buku(judul, penulis)
        if hasil == "limit":
            messagebox.showwarning("Peringatan", "Anda hanya dapat meminjam maksimal 4 buku!")
        elif hasil:
            messagebox.showinfo("Info", "Buku berhasil dipinjam!")
            self.lakukan_pencarian()
            self.perbarui_jumlah_dipinjam()
        else:
            messagebox.showwarning("Peringatan", "Buku tidak tersedia atau sudah dipinjam!")

    def perbarui_jumlah_dipinjam(self):
        jumlah_dipinjam = self.perpustakaan.hitung_buku_dipinjam()
        self.label_jumlah_dipinjam.config(text=f"{jumlah_dipinjam}/4 buku untuk dipinjam")

    def tampilkan_utama(self):
        self.frame_pencarian.pack_forget()
        self.frame_utama.pack(pady=20)

    def tampilkan_pencarian(self):
        self.frame_utama.pack_forget()
        self.lakukan_pencarian()
        self.frame_pencarian.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiPerpustakaan(root)
    root.mainloop()
    