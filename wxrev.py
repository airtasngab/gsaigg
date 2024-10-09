import sys
import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import locale
from PIL import Image, ImageDraw, ImageFont, ImageTk
from PIL import Image
from tkinter import messagebox
import webbrowser

locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
def resource_path(relative_path):
    """ Dapatkan path absolut untuk file dalam resource (jika dibundle menggunakan PyInstaller) """
    try:
        base_path = sys._MEIPASS  # pylint: disable=W0212,E1101
    except Exception:
        base_path = os.path.abspath(".")  # untuk jalur file saat development

    return os.path.join(base_path, relative_path)
def open_publer():
    webbrowser.open('https://app.publer.io/#/posts')

class WxrevMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  
        self.controller = controller
        self.parent = parent
        self.grid(sticky="nsew")

        self.selected_date = None
        
        self.temperature_info = ""
        self.pressure_info = ""
        self.humidity_info = ""
        self.wind_info = ""
        
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_input_widgets()
        
        self.data_frame = None  # Initialize data_frame as None
        self.preview_frame = None  # Initialize preview_frame as None
        
        # Load gambar untuk tombol "Kembali"
        image_path_kembali = resource_path("assets//back-button.png")
        image = Image.open(image_path_kembali)
        
        image = image.resize((25, 25), Image.Resampling.LANCZOS)
        back_button_image = ImageTk.PhotoImage(image)

        # Ganti tombol "Kembali" dengan tombol gambar
        back_button = tk.Button(self.scrollable_frame, image=back_button_image, command=lambda: self.controller.show_frame("HomePageApp"), borderwidth=0)
        back_button.image = back_button_image  # Simpan referensi gambar agar tidak dihapus oleh garbage collector
        back_button.grid(row=0, column=0, padx=5, pady=20, sticky=tk.W)

    def create_input_widgets(self):   
        # Label WXREV Code
        ttk.Label(self.scrollable_frame, text="WXREV Code :").grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        self.wxrev_entry = ttk.Entry(self.scrollable_frame, width=70)
        self.wxrev_entry.grid(row=0, column=2, pady=5, sticky=(tk.W, tk.E))

        # Label Tanggal
        ttk.Label(self.scrollable_frame, text="Tanggal :").grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        self.date_entry = DateEntry(self.scrollable_frame, width=27, background='darkblue',
                                    foreground='white', borderwidth=2, year=2024)
        self.date_entry.grid(row=1, column=2, pady=5, sticky=(tk.W, tk.E))

        # Label Cuaca
        ttk.Label(self.scrollable_frame, text="Cuaca :").grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        self.weather_var = tk.StringVar()
        self.weather_combobox = ttk.Combobox(self.scrollable_frame, textvariable=self.weather_var, width=28)
        self.weather_combobox['values'] = (
            "Cerah", "Cerah Berawan", "Berawan", "Berawan Tebal", "Hujan Ringan",
            "Hujan Sedang", "Hujan Lebat", "Hujan Lokal", "Hujan Petir", "Kabut", "Asap")
        self.weather_combobox.grid(row=2, column=2, pady=5, sticky=(tk.W, tk.E))

        # Tombol Generate
        generate_button = ttk.Button(self.scrollable_frame, text="Generate", command=self.generate)
        generate_button.grid(row=2, column=3,  padx=10, sticky=tk.W)
        
        # Tambahkan weight agar kolom kedua memiliki keleluasaan lebar
        self.scrollable_frame.columnconfigure(2, weight=1)

    def generate(self):
        wxrev_code = self.wxrev_entry.get()
        tanggal = self.date_entry.get()
        cuaca = self.weather_var.get()
        
        date_obj = datetime.strptime(tanggal, '%m/%d/%y')
        self.selected_date = date_obj.strftime('%A, %d %B %Y')
        formatted_date = self.selected_date
        
        temperature_info, pressure_info, humidity_info, wind_info = self.translate_wxrev_code(wxrev_code)
        
        self.show_data_entry(wxrev_code, formatted_date, cuaca, temperature_info, pressure_info, humidity_info, wind_info)
        self.preview_image(wxrev_code, formatted_date, cuaca)

    def show_data_entry(self, wxrev_code, formatted_date, cuaca, temperature_info, pressure_info, humidity_info, wind_info):
        if self.data_frame:
            self.data_frame.destroy()  # Hapus frame data lama jika ada
        
        self.data_frame = ttk.Frame(self.scrollable_frame, padding="10 10 10 10")
        self.data_frame.grid(row=4, column=0, columnspan=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.scrollable_frame.rowconfigure(4, weight=1)

        # Gunakan font spesifik
        date_font = ("Anton", 12)
        weather_font = ("Agrandir", 12)
        data_font = ("Open Sans", 12)

        ttk.Label(self.data_frame, text=f"Tanggal: {formatted_date}", font=date_font).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(self.data_frame, text=f"Cuaca: {cuaca}", font=weather_font).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(self.data_frame, text=f"Temperature: {temperature_info}", font=data_font).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(self.data_frame, text=f"Pressure: {pressure_info}", font=data_font).grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Label(self.data_frame, text=f"Humidity: {humidity_info}", font=data_font).grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Label(self.data_frame, text=f"Wind: {wind_info}", font=data_font).grid(row=5, column=0, sticky=tk.W, pady=5)

    def preview_image(self, wxrev_code, formatted_date, cuaca):
        if self.preview_frame:
            self.preview_frame.destroy()  # Hapus frame preview lama jika ada
        if self.data_frame:
            self.data_frame.destroy()  # Hapus frame data entry
        
        self.preview_frame = ttk.Frame(self.scrollable_frame, padding="10 10 10 10")
        self.preview_frame.grid(row=4, column=2, columnspan=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        wxrev_bg_path = resource_path("assets//bg_wxrev.png")
        # Menggunakan resource_path untuk mendapatkan path ke gambar
        cuaca_wxrev_path = resource_path(os.path.join("assets", f"{cuaca.lower().replace(' ', '_')}.png"))

        
        try:
            background = Image.open(wxrev_bg_path)
            background = background.resize((1080, 1080))  # Resize to 1080x1080 pixels for final image
        except IOError:
            print("Tidak dapat membuka gambar latar belakang")
            return
        
        try:
            cuaca_image = Image.open(cuaca_wxrev_path)
            # cuaca_image = cuaca_image.resize((200, 200))  # Resize cuaca image
        except IOError:
            print("Tidak dapat membuka gambar cuaca")
            return
        
        # Calculate the coordinates to center the cuaca image on the background
        background_width, background_height = background.size
        cuaca_image_width, cuaca_image_height = cuaca_image.size
        x = (background_width - cuaca_image_width) // 2
        y = (background_height - cuaca_image_height) // 2 - 140

        # Paste cuaca image on the background
        background.paste(cuaca_image, (x, y), cuaca_image)
        
        draw = ImageDraw.Draw(background)
        
        font_size = 36  # Adjusted font size for 1080x1080 image

        # Menggunakan resource_path untuk mendapatkan path ke font
        date_font_path = resource_path("font/Anton-Regular.ttf")
        weather_font_path = resource_path("font/Agrandir-GrandHeavy.otf")
        data_font_path = resource_path("font/OpenSans-Bold.ttf")

        # Inisialisasi variabel font
        date_font = ImageFont.load_default()
        weather_font = ImageFont.load_default()
        data_font = ImageFont.load_default()

        # Coba memuat font dengan cara yang lebih aman
        try:
            date_font = ImageFont.truetype(date_font_path, font_size)
        except IOError:
            print(f"Warning: Unable to load date font from {date_font_path}, using default font.")

        try:
            weather_font = ImageFont.truetype(weather_font_path, 48)
        except IOError:
            print(f"Warning: Unable to load weather font from {weather_font_path}, using default font.")

        try:
            data_font = ImageFont.truetype(data_font_path, 28)
        except IOError:
            print(f"Warning: Unable to load data font from {data_font_path}, using default font.")



        
        text_date = f"{formatted_date}"
        text_cuaca = f"{cuaca}"
        text_temperature_info = f"{self.temperature_info}"
        text_pressure_info = f"{self.pressure_info}"
        text_humidity_info = f"{self.humidity_info}"
        text_wind_info = f"{self.wind_info}"

        # Set the y positions for temperature and pressure
        y_position_temperature = 716
        y_position_pressure = 910
        y_position_humidity = 716
        y_position_wind = 910

        # Calculate positions to center text
        image_width = background.width
        text_bbox_date = draw.textbbox((0, 0), text_date, font=date_font)
        text_bbox_cuaca = draw.textbbox((0, 0), text_cuaca, font=weather_font)

        text_width_date = text_bbox_date[2] - text_bbox_date[0]
        text_width_cuaca = text_bbox_cuaca[2] - text_bbox_cuaca[0]

        posisi_date = ((image_width - text_width_date) / 2, 206)
        posisi_cuaca = ((image_width - text_width_cuaca) / 2, 540)

        # Calculate the bounding boxes for the text
        text_bbox_temperature = draw.textbbox((0, 0), text_temperature_info, font=data_font)
        text_bbox_pressure = draw.textbbox((0, 0), text_pressure_info, font=data_font)
        text_bbox_humidity = draw.textbbox((0, 0), text_humidity_info, font=data_font)
        text_bbox_wind = draw.textbbox((0, 0), text_wind_info, font=data_font)

        # Calculate the width of each text
        text_width_temperature = text_bbox_temperature[2] - text_bbox_temperature[0]
        text_width_pressure = text_bbox_pressure[2] - text_bbox_pressure[0]
        text_width_humidity = text_bbox_humidity[2] - text_bbox_humidity[0]
        text_width_wind = text_bbox_wind[2] - text_bbox_wind[0]

        # Calculate the x positions to center the text on the desired x-axis
        x_position_temperature = 347 - text_width_temperature / 2
        x_position_pressure = 350 - text_width_pressure / 2
        x_position_humidity = 885 - text_width_humidity / 2
        x_position_wind = 880 - text_width_wind / 2

        # Set the positions with y-coordinates
        posisi_temperature_info = (x_position_temperature, y_position_temperature)
        posisi_pressure_info = (x_position_pressure, y_position_pressure)
        posisi_humidity_info = (x_position_humidity, y_position_humidity)
        posisi_wind_info = (x_position_wind, y_position_wind)

        # Draw the text on the image
        draw.text(posisi_date, text_date, fill='white', font=date_font)
        draw.text(posisi_cuaca, text_cuaca, fill='white', font=weather_font)
        draw.text(posisi_temperature_info, text_temperature_info, fill='white', font=data_font)
        draw.text(posisi_pressure_info, text_pressure_info, fill='white', font=data_font)
        draw.text(posisi_humidity_info, text_humidity_info, fill='white', font=data_font)
        draw.text(posisi_wind_info, text_wind_info, fill='white', font=data_font)

        # Draw the text with white font color for temperature and humidity
        draw.text((x_position_temperature, y_position_temperature), text_temperature_info, fill='white', font=data_font)
        draw.text((x_position_pressure, y_position_pressure), text_pressure_info, fill='black', font=data_font)
        draw.text((x_position_humidity, y_position_humidity), text_humidity_info, fill='white', font=data_font)
        draw.text((x_position_wind, y_position_wind), text_wind_info, fill='black', font=data_font)

        # Draw date and weather text
        draw.text(posisi_date, text_date, fill='black', font=date_font)
        draw.text(posisi_cuaca, text_cuaca, fill='black', font=weather_font)

        # Save the image with a structured directory format
        date_for_filename = datetime.strptime(formatted_date, '%A, %d %B %Y').strftime('%Y/%m/%d')
        year, month, day = date_for_filename.split('/')
        save_dir = os.path.join(".","Infografis", "WXREV", year, month)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{day}.png")


        # Setelah membuat background image di dalam preview_image
        self.background = background  # Simpan sebagai atribut instance

        # Simpan gambar
        self.save_path = save_path  # Simpan path untuk digunakan saat menekan tombol simpan
        
        # Create a 400x400 preview image
        preview_image = background.resize((500, 500))
        preview_image_tk = ImageTk.PhotoImage(preview_image)
        image_label = tk.Label(self.preview_frame, image=preview_image_tk)
        image_label.image = preview_image_tk  # Simpan referensi gambar
        
        image_label.grid(row=0, column=0, padx=5, pady=5)

        caption_text = (
            f"Selamat pagi, sobat cuaca!\n"
            f"Berikut kami sampaikan ringkasan keadaan cuaca kemarin di wilayah Kabupaten Kotabaru dan sekitarnya pada {formatted_date}\n"
            f"Semoga bermanfaat!\n\n"
            f"#CuacaKalsel #infoBMKG #InfoKalsel #CuacaKotabaru #KotabaruInfo #BanggaMelayaniBangsa"
        )

        caption_label = tk.Label(self.preview_frame, text=caption_text, font=32, justify=tk.LEFT, wraplength=300)
        caption_label.grid(row=0, column=1, columnspan=4, padx=10, pady=10)
        
        # Tambahkan tombol copy
        copy_button = ttk.Button(self.preview_frame, text="Copy Caption", command=lambda: self.copy_to_clipboard(caption_text))
        copy_button.grid(row=0, column=3, sticky='ne',padx=0, pady=0)

        # Tambahkan tombol simpan
        save_button = ttk.Button(self.preview_frame, text="Simpan", command=lambda: self.save_image(save_path))
        save_button.grid(row=2, column=0, sticky='sw', padx=10, pady=20)

        diseminasi_button = ttk.Button(self.preview_frame, text="Diseminasi", command=open_publer)
        diseminasi_button.grid(row=2, column=1, columnspan=2, sticky='ss', padx=10, pady=20)

    # Tambahkan fungsi untuk menyimpan gambar
    def save_image(self, save_path):
        try:
            # Simpan gambar yang telah dibuat
            self.background.save(save_path)
            messagebox.showinfo("Sukses", "Gambar telah disimpan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan gambar: {str(e)}")
  
    def copy_to_clipboard(self, caption_text):
        """Menyalin teks caption ke clipboard"""
        self.clipboard_clear()
        self.clipboard_append(caption_text)
        print("Caption telah disalin ke clipboard.")
        
    def translate_wxrev_code(self, wxrev_code):
        parts = wxrev_code.split()
        wxrev_index = parts.index('WXREV') + 3
        
        temperature_code = parts[wxrev_index]
        pressure_code = parts[wxrev_index + 1]
        humidity_code = parts[wxrev_index + 2]
        wind_code = parts[wxrev_index + 4]

        min_temp = int(temperature_code[3:])
        max_temp = int(temperature_code[1:3])
        temperature_info = f"{min_temp} - {max_temp} Celsius"
        
        qfe = 1000 + int(pressure_code[3:])
        qff = 1000 + int(pressure_code[1:3])
        pressure_info = f"{qfe} - {qff} mb"
        
        min_humidity = int(humidity_code[3:])
        max_humidity = int(humidity_code[1:3])
        humidity_info = f"{min_humidity} - {max_humidity} %"
        
        directions = {
            '0': 'Utara', 
            '1': 'Timur Laut', 
            '2': 'Timur', 
            '3': 'Tenggara',
            '4': 'Selatan', 
            '5': 'Barat Daya', 
            '6': 'Barat', 
            '7': 'Barat Laut'
        }
        wind_direction_code = wind_code[2:3]
        wind_direction = directions.get(wind_direction_code, 'Tidak diketahui')
        wind_speed = int(wind_code[3:])
        wind_info = f"{wind_direction} {wind_speed} knot"
        
        self.temperature_info = f"{min_temp} - {max_temp} \u00B0C"
        self.pressure_info = f"{qfe} - {qff} mb"
        self.humidity_info = f"{min_humidity} - {max_humidity} %"
        self.wind_info = f"{wind_direction} | {wind_speed} knot"

        return temperature_info, pressure_info, humidity_info, wind_info

if __name__ == "__main__":
    root = tk.Tk()
    app = WxrevMenu(root, None)  # Tambahkan controller None untuk menjalankan tanpa kontroler
    root.mainloop()
