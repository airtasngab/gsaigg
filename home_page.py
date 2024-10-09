import sys
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import webbrowser

def resource_path(relative_path):
    """ Dapatkan path absolut untuk file dalam resource (jika dibundle menggunakan PyInstaller) """
    try:
        base_path = sys._MEIPASS  # pylint: disable=W0212,E1101
    except Exception:
        base_path = os.path.abspath(".")  # untuk jalur file saat development

    return os.path.join(base_path, relative_path)

def panduan():
    webbrowser.open('https://drive.google.com/file/d/1RkzD_JL4eIxGnjvMiOQo7cMeU-l7LiSt/view?usp=sharing')

class HomePageApp(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_homepage()

    def create_rounded_button(self, text, command, width=150, height=50, corner_radius=20, shadow_offset=5, bg="#2C2C2C", fg="white"):
        """Fungsi untuk membuat tombol dengan sudut lengkung dan efek shadow"""
        total_width = width + shadow_offset
        total_height = height + shadow_offset

        # Buat kanvas untuk gambar tombol dengan shadow offset
        image = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Warna shadow (transparan hitam)
        shadow_color = (0, 0, 0, 100)

        # Menggambar bayangan dengan sudut melengkung
        draw.rounded_rectangle((shadow_offset, shadow_offset, width + shadow_offset, height + shadow_offset), corner_radius, fill=shadow_color)

        # Membuat blur pada bayangan agar tampak lebih lembut
        image = image.filter(ImageFilter.GaussianBlur(3))

        # Warna latar tombol
        fill_color = bg

        # Menggambar tombol di atas bayangan
        draw = ImageDraw.Draw(image)  # Menggambar ulang setelah efek blur
        draw.rounded_rectangle((0, 0, width, height), corner_radius, fill=fill_color)

        # Konversi gambar untuk digunakan di tkinter
        button_image = ImageTk.PhotoImage(image)

        # Membuat label sebagai tombol
        button = tk.Label(self, image=button_image, text=text, compound="center", fg=fg, font=("Helvetica", 12))
        button.image = button_image  # Referensi agar tidak dihapus oleh garbage collector

        # Bind untuk klik tombol
        button.bind("<Button-1>", lambda e: command())

        return button

    def create_homepage(self):
        # Memuat logo
        logo_path = resource_path("assets//logo.png")  # Sesuaikan dengan lokasi file logo Anda
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)  # Mengubah ukuran logo jika diperlukan
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Header dengan logo dan teks
        header_frame = tk.Frame(self, bg="#2C2C2C")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 125))

        # Label untuk logo
        logo_label = tk.Label(header_frame, image=logo_photo, bg="#2C2C2C")
        logo_label.image = logo_photo  # Menyimpan referensi agar tidak dihapus oleh garbage collector
        logo_label.pack(side="left", padx=(30, 20), pady=(10, 10))

        # Label untuk teks
        header_label = tk.Label(header_frame, text="INFO GRAFIS GENERATOR\nSTAMET GSA", font=("Helvetica", 16, "bold"), bg="#2C2C2C", fg="white")
        header_label.pack(side="top", padx=(30, 20), pady=(10, 10))

        # Load gambar untuk tombol "Kembali"
        image_path_guide = resource_path("assets//guide.png")
        image = Image.open(image_path_guide)
        image = image.resize((25, 25), Image.Resampling.LANCZOS)
        guide_button_image = ImageTk.PhotoImage(image)

        # Ganti tombol "guide" dengan tombol gambar
        guide_button = tk.Button(self, image=guide_button_image, command=panduan)
        guide_button.image = guide_button_image  # Simpan referensi gambar agar tidak dihapus oleh garbage collector
        guide_button.grid(row=0, column=1, padx=50, pady=20, sticky=tk.E)

        # Tombol-tombol dengan sudut melengkung dan bayangan
        wxrev_button = self.create_rounded_button("Rangkuman Cuaca Kemarin", lambda: self.controller.show_frame("WxrevMenu"), 300, 80)
        wxrev_button.grid(row=1, column=0, padx=20, pady=50)

        prakgel_button = self.create_rounded_button("Prakiraan Gelombang", lambda: self.controller.show_frame("PrakgelMenu"), 300, 80)
        prakgel_button.grid(row=1, column=1, padx=20, pady=50)

        cuaca_ekstrem_button = self.create_rounded_button("Peringatan Dini Cuaca Ekstrem", lambda: self.controller.show_frame("Pdce3hMenu"), 300, 80)
        cuaca_ekstrem_button.grid(row=2, column=0, padx=20, pady=50)

        button_404 = self.create_rounded_button("404", lambda: self.controller.show_frame("PageNotFound"), 300, 80)
        button_404.grid(row=2, column=1, padx=20, pady=50)

        # Mengatur grid agar lebih fleksibel
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

# MainApp tetap sama, tinggal menjalankan HomePageApp
if __name__ == "__main__":
    app = tk.Tk()
    frame = HomePageApp(app, None)
    frame.pack(fill="both", expand=True)
    app.mainloop()
