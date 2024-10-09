import sys
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def resource_path(relative_path):
    """ Dapatkan path absolut untuk file dalam resource (jika dibundle menggunakan PyInstaller) """
    try:
        base_path = sys._MEIPASS  # pylint: disable=W0212,E1101
    except Exception:
        base_path = os.path.abspath(".")  # untuk jalur file saat development

    return os.path.join(base_path, relative_path)
class PageNotFound(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.root = parent

        # Membuat Canvas untuk menggambar teks "404"
        self.canvas = tk.Canvas(self, width=1400, height=750)
        self.canvas.grid(row=0, column=0, padx=5, pady=5)

        # Dapatkan ukuran canvas
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        # Menggambar teks "404" di latar belakang, tepat di tengah
        self.canvas.create_text(canvas_width / 2, canvas_height / 2, text="404", font=("Helvetica", 150, "bold"), fill="lightgray", anchor="center")

        # Load gambar untuk tombol "Kembali"
        image_path_kembali = resource_path("assets//back-button.png")
        image = Image.open(image_path_kembali)
        image = image.resize((25, 25), Image.Resampling.LANCZOS)
        back_button_image = ImageTk.PhotoImage(image)

        # Ganti tombol "Kembali" dengan tombol gambar
        back_button = tk.Button(self, image=back_button_image, command=lambda: self.controller.show_frame("HomePageApp"), borderwidth=0)
        back_button.image = back_button_image  # Simpan referensi gambar agar tidak dihapus oleh garbage collector
        back_button_window = self.canvas.create_window(10, 10, anchor="nw", window=back_button)

if __name__ == "__main__":
    root = tk.Tk()
    app = PageNotFound(root, None)
    app.pack(expand=True, fill="both")
    root.mainloop()
