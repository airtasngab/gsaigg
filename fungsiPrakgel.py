import sys
import os
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timedelta
from PIL import Image
from tkinter import Tk, messagebox
import webbrowser
from dateutil import parser
import pyperclip

def resource_path(relative_path):
    """ Dapatkan path absolut untuk file dalam resource (jika dibundle menggunakan PyInstaller) """
    try:
        base_path = sys._MEIPASS  # pylint: disable=W0212,E1101
    except Exception:
        base_path = os.path.abspath(".")  # untuk jalur file saat development

    return os.path.join(base_path, relative_path)

# Baca gambar latar belakang
path_bg = resource_path("assets//bg_prakgel1.png")
path_bg2 = resource_path("assets//bg_prakgel2.png")

background = Image.open(path_bg)
background2 = Image.open(path_bg2)
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


    # Tambahkan kondisi cuaca lainnya sesuai kebutuhan
}
# Fungsi untuk menambahkan gambar ikon cuaca
def add_icon(draw, cuaca, position, background):
    # Pilih ikon cuaca berdasarkan data cuaca
    cuaca_lower = cuaca.lower()  # Agar tidak case-sensitive
    icon_path = cuaca_icons.get(cuaca_lower)

    if icon_path:  # Jika ikon tersedia
        try:
            icon_image = Image.open(icon_path)
            # Ubah ukuran ikon jika diperlukan (misalnya 50x50 piksel)
            icon_image = icon_image.resize((400, 400))
            # Tempelkan ikon di posisi yang ditentukan
            background.paste(icon_image, position, icon_image)  # Ikon dengan alpha channel
        except FileNotFoundError:
            print(f"Ikon untuk '{cuaca}' tidak ditemukan di jalur: {icon_path}")
    else:
        print(f"Tidak ada ikon yang cocok untuk cuaca: {cuaca}")


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

# Fungsi untuk menambahkan teks ke gambar dengan posisi tengah
def posisi_center_data(draw, text, position, font, max_width, fill=(255, 255, 255)):
    # Hitung ukuran teks menggunakan textbbox (lebih akurat dan versi baru dari Pillow)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    
    # Jika teks lebih lebar dari area maksimum yang diizinkan, pangkas atau ubah ukuran font
    if text_width > max_width:
        # Buat mekanisme untuk memotong teks, jika diperlukan
        while text_width > max_width and len(text) > 0:
            text = text[:-1]
            text_bbox = draw.textbbox((0, 0), text + "...", font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        text += "..."
    
    # Hitung posisi X agar teks berada di tengah
    x = position[0] + (max_width - text_width) // 2
    
    # Posisi Y tetap sesuai yang diberikan
    y = position[1]
    
    # Tambahkan teks di posisi yang telah dihitung
    draw.text((x, y), text, font=font, fill=fill)

# Fungsi untuk menambahkan teks yang disesuaikan dengan kontrol padding antar baris
def posisi_data_cuaca(draw, text, position, font, max_width, line_spacing=0, fill=(255, 255, 255)):
    # Pisahkan teks menjadi beberapa baris berdasarkan newline (\n)
    lines = text.split('\n')

    # Hitung tinggi teks total (menggunakan height dari textbbox)
    total_height = 0
    line_heights = []
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        line_height = text_bbox[3] - text_bbox[1]
        line_heights.append(line_height)
        total_height += line_height + line_spacing

    # Hitung posisi awal Y untuk menempatkan teks agar vertikal berada di tengah
    y = position[1] - total_height // 2

    # Cetak setiap baris teks secara manual
    for i, line in enumerate(lines):
        # Hitung lebar baris saat ini
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]

        # Hitung posisi X agar teks berada di tengah
        x = position[0] + (max_width - text_width) // 2

        # Cetak teks pada posisi yang dihitung
        draw.text((x, y), line, font=font, fill=fill)

        # Pindahkan Y ke bawah untuk baris berikutnya, dengan menambahkan line_spacing
        y += line_heights[i] + line_spacing

# Fungsi untuk mem-parsing halaman web dan mengambil data yang diperlukan
def parse_weather_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract informasi dan lakukan parsing seperti yang telah dilakukan sebelumnya
    # ...
    # Extract information for blog-view
    blog_view_elements = soup.find_all(class_='blog-view')
    blog_view_info = [element.get_text(strip=True) for element in blog_view_elements]

    # Format output for testing
    if len(blog_view_info) > 2:
        output_text = blog_view_info[2]
    else:
        output_text = "Data not available."

    # Fungsi untuk konversi waktu dari WIB ke WITA
    # def convert_wib_to_wita(wib_time_str):
    #     wib_time_str += ' WIB'  # Menambahkan WIB jika tidak ada
    #     wib_time = datetime.strptime(wib_time_str, '%A, %d %B %Y %H:%M WIB')
    #     wita_time = wib_time + timedelta(hours=1)
    #     wita_time_str = wita_time.strftime('%A, %d %B %Y %H:%M WITA')
    #     return wita_time_str
    
    

    def convert_wib_to_wita(wib_time_str):
        # Parse the date string with dateutil.parser
        wib_time = parser.parse(wib_time_str)
        wita_time = wib_time + timedelta(hours=1)
        wita_time_str = wita_time.strftime('%A, %d %B %Y %H:%M WITA')
        return wita_time_str


    # Konversi nama hari dan bulan ke bahasa Indonesia
    hari_indo = {
        'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
        'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
    }

    bulan_indo = {
        'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
        'April': 'April', 'May': 'Mei', 'June': 'Juni',
        'July': 'Juli', 'August': 'Agustus', 'September': 'September',
        'October': 'Oktober', 'November': 'November', 'December': 'Desember'
    }

    def translate_datetime(date_str):
        for eng, indo in hari_indo.items():
            date_str = date_str.replace(eng, indo)
        for eng, indo in bulan_indo.items():
            date_str = date_str.replace(eng, indo)
        return date_str

    # Fungsi untuk mengonversi kecepatan dari knots ke km/jam
    def convert_knots_to_kmph(knots):
        return round(knots * 1.852)

    # Parsing tanggal dan waktu
    tanggal_element = soup.find('p').text
    tanggal_pattern = r'Berlaku mulai (.+?) Sampai (.+)'
    tanggal_match = re.search(tanggal_pattern, tanggal_element)
    tanggal_mulai_wib = tanggal_match.group(1).strip()
    tanggal_sampai_wib = tanggal_match.group(2).strip()

    def format_date(tanggal_mulai, tanggal_sampai):
        mulai_wita = convert_wib_to_wita(tanggal_mulai)
        sampai_wita = convert_wib_to_wita(tanggal_sampai)

        # Mengambil bagian tanggal dan waktu dari hasil konversi WITA
        mulai_date_parts = mulai_wita.split(' ')
        sampai_date_parts = sampai_wita.split(' ')

        # Mengambil bagian tanggal yang terdiri dari Hari, Tanggal, Bulan, dan Tahun
        mulai_date_str = ' '.join(mulai_date_parts[0:4])  # Menyertakan Tahun
        mulai_time = mulai_date_parts[4]
        sampai_date_str = ' '.join(sampai_date_parts[0:4])  # Menyertakan Tahun
        sampai_time = sampai_date_parts[4]

        # Jika tanggal mulai dan sampai sama, hanya tampilkan satu tanggal
        if mulai_date_str == sampai_date_str:
            result = f"Berlaku mulai {translate_datetime(mulai_date_str)} pukul {mulai_time} - {sampai_time} WITA"
        else:
            result = f"Berlaku mulai {translate_datetime(mulai_date_str)} pukul {mulai_time} WITA - {translate_datetime(sampai_date_str)} pukul {sampai_time} WITA"
        
        return result

    try:
        tanggal_info = format_date(tanggal_mulai_wib, tanggal_sampai_wib)
    except ValueError as e:
        tanggal_info = f'Error parsing date: {e}\n'

    # Parsing peringatan
    peringatan_element = soup.find('h3', string='Peringatan').find_all_next('p')[1].text.strip()

    # Parsing cuaca
    cuaca_element = soup.find('div', class_='number-structure-left').find_all('p')[1].text.strip()

    # Parsing arah angin
    arah_angin_element = soup.find_all('div', class_='number-structure-left')[1].find_all('p')[2].text.strip()
    arah_angin_element = re.sub(r'\s+', ' ', arah_angin_element)

    # Parsing kecepatan angin
    kecepatan_angin_text = soup.find_all('div', class_='number-structure-left')[1].find_all('p')[1].text.strip()
    kecepatan_angin_knots = [int(k.strip()) for k in re.findall(r'\d+', kecepatan_angin_text)]
    kecepatan_angin_kmph = [convert_knots_to_kmph(k) for k in kecepatan_angin_knots]
    kecepatan_angin_element = f"{kecepatan_angin_kmph[0]} - {kecepatan_angin_kmph[1]} km/jam"

    # Parsing gelombang
    gelombang_element = soup.find_all('div', class_='number-structure-left')[2].find_all('p')[2].text.strip()

    return {
        'tanggal': tanggal_info,
        'peringatan': peringatan_element,
        'cuaca': cuaca_element,
        'arah_angin': arah_angin_element,
        'kecepatan_angin': kecepatan_angin_element,
        'gelombang': gelombang_element
    }

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

def show_popup(message):
    root = Tk()
    root.withdraw()  # Menyembunyikan jendela utama tkinter
    messagebox.showinfo("Notifikasi", message)
    root.destroy()  # Menghancurkan jendela tkinter setelah pop-up

# Fungsi untuk membuka web diseminasi
def buka_web():
    webbrowser.open("https://app.publer.io/#/posts")

# Fungsi untuk membuka dua URL
def buka_kedua_url():
    webbrowser.open_new_tab("https://maritim.bmkg.go.id/area/pelayanan/?kode=M.02&hari=1")  # URL pertama
    webbrowser.open_new_tab("https://maritim.bmkg.go.id/area/pelayanan/?kode=M.01&hari=1")  # URL kedua

# Fungsi untuk menyalin caption ke clipboard
def copy_caption():
    caption = 'Jangan lupa cek info prakiraan cuaca kelautan wilayah Kotabaru malam ini dan esok hari ya!\nInfo lebih lanjut bisa langsung cek website kita berikut ini https://peta-maritim.bmkg.go.id/\n#CuacaKalsel #infoBMKG #InfoKalsel #CuacaKotabaru #KotabaruInfo #BanggaMelayaniBangsa'
    pyperclip.copy(caption)
    show_popup("Caption berhasil disalin ke clipboard!")

def create_folder_structure(base_folder, gelombang, tahun, bulan):
    folder_path = os.path.join(base_folder, gelombang, tahun, bulan)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# Fungsi untuk menyimpan gambar ke komputer
def simpan_ke_komputer(image1, image2):
    # Ambil tanggal dari data scraping atau sekarang
    tanggal_wita = datetime.now()
    tahun = tanggal_wita.strftime('%Y')
    bulan = tanggal_wita.strftime('%m')
    tanggal = tanggal_wita.strftime('%d')

    # Struktur folder
    base_folder = resource_path("Infografis")
    gelombang = "Gelombang"
    folder_path = create_folder_structure(base_folder, gelombang, tahun, bulan)

    # Simpan hasi gambar
    file_name1 = f"{tanggal}_a.png"
    file_name2 = f"{tanggal}_b.png"
    output_image_path1 = os.path.join(folder_path, file_name1)
    output_image_path2 = os.path.join(folder_path, file_name2)

    if output_image_path1 and output_image_path2:
        image1.save(output_image_path1)
        image2.save(output_image_path2)
        message = f"Gambar disimpan di {output_image_path1} dan {output_image_path2}."
        show_popup(message)