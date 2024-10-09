import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkcalendar import DateEntry
import pytesseract
from datetime import datetime, timedelta
import webbrowser

'''
    ini versi lama kurang: teks belum rapi pada box dan tanggal belum diprint
'''

def resource_path(relative_path):
    """ Dapatkan path absolut untuk file dalam resource (jika dibundle menggunakan PyInstaller) """
    try:
        base_path = sys._MEIPASS  # pylint: disable=W0212,E1101
    except Exception:
        base_path = os.path.abspath(".")  # untuk jalur file saat development

    return os.path.join(base_path, relative_path)

def draw_text_wrapped_centered(draw, text, position, font, max_width, max_height, fill):
    # Memecah teks menjadi beberapa baris jika melebihi max_width
    lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        # Menggunakan textbbox untuk mengukur lebar teks
        test_line_width = draw.textbbox((0, 0), test_line, font=font)[2]
        if test_line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())  # Tambahkan baris dan hapus spasi ekstra
            current_line = word + " "

    # Menyimpan sisa kata-kata di baris terakhir
    if current_line:
        lines.append(current_line.strip())

    # Hitung tinggi total teks untuk penempatan vertikal
    total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines])

    # Hitung posisi Y untuk menempatkan teks di tengah secara vertikal
    y_start = position[1] + (max_height - total_text_height) // 2

    # Menggambar setiap baris dengan rata tengah (horizontal) dan penempatan vertikal
    y_offset = y_start
    for line in lines:
        line_width = draw.textbbox((0, 0), line, font=font)[2]
        x_position = position[0] + (max_width - line_width) // 2  # Rata tengah horizontal
        draw.text((x_position, y_offset), line, font=font, fill=fill)
        # Menghitung tinggi baris
        line_height = draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
        y_offset += line_height  # Tambahkan jarak antar baris


# Fungsi untuk menambahkan teks di posisi yang sejajar dengan background (centered)
def posisi_center_tgl(draw, text, position_y, font, image_width, fill=(255, 255, 255)):
    # Hitung ukuran teks
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Tentukan posisi X agar teks berada di tengah secara horizontal
    x = (image_width - text_width) // 2
    y = position_y  # Gunakan posisi Y yang diberikan

    # Tambahkan teks di posisi yang sudah dihitung
    draw.text((x, y), text, font=font, fill=fill)
# Ambil lebar gambar (background) agar bisa digunakan untuk center alignment

def diseminasi():
    webbrowser.open('https://app.publer.io/#/posts')

def convert_day_to_indonesian(day_name):
    day_translation = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }
    return day_translation.get(day_name, day_name)

def convert_month_to_indonesian(month_name):
    """Konversi nama bulan bahasa Inggris ke bahasa Indonesia."""
    month_translation = {
        "January": "Januari",
        "February": "Februari",
        "March": "Maret",
        "April": "April",
        "May": "Mei",
        "June": "Juni",
        "July": "Juli",
        "August": "Agustus",
        "September": "September",
        "October": "Oktober",
        "November": "November",
        "December": "Desember"
    }
    return month_translation.get(month_name, month_name)

class Pdce3hMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.root = parent

        # Menambahkan path Tesseract secara manual
        tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

        self.create_widgets()
        self.sections_list = []
        self.date_text = ""
        self.preview_image_ready = False
        
    def get_month_name(self, month_number):
        """Konversi angka bulan menjadi nama bulan dalam bahasa Indonesia"""
        months = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        return months[int(month_number) - 1]

    def get_day_name(self, date):
        """Fungsi untuk mendapatkan nama hari dari suatu tanggal"""
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        return days[date.weekday()]

    def create_widgets(self):
        # Load gambar untuk tombol "Kembali"
        image_path = resource_path("assets//back-button.png")
        image = Image.open(image_path)
        image = image.resize((25, 25), Image.Resampling.LANCZOS)
        back_button_image = ImageTk.PhotoImage(image)

        # Ganti tombol "Kembali" dengan tombol gambar
        back_button = tk.Button(self, image=back_button_image, command=lambda: self.controller.show_frame("HomePageApp"), borderwidth=0)
        back_button.image = back_button_image  # Simpan referensi gambar agar tidak dihapus oleh garbage collector
        back_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        # DateEntry untuk input tanggal
        self.label_date = tk.Label(self, text="Tanggal Mulai :")
        self.label_date.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.date_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Button untuk memilih file gambar
        self.button_select_image = tk.Button(self, text="Select Image File", command=self.open_image_file)
        self.button_select_image.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Button untuk preview hasil print teks di atas gambar
        self.button_preview = tk.Button(self, text="Preview Text on Image", command=self.preview_text_on_image)
        self.button_preview.grid(row=0, column=4, padx=10, pady=5, sticky="e")

        # Frame utama yang menampung frame_sections tanpa scrollbar
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        # Mengatur grid untuk main_frame
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Frame untuk teks
        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ns")

        # Frame untuk gambar yang dipilih dan preview gambar
        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Menambahkan frame untuk menampilkan gambar yang dipilih
        self.selected_image_frame = tk.Frame(self.image_frame)
        self.selected_image_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        self.selected_image_label = tk.Label(self.selected_image_frame)
        self.selected_image_label.pack()

        # Menambahkan frame untuk preview gambar
        self.preview_image_frame = tk.Frame(self.image_frame)
        self.preview_image_frame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

        self.preview_image_label = tk.Label(self.preview_image_frame)
        self.preview_image_label.pack()

    def generate_caption(self):
        """Fungsi untuk membuat caption dengan tanggal yang disesuaikan dari DateEntry"""
        start_date = self.date_entry.get_date()  # Mengambil tanggal dari DateEntry
        end_date = start_date + timedelta(days=2)  # Menambah 2 hari untuk periode 3 harian

        # Dapatkan nama hari dan bulan dalam bahasa Indonesia
        start_day_name = convert_day_to_indonesian(start_date.strftime("%A"))
        end_day_name = convert_day_to_indonesian(end_date.strftime("%A"))

        start_month_name = convert_month_to_indonesian(start_date.strftime("%B"))
        end_month_name = convert_month_to_indonesian(end_date.strftime("%B"))

        # Format tanggal ke dalam format yang diinginkan
        start_date_str = f"{start_day_name}, {start_date.strftime('%d')} {start_month_name} {start_date.strftime('%Y')}"
        end_date_str = f"{end_day_name}, {end_date.strftime('%d')} {end_month_name} {end_date.strftime('%Y')}"

        # Membuat caption dengan tanggal yang sudah disesuaikan
        caption = f"""Selamat Pagi, sobat cuaca!\nBerikut peringatan dini cuaca ekstrem 3 harian ({start_date_str} - {end_date_str}).\nSemoga bermanfaat ya!\n#CuacaKalsel #infoBMKG #InfoKalsel #CuacaKotabaru #KotabaruInfo #BanggaMelayaniBangsa"""
        return caption

    def copy_caption(self):
        """Fungsi untuk menyalin teks caption ke clipboard"""
        caption_text = self.generate_caption()  # Buat caption dengan tanggal yang disesuaikan
        self.root.clipboard_clear()  # Bersihkan clipboard
        self.root.clipboard_append(caption_text)  # Tambahkan teks caption ke clipboard
        messagebox.showinfo("Caption Copied", "Caption berhasil disalin ke clipboard!")

    def open_image_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                # Ekstraksi teks dari gambar menggunakan Tesseract
                image_text = pytesseract.image_to_string(file_path)

                # Memisahkan teks berdasarkan dua garis
                sections = image_text.split("\n\n")  # Memisahkan berdasarkan dua garis atau pemisah lain
                
                # Filter hanya untuk section 3, 5, dan 7
                filtered_sections = [sections[i] for i in [3, 5, 7] if i < len(sections)]

                # Reset sections_list dan bersihkan frame sections
                self.sections_list = []
                for widget in self.text_frame.winfo_children():
                    widget.destroy()

                # Menyusun teks dan menambahkannya ke sections_list
                for section in filtered_sections:
                    text_frame = tk.Frame(self.text_frame)
                    entry = tk.Text(text_frame, height=10, width=30, wrap=tk.WORD)

                    # Memformat teks agar terlihat rata tengah
                    centered_text = self.center_text(section, entry)
                    entry.insert(tk.END, centered_text)
                    entry.tag_configure("center", justify='center')  # Mengatur justify menjadi center
                    entry.tag_add("center", "1.0", "end")  # Menambahkan tag ke teks
                    entry.grid(row=0, column=0, padx=2, pady=5)

                    text_frame.grid(row=len(self.sections_list), column=0, pady=5, sticky="w")

                    self.sections_list.append({
                        "text_widget": entry,
                        "x": 225,  # Set posisi x default
                        "y": 430 + 150 * len(self.sections_list),  # Set posisi y dinamis berdasarkan indeks
                        "font_size": 24,  # Set ukuran font default
                        "font_path": 'D:\\dev\\latsar\\font\\OpenSans-Bold.ttf',  # Set path font default
                        "color": "#441557"  # Set warna default
                    })

                # Menampilkan gambar yang dipilih di frame sebelah kiri (selected_image_frame)
                image = Image.open(file_path)
                image.thumbnail((500, 500))  # Mengubah ukuran gambar
                img_tk = ImageTk.PhotoImage(image)

                self.selected_image_label.config(image=img_tk)
                self.selected_image_label.image = img_tk  # Menyimpan referensi agar gambar tidak dihapus

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def center_text(self, text, text_widget):
        """Mengatur teks menjadi rata tengah dengan menambahkan padding sesuai kebutuhan"""
        lines = text.split('\n')
        centered_lines = []
        for line in lines:
            line_length = len(line)
            widget_width = text_widget.cget("width")
            padding = max((widget_width - line_length) // 2, 0)
            centered_lines.append(' ' * padding + line)
        return '\n'.join(centered_lines)

    def preview_text_on_image(self):
        try:
            # Ambil nilai input tanggal
            self.date_text = self.date_entry.get()

            # Parse date_text into datetime object
            selected_date = datetime.strptime(self.date_text, "%m/%d/%y")
            end_date = selected_date + timedelta(days=2)

            # Format hari dan tanggal dalam bahasa Indonesia
            start_day_name = convert_day_to_indonesian(selected_date.strftime("%A"))
            end_day_name = convert_day_to_indonesian(end_date.strftime("%A"))
            start_date_str = f"{start_day_name}, {selected_date.strftime('%d')} {convert_month_to_indonesian(selected_date.strftime('%B'))} {selected_date.strftime('%Y')}"
            end_date_str = f"{end_day_name}, {end_date.strftime('%d')} {convert_month_to_indonesian(end_date.strftime('%B'))} {end_date.strftime('%Y')}"

            # Buat teks untuk ditampilkan
            date_range_text = f"{start_date_str} - {end_date_str}"

            # Membuka gambar background
            background_path = 'D:\\dev\\latsar\\assets\\bg_pdce3h.png'
            self.background_image = Image.open(background_path)  # Simpan background asli untuk penyimpanan nanti
            draw = ImageDraw.Draw(self.background_image)

            # Menambahkan teks tanggal awal - akhir di bagian tengah atas gambar
            font_path = 'D:\\dev\\latsar\\font\\Anton.ttf'
            font = ImageFont.truetype(font_path, 24)  # Ukuran font disesuaikan
            image_width = self.background_image.width
            y_position = 250  # Sesuaikan posisi y di mana teks akan diletakkan

            # Gambar teks di posisi tengah
            posisi_center_tgl(draw, date_range_text, y_position, font, image_width, fill=(255, 255, 255))

            # Membuat format tanggal 'bulan \n tanggal' dengan dua digit untuk tanggal
            month_name = self.get_month_name(selected_date.month)
            dates = [(selected_date + timedelta(days=i)).strftime(f"%d\n{month_name}") for i in range(3)]

            # Menyimpan tanggal hari ini, besok, dan lusa
            dates = [selected_date, selected_date + timedelta(days=1), selected_date + timedelta(days=2)]

            # Menyimpan perubahan teks dari GUI ke sections_list dan menambahkan teks ke gambar
            coordinates = [(200, 450), (200, 595), (200, 735)]  # Koordinat untuk setiap kalimat
            
            for index, section in enumerate(self.sections_list[:3]):  # Maksimal 3 section
                edited_text = section["text_widget"].get("1.0", tk.END).strip()  # Ambil teks yang diedit
                section["text"] = edited_text

                font_size = section.get("font_size", 32)
                font_path = section.get("font_path", 'font/OpenSans-Bold.ttf')
                font = ImageFont.truetype(font_path, font_size)

                # Ambil posisi yang sesuai
                position = coordinates[index]

                # Panggil fungsi untuk menggambar teks di posisi yang sesuai
                draw_text_wrapped_centered(
                    draw, 
                    section["text"], 
                    position, 
                    font, 
                    max_width=800,  # Lebar maksimal
                    max_height=65,  # Tinggi maksimal area teks
                    fill="#441557"  # Warna teks
                )
            
            # Tambahkan teks bulan dan tanggal ke gambar dengan center align
            if self.date_text:
                # Font untuk bulan
                font_path_month = resource_path("font//Anteb-ExtraBold.ttf")
                font_month = ImageFont.truetype(font_path_month, 24)
                # Font untuk tanggal
                font_path_day = resource_path("font//Anteb-ExtraBold.ttf")
                font_day = ImageFont.truetype(font_path_day, 48)
                
                for i, selected_date in enumerate(dates):
                    month_name = self.get_month_name(selected_date.strftime('%m'))
                    formatted_month = month_name
                    formatted_day = selected_date.strftime('%d')

                    # Hitung lebar teks bulan dan tanggal
                    month_bbox = draw.textbbox((0, 0), formatted_month, font=font_month)
                    day_bbox = draw.textbbox((0, 0), formatted_day, font=font_day)
                    month_width = month_bbox[2] - month_bbox[0]
                    day_width = day_bbox[2] - day_bbox[0]

                    # Hitung posisi x untuk center align
                    image_width = self.background_image.width
                    month_x = (253 - month_width) // 2
                    day_x = (250 - day_width) // 2

                    draw.text((month_x, 445 + (i * 145)), formatted_month, font=font_month, fill="#FFFFFF")
                    draw.text((day_x, 490 + (i * 145)), formatted_day, font=font_day, fill="#441557")

            # Menampilkan preview gambar di sebelah kanan (preview_image_frame)
            self.show_image(self.background_image.copy())  # Tampilkan salinan background untuk pratinjau

            # Tombol untuk menyimpan dan posting
            save_and_post_button = ttk.Button(self.image_frame, text="Simpan Ke Komputer", command=self.save_image)
            save_and_post_button.grid(row=2, column=0, padx=10, pady=20, sticky="sw")

            diseminasi_page_button = ttk.Button(self.image_frame, text="Diseminasi Ke Sosial Media", command=diseminasi)
            diseminasi_page_button.grid(row=2, column=1, padx=10, pady=20, sticky="sw")

            # Tombol untuk menyalin caption ke clipboard
            self.copy_caption_button = tk.Button(self.image_frame, text="Copy Caption", command=self.copy_caption)
            self.copy_caption_button.grid(row=4, column=0, padx=10, pady=5, sticky="sw")

            # Membuat caption dan menampilkan di GUI
            caption_text = self.generate_caption()
            caption_label = tk.Label(self.image_frame, text=caption_text, wraplength=800, justify="left", font=("Arial", 10), bg="white")
            caption_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def save_image(self):
        try:
            # Cek apakah gambar preview sudah siap
            if not self.preview_image_ready:
                raise Exception("Preview image not ready")

            # Ambil tanggal awal dan akhir
            selected_date = datetime.strptime(self.date_text, "%m/%d/%y")
            end_date = selected_date + timedelta(days=2)

            # Membuat struktur direktori berdasarkan tahun dan bulan
            year = selected_date.strftime("%Y")
            month = selected_date.strftime("%m")
            day_start = selected_date.strftime("%d")
            day_end = end_date.strftime("%d")
            file_name = f"{day_start}-{day_end}.png"

            # Path folder sesuai format 'Infografis > PD 3 Harian > tahun > bulan'
            folder_path = os.path.join("Infografis", "PD 3 Harian", year, month)
            os.makedirs(folder_path, exist_ok=True)  # Membuat folder jika belum ada

            # Path file lengkap
            file_path = os.path.join(folder_path, file_name)

            # Menyimpan background asli dengan teks yang ditambahkan
            self.background_image.save(file_path)
            messagebox.showinfo("Info", f"Image saved as {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the image: {str(e)}")

    def show_image(self, image):
        """Tampilkan pratinjau gambar yang dihasilkan di preview_image_frame."""
        image.thumbnail((500, 500))  # Resize gambar
        img_tk = ImageTk.PhotoImage(image)

        self.preview_image_label.config(image=img_tk)
        self.preview_image_label.image = img_tk  # Simpan referensi agar gambar tidak dihapus
        self.preview_image_ready = True  # Tandai bahwa gambar pratinjau sudah siap

if __name__ == "__main__":
    root = tk.Tk()
    app = Pdce3hMenu(root, None)
    root.mainloop()