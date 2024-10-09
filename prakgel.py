import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import Button, ttk
from fungsiPrakgel import add_icon, posisi_center_tgl, posisi_center_data, posisi_data_cuaca, parse_weather_data, draw_text_wrapped_centered, copy_caption, buka_kedua_url, buka_web, simpan_ke_komputer

def resource_path(relative_path):
    """ Dapatkan path absolut untuk file dalam resource (jika dibundle menggunakan PyInstaller) """
    try:
        base_path = sys._MEIPASS  # pylint: disable=W0212,E1101
    except Exception:
        base_path = os.path.abspath(".")  # untuk jalur file saat development

    return os.path.join(base_path, relative_path)


class PrakgelMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Load gambar untuk tombol "Kembali"
        image_path = resource_path("assets//back-button.png")
        image = Image.open(image_path)
        image = image.resize((25, 25), Image.Resampling.LANCZOS)
        back_button_image = ImageTk.PhotoImage(image)

        # Tambahkan tombol "Kembali"
        back_button = tk.Button(self, image=back_button_image, command=lambda: controller.show_frame("HomePageApp"), borderwidth=0)
        back_button.image = back_button_image  # Simpan referensi gambar agar tidak dihapus oleh garbage collector
        back_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        # Background images (sama seperti yang ada di program pertama)
        bg1_path = resource_path("assets//bg_prakgel1.png")
        bg2_path = resource_path("assets//bg_prakgel2.png")
        self.background1 = Image.open(bg1_path)
        self.background2 = Image.open(bg2_path)
        self.image_width, self.image_height = self.background1.size

        # Mengatur konfigurasi grid untuk frame gambar agar berada di tengah
        self.grid_columnconfigure(0, weight=1)  # Kolom kosong di sebelah kiri
        self.grid_columnconfigure(1, weight=1)  # Kolom untuk frame gambar
        self.grid_columnconfigure(2, weight=1)  # Kolom kosong di sebelah kanan

        # Frame untuk menampilkan gambar di tengah
        self.frame_gambar = tk.Frame(self)
        self.frame_gambar.grid(row=1, column=0, columnspan=4, padx=20, pady=20)  # Menempatkan di kolom 1 tanpa sticky untuk memastikan di tengah

        # Tombol "Mulai" di tengah frame (hanya di kolom 1)
        start_button = Button(self, text="Mulai", command=lambda: self.mulai_program(self.frame_gambar), height=1, width=10)
        start_button.grid(row=3, column=0, columnspan=4, padx=20, pady=10)  # Tombol di kolom 1, tetap berada di tengah

        # Spacer untuk memastikan tombol lainnya berada di bawah
        self.grid_rowconfigure(7, weight=1)  # Membuat baris 7 sebagai spacer

        # Tombol "Simpan Ke Komputer" di bagian bawah kiri
        simpan_button = ttk.Button(self, text="Simpan Ke Komputer", command=lambda: simpan_ke_komputer(self.background1, self.background2))
        simpan_button.grid(row=8, column=0, padx=20, pady=10, sticky='sw')

        # Tombol "Cek website" di bagian bawah, di samping tombol "Simpan Ke Komputer"
        url_button = ttk.Button(self, text="Cek website", command=buka_kedua_url)
        url_button.grid(row=8, column=1, padx=20, pady=10, sticky='sw')

        # Tombol "Copy Caption" di bagian bawah, di samping tombol "Cek website"
        copy_button = ttk.Button(self, text="Copy Caption", command=copy_caption)
        copy_button.grid(row=8, column=2, padx=20, pady=10, sticky='sw')

        # Tombol "Diseminasi" di bagian bawah kanan
        diseminasi_button = ttk.Button(self, text="Diseminasi", command=buka_web)
        diseminasi_button.grid(row=8, column=3, padx=20, pady=10, sticky='se')




    def mulai_program(self, frame):
        # Logika yang ada di program pertama untuk memulai parsing dan menampilkan gambar
        urls = [
            'https://maritim.bmkg.go.id/area/pelayanan/?kode=M.02&hari=1',
            'https://maritim.bmkg.go.id/area/pelayanan/?kode=M.01&hari=1',
            'https://maritim.bmkg.go.id/area/pelayanan/?kode=M.02&hari=2',
            'https://maritim.bmkg.go.id/area/pelayanan/?kode=M.01&hari=2'
        ]
        page1 = []
        page2 = []

        # Mem-parsing data seperti di program pertama
        data_timur1 = parse_weather_data(urls[0])
        data_barat1 = parse_weather_data(urls[1])
        page1.append({'timur1': data_timur1, 'barat1': data_barat1})

        data_timur2 = parse_weather_data(urls[2])
        data_barat2 = parse_weather_data(urls[3])
        page2.append({'timur2': data_timur2, 'barat2': data_barat2})

        draw = ImageDraw.Draw(self.background1)
        draw2 = ImageDraw.Draw(self.background2)

        # Koordinat dan Font masih sama seperti sebelumnya
        font_path = resource_path("font//OpenSans-Bold.ttf")
        font_path_anton = resource_path("font//Anton.ttf")
        font_size = 17
        font_size_tgl = 22
        font = ImageFont.truetype(font_path, font_size)
        font_tgl = ImageFont.truetype(font_path_anton, font_size_tgl)

        # Tambahkan kamus untuk memetakan cuaca dengan ikon
        cuaca_icons = {
            'asap':'./assets/asap.png',
            'berawan tebal':'./assets/berawan_tebal.png',
            'berawan': './assets/berawan.png',
            'cerah berawan': './assets/cerah_berawan.png',
            'cerah': './assets/cerah.png',
            'hujan lebat': './assets/hujan_lebat.png',
            'hujan lokal': './assets/hujan_lokal.png',
            'hujan petir': './assets/hujan_petir.png',
            'hujan ringan': './assets/hujan_ringan.png',
            'hujan sedang': './assets/hujan_sedang.png',
            'kabut': './assets/kabut.png',

        }
        
        # Contoh data `page1` yang digunakan untuk di-print (digantikan dengan hasil scraping)
        data_timur1 = page1[0]['timur1']
        data_barat1 = page1[0]['barat1']
        data_timur2 = page2[0]['timur2']
        data_barat2 = page2[0]['barat2']

        # Koordinat untuk menempatkan teks pada gambar

        coordinates = {
            'timur1': {'tanggal': (170, 210), 'arah_angin': (655, 320), 'kecepatan_angin': (655, 360), 'gelombang': (655, 415), 'cuaca': (860, 415), 'peringatan': (600, 540), 'icon': (760, 150)},
            'barat1': {'arah_angin': (725, 727), 'kecepatan_angin': (725, 767), 'gelombang': (725, 822), 'cuaca': (530, 822), 'icon': (430, 560)},
            'timur2': {'tanggal': (170, 200), 'arah_angin': (655, 320), 'kecepatan_angin': (655, 360), 'gelombang': (655, 415), 'cuaca': (860, 415), 'peringatan': (600, 540), 'icon': (760, 150)},
            'barat2': {'arah_angin': (725, 727), 'kecepatan_angin': (725, 767), 'gelombang': (725, 822), 'cuaca': (530, 822), 'icon': (430, 560)}
        }

        # Tambahkan ikon dan teks seperti di program pertama
        add_icon(draw, data_timur1['cuaca'], coordinates['timur1']['icon'], self.background1)
        add_icon(draw, data_barat1['cuaca'], coordinates['barat1']['icon'], self.background1)
        add_icon(draw2, data_timur2['cuaca'], coordinates['timur2']['icon'], self.background2)
        add_icon(draw2, data_barat2['cuaca'], coordinates['barat2']['icon'], self.background2)

        # Menambahkan data cuaca
        posisi_center_tgl(draw, data_timur1['tanggal'], coordinates['timur1']['tanggal'][1], font_tgl, self.image_width, fill=(247, 137, 0))
        posisi_center_tgl(draw2, data_timur2['tanggal'], coordinates['timur2']['tanggal'][1], font_tgl, self.image_width, fill=(47,81,132))
        print(data_timur1['tanggal'])
        print(data_timur2['tanggal'])

        # PAGE 1
        # menambahkan teks data cuaca timur 1
        posisi_center_data(draw, data_timur1['arah_angin'], coordinates['timur1']['arah_angin'], font, max_width=200)
        posisi_center_data(draw, data_timur1['kecepatan_angin'], coordinates['timur1']['kecepatan_angin'], font, max_width=200)
        posisi_center_data(draw, data_timur1['gelombang'], coordinates['timur1']['gelombang'], font, max_width=200)

        # menambahkan teks data cuaca barat 1
        posisi_center_data(draw, data_barat1['arah_angin'], coordinates['barat1']['arah_angin'], font, max_width=200)
        posisi_center_data(draw, data_barat1['kecepatan_angin'], coordinates['barat1']['kecepatan_angin'], font, max_width=200)
        posisi_center_data(draw, data_barat1['gelombang'], coordinates['barat1']['gelombang'], font, max_width=200)

        # PAGE 2
        # menambahkan teks data cuaca timur 2
        posisi_center_data(draw2, data_timur2['arah_angin'], coordinates['timur2']['arah_angin'], font, max_width=200)
        posisi_center_data(draw2, data_timur2['kecepatan_angin'], coordinates['timur2']['kecepatan_angin'], font, max_width=200)
        posisi_center_data(draw2, data_timur2['gelombang'], coordinates['timur2']['gelombang'], font, max_width=200)
        # menambahkan teks data cuaca barat 2
        posisi_center_data(draw2, data_barat2['arah_angin'], coordinates['barat2']['arah_angin'], font, max_width=200)
        posisi_center_data(draw2, data_barat2['kecepatan_angin'], coordinates['barat2']['kecepatan_angin'], font, max_width=200)
        posisi_center_data(draw2, data_barat2['gelombang'], coordinates['barat2']['gelombang'], font, max_width=200)

        # PAGE 1
        # Menambahkan teks data cuaca timur1 dengan padding Y kecil antara baris
        posisi_data_cuaca(draw, data_timur1['cuaca'].replace(' ', '\n'), coordinates['timur1']['cuaca'], font, max_width=200, line_spacing=-2, fill=(247, 137, 0))
        # Menambahkan teks data cuaca barat1 dengan padding Y kecil antara baris
        posisi_data_cuaca(draw, data_barat1['cuaca'].replace(' ', '\n'), coordinates['barat1']['cuaca'], font, max_width=200, line_spacing=-2, fill=(247, 137, 0))

        # PAGE 2
        # Menambahkan teks data cuaca timur2 dengan padding Y kecil antara baris
        posisi_data_cuaca(draw2, data_timur2['cuaca'].replace(' ', '\n'), coordinates['timur2']['cuaca'], font, max_width=200, line_spacing=-2, fill=(47,81,132))
        # Menambahkan teks data cuaca barat2 dengan padding Y kecil antara baris
        posisi_data_cuaca(draw2, data_barat2['cuaca'].replace(' ', '\n'), coordinates['barat2']['cuaca'], font, max_width=200, line_spacing=-2, fill=(47,81,132))

        if data_timur1['peringatan'] == 'NIL':
            data_timur1['peringatan'] = 'NIHIL'

        if data_timur2['peringatan'] == 'NIL':
            data_timur2['peringatan'] = 'NIHIL'

        draw_text_wrapped_centered(
            draw, 
            'Kotabaru, Tanah Bumbu, Hulu Sungai Selatan, Hulu Sungai dan Tengah.', 
            coordinates['timur2']['peringatan'], 
            font, 
            max_width=400,  # Lebar maksimal
            max_height=65,  # Tinggi maksimal area teks
            fill=(255, 0, 0)  # Warna teks
        )
        draw_text_wrapped_centered(
            draw2, 
            'Banjarmasin, Banjarbaru, Banjar, Barito Kuala, Tapin, Hulu Sungai Selatan, Hulu Sungai Tengah, Hulu Sungai Utara, Balangan, dan Tabalong, serta pada dini hari di wilayah Kabupaten Hulu Sungai Utara, Balangan, Tabatong, dan sekitarnya.', 
            coordinates['timur2']['peringatan'], 
            font, 
            max_width=400,  # Lebar maksimal
            max_height=65,  # Tinggi maksimal area teks
            fill=(255, 0, 0)  # Warna teks
        )

        # Menampilkan gambar yang telah diperbarui
        self.preview_image(frame, self.background1, self.background2)

    def preview_image(self, frame, image1, image2):
        # Resize image untuk preview
        preview_image1 = image1.resize((500, 500))
        preview_image2 = image2.resize((500, 500))

        # Convert to PhotoImage untuk tkinter
        preview_image_tk1 = ImageTk.PhotoImage(preview_image1)
        preview_image_tk2 = ImageTk.PhotoImage(preview_image2)

        # Label untuk menampilkan gambar pertama
        label_image1 = tk.Label(frame, image=preview_image_tk1)
        label_image1.image = preview_image_tk1
        label_image1.grid(row=0, column=0, padx=20, pady=10)

        # Label untuk menampilkan gambar kedua
        label_image2 = tk.Label(frame, image=preview_image_tk2)
        label_image2.image = preview_image_tk2
        label_image2.grid(row=0, column=1, padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PrakgelMenu(root, None)
    root.mainloop()