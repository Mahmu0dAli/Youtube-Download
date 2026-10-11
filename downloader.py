import os
import sys
import subprocess

# --- 1. Auto-Check & Install Required Dependencies ---
REQUIRED_PACKAGES = {
    "customtkinter": "customtkinter",
    "yt_dlp": "yt-dlp",
    "imageio_ffmpeg": "imageio-ffmpeg"
}

def check_and_install_packages():
    missing = []
    for module_name, pip_name in REQUIRED_PACKAGES.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(pip_name)
    
    if missing:
        print(f"Installing missing packages automatically: {', '.join(missing)}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("Packages installed successfully!")
        except Exception as e:
            print(f"Error installing packages: {e}")
            sys.exit(1)

check_and_install_packages()

# --- 2. Main Application ---
import threading
import queue
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

import yt_dlp
import imageio_ffmpeg

# Set ffmpeg path
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- Translations Dictionary ---
TRANSLATIONS = {
    "ar": {
        "title": "أداة تحميل الفيديوهات وقوائم التشغيل (Advanced YouTube Downloader)",
        "url_label": "رابط الفيديو / القائمة:",
        "url_placeholder": "الصق الرابط هنا (Ctrl+V)...",
        "type_label": "النوع:",
        "type_video": "فيديو (Video)",
        "type_audio": "صوت فقط (Audio MP3)",
        "quality_label": "الدقة والجودة:",
        "qual_best_video": "أفضل دقة (Best)",
        "qual_best_audio": "أفضل جودة صوت (MP3)",
        "mode_label": "وضع التحميل:",
        "mode_playlist": "قائمة/جماعي (Playlist/Batch)",
        "mode_single": "فردي فقط (Single Video)",
        "speed_label": "تحديد السرعة:",
        "speed_unlimited": "غير محدود (Unlimited)",
        "path_label": "مجلد الحفظ:",
        "browse_btn": "استعراض...",
        "download_btn": "بدء التحميل",
        "stop_btn": "إيقاف مؤقت / إلغاء",
        "curr_item_label": "الملف الحالي:",
        "waiting": "في الانتظار...",
        "overall_label": "التقدم الإجمالي:",
        "lang_label": "اللغة (Language):",
        "success_title": "نجاح",
        "success_msg": "تم تحميل الملفات بنجاح!",
        "error_title": "خطأ",
        "error_url": "الرجاء إدخال الرابط!",
        "error_path": "تعذر إنشاء مجلد الحفظ:",
        "stopped": "تم التوقف / حدث خطأ.",
        "downloading": "جاري التحميل...",
        "speed": "السرعة",
        "eta": "متبقي",
        "processing": "جاري المعالجة والدمج (FFmpeg)...",
        "completed": "مكتمل",
        "footer": "Developed by Mahmoud Ali | GitHub: github.com/Mahmu0dAli"
    },
    "en": {
        "title": "Advanced YouTube Downloader",
        "url_label": "Video / Playlist URL:",
        "url_placeholder": "Paste URL here (Ctrl+V)...",
        "type_label": "Type:",
        "type_video": "Video",
        "type_audio": "Audio Only (MP3)",
        "quality_label": "Quality:",
        "qual_best_video": "Best Quality",
        "qual_best_audio": "Best Audio (MP3)",
        "mode_label": "Mode:",
        "mode_playlist": "Playlist / Batch",
        "mode_single": "Single Video",
        "speed_label": "Speed Limit:",
        "speed_unlimited": "Unlimited",
        "path_label": "Save Path:",
        "browse_btn": "Browse...",
        "download_btn": "Start Download",
        "stop_btn": "Pause / Cancel",
        "curr_item_label": "Current Item:",
        "waiting": "Waiting...",
        "overall_label": "Overall Progress:",
        "lang_label": "Language:",
        "success_title": "Success",
        "success_msg": "Files downloaded successfully!",
        "error_title": "Error",
        "error_url": "Please enter a URL!",
        "error_path": "Could not create save directory:",
        "stopped": "Stopped / Error occurred.",
        "downloading": "Downloading...",
        "speed": "Speed",
        "eta": "ETA",
        "processing": "Processing & Merging (FFmpeg)...",
        "completed": "completed",
        "footer": "Developed by Mahmoud Ali | GitHub: github.com/Mahmu0dAli"
    },
    "tr": {
        "title": "Gelişmiş YouTube İndirici (Advanced YouTube Downloader)",
        "url_label": "Video / Oynatma Listesi URL:",
        "url_placeholder": "URL'yi buraya yapıştırın (Ctrl+V)...",
        "type_label": "Tür:",
        "type_video": "Video",
        "type_audio": "Sadece Ses (Audio MP3)",
        "quality_label": "Kalite:",
        "qual_best_video": "En İyi Kalite (Best)",
        "qual_best_audio": "En İyi Ses (MP3)",
        "mode_label": "Mod:",
        "mode_playlist": "Oynatma Listesi / Toplu",
        "mode_single": "Tekli Video",
        "speed_label": "Hız Sınırı:",
        "speed_unlimited": "Sınırsız (Unlimited)",
        "path_label": "Kayıt Yolu:",
        "browse_btn": "Gözat...",
        "download_btn": "İndirmeyi Başlat",
        "stop_btn": "Duraklat / İptal",
        "curr_item_label": "Mevcut Öğe:",
        "waiting": "Bekliyor...",
        "overall_label": "Genel İlerleme:",
        "lang_label": "Dil (Language):",
        "success_title": "Başarılı",
        "success_msg": "Dosyalar başarıyla indirildi!",
        "error_title": "Hata",
        "error_url": "Lütfen bir URL girin!",
        "error_path": "Kayıt dizini oluşturulamadı:",
        "stopped": "Durduruldu / Hata oluştu.",
        "downloading": "İndiriliyor...",
        "speed": "Hız",
        "eta": "Kalan",
        "processing": "İşleniyor ve Birleştiriliyor (FFmpeg)...",
        "completed": "tamamlandı",
        "footer": "Developed by Mahmoud Ali | GitHub: github.com/Mahmu0dAli"
    }
}

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_lang = "ar"  # Default language
        self.t = TRANSLATIONS[self.current_lang]

        self.title(self.t["title"])
        self.geometry("850x730")
        self.minsize(750, 680)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        # 0. Language Selector Frame
        self.lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lang_frame.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.lang_frame.grid_columnconfigure(1, weight=1)

        self.lang_label = ctk.CTkLabel(self.lang_frame, text=self.t["lang_label"], font=("Arial", 12, "bold"))
        self.lang_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.lang_var = ctk.StringVar(value="العربية (AR)")
        self.lang_menu = ctk.CTkOptionMenu(
            self.lang_frame,
            values=["العربية (AR)", "English (EN)", "Türkçe (TR)"],
            variable=self.lang_var,
            command=self.change_language,
            width=150
        )
        self.lang_menu.grid(row=0, column=1, sticky="w")

        # 1. URL Frame
        self.url_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.url_frame.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")
        self.url_frame.grid_columnconfigure(1, weight=1)

        self.url_label = ctk.CTkLabel(self.url_frame, text=self.t["url_label"], font=("Arial", 14, "bold"))
        self.url_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text=self.t["url_placeholder"], height=35)
        self.url_entry.grid(row=0, column=1, sticky="ew")
        self.url_entry.focus()

        # 2. Options Frame (Type, Resolution)
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_columnconfigure(3, weight=1)

        self.type_label = ctk.CTkLabel(self.options_frame, text=self.t["type_label"], font=("Arial", 12))
        self.type_label.grid(row=0, column=0, padx=15, pady=12, sticky="w")
        
        self.type_var = ctk.StringVar(value=self.t["type_video"])
        self.type_menu = ctk.CTkOptionMenu(
            self.options_frame, 
            values=[self.t["type_video"], self.t["type_audio"]],
            variable=self.type_var,
            command=self.on_type_change
        )
        self.type_menu.grid(row=0, column=1, padx=15, pady=12, sticky="ew")

        self.quality_label = ctk.CTkLabel(self.options_frame, text=self.t["quality_label"], font=("Arial", 12))
        self.quality_label.grid(row=0, column=2, padx=15, pady=12, sticky="w")

        self.quality_var = ctk.StringVar(value=self.t["qual_best_video"])
        self.quality_menu = ctk.CTkOptionMenu(
            self.options_frame,
            values=[self.t["qual_best_video"], "1080p", "720p", "480p", "360p"],
            variable=self.quality_var
        )
        self.quality_menu.grid(row=0, column=3, padx=15, pady=12, sticky="ew")

        # 3. Advanced Options Frame (Mode, Speed Limit)
        self.adv_frame = ctk.CTkFrame(self)
        self.adv_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.adv_frame.grid_columnconfigure(1, weight=1)
        self.adv_frame.grid_columnconfigure(3, weight=1)

        self.mode_label = ctk.CTkLabel(self.adv_frame, text=self.t["mode_label"], font=("Arial", 12))
        self.mode_label.grid(row=0, column=0, padx=15, pady=12, sticky="w")

        self.mode_var = ctk.StringVar(value=self.t["mode_playlist"])
        self.mode_menu = ctk.CTkOptionMenu(
            self.adv_frame,
            values=[self.t["mode_playlist"], self.t["mode_single"]],
            variable=self.mode_var
        )
        self.mode_menu.grid(row=0, column=1, padx=15, pady=12, sticky="ew")

        self.speed_label = ctk.CTkLabel(self.adv_frame, text=self.t["speed_label"], font=("Arial", 12))
        self.speed_label.grid(row=0, column=2, padx=15, pady=12, sticky="w")

        self.speed_var = ctk.StringVar(value=self.t["speed_unlimited"])
        self.speed_menu = ctk.CTkOptionMenu(
            self.adv_frame,
            values=[self.t["speed_unlimited"], "500 KB/s", "1 MB/s", "2 MB/s", "5 MB/s"],
            variable=self.speed_var
        )
        self.speed_menu.grid(row=0, column=3, padx=15, pady=12, sticky="ew")

        # 4. Save Path Frame
        self.path_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.path_frame.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        self.path_frame.grid_columnconfigure(1, weight=1)

        self.path_label = ctk.CTkLabel(self.path_frame, text=self.t["path_label"], font=("Arial", 12))
        self.path_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.path_entry = ctk.CTkEntry(self.path_frame, height=30)
        self.path_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        self.path_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))

        self.browse_btn = ctk.CTkButton(self.path_frame, text=self.t["browse_btn"], width=100, command=self.browse_path)
        self.browse_btn.grid(row=0, column=2)

        # 5. Buttons Frame (Download & Stop)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.download_btn = ctk.CTkButton(
            self.btn_frame, 
            text=self.t["download_btn"], 
            font=("Arial", 15, "bold"), 
            height=42,
            fg_color="#2fa572", 
            hover_color="#1e7b51",
            command=self.start_download_thread
        )
        self.download_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.stop_btn = ctk.CTkButton(
            self.btn_frame, 
            text=self.t["stop_btn"], 
            font=("Arial", 15, "bold"), 
            height=42,
            fg_color="#c0392b", 
            hover_color="#962d22",
            state="disabled",
            command=self.stop_download
        )
        self.stop_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # 6. Progress Bars Frame
        self.prog_frame = ctk.CTkFrame(self)
        self.prog_frame.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        self.prog_frame.grid_columnconfigure(1, weight=1)

        # Current Item Progress
        self.curr_label_title = ctk.CTkLabel(self.prog_frame, text=self.t["curr_item_label"], font=("Arial", 11, "bold"))
        self.curr_label_title.grid(row=0, column=0, padx=10, pady=(10, 2), sticky="w")

        self.curr_info_label = ctk.CTkLabel(self.prog_frame, text=self.t["waiting"], font=("Arial", 11), text_color="gray")
        self.curr_info_label.grid(row=0, column=1, padx=10, pady=(10, 2), sticky="w")

        self.curr_bar = ctk.CTkProgressBar(self.prog_frame)
        self.curr_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        self.curr_bar.set(0)

        # Overall Progress
        self.overall_label_title = ctk.CTkLabel(self.prog_frame, text=self.t["overall_label"], font=("Arial", 11, "bold"))
        self.overall_label_title.grid(row=2, column=0, padx=10, pady=(5, 2), sticky="w")

        self.overall_info_label = ctk.CTkLabel(self.prog_frame, text="0 / 0", font=("Arial", 11), text_color="gray")
        self.overall_info_label.grid(row=2, column=1, padx=10, pady=(5, 2), sticky="w")

        self.overall_bar = ctk.CTkProgressBar(self.prog_frame)
        self.overall_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        self.overall_bar.set(0)

        # 7. Log Console & Footer Frame
        self.console_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.console_frame.grid(row=7, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.console_frame.grid_columnconfigure(0, weight=1)
        self.console_frame.grid_rowconfigure(0, weight=1)

        self.log_box = ctk.CTkTextbox(self.console_frame, font=("Consolas", 11))
        self.log_box.grid(row=0, column=0, sticky="nsew", pady=(0, 5))

        self.footer_label = ctk.CTkLabel(
            self.console_frame, 
            text=self.t["footer"], 
            font=("Arial", 10), 
            text_color="gray"
        )
        self.footer_label.grid(row=1, column=0, sticky="e")

        self.msg_queue = queue.Queue()
        self.after(100, self.process_queue)
        self.ydl_instance = None

    def change_language(self, choice):
        if "AR" in choice:
            self.current_lang = "ar"
        elif "EN" in choice:
            self.current_lang = "en"
        elif "TR" in choice:
            self.current_lang = "tr"
        
        self.t = TRANSLATIONS[self.current_lang]
        self.update_ui_texts()

    def update_ui_texts(self):
        self.title(self.t["title"])
        self.lang_label.configure(text=self.t["lang_label"])
        self.url_label.configure(text=self.t["url_label"])
        self.url_entry.configure(placeholder_text=self.t["url_placeholder"])
        self.type_label.configure(text=self.t["type_label"])
        
        curr_type = self.type_var.get()
        new_types = [self.t["type_video"], self.t["type_audio"]]
        self.type_menu.configure(values=new_types)
        if "صوت" in curr_type or "Audio" in curr_type or "Ses" in curr_type:
            self.type_var.set(self.t["type_audio"])
        else:
            self.type_var.set(self.t["type_video"])

        self.quality_label.configure(text=self.t["quality_label"])
        self.on_type_change(self.type_var.get())

        self.mode_label.configure(text=self.t["mode_label"])
        self.mode_menu.configure(values=[self.t["mode_playlist"], self.t["mode_single"]])
        self.mode_var.set(self.t["mode_playlist"])

        self.speed_label.configure(text=self.t["speed_label"])
        self.speed_menu.configure(values=[self.t["speed_unlimited"], "500 KB/s", "1 MB/s", "2 MB/s", "5 MB/s"])
        self.speed_var.set(self.t["speed_unlimited"])

        self.path_label.configure(text=self.t["path_label"])
        self.browse_btn.configure(text=self.t["browse_btn"])
        self.download_btn.configure(text=self.t["download_btn"])
        self.stop_btn.configure(text=self.t["stop_btn"])
        self.curr_label_title.configure(text=self.t["curr_item_label"])
        self.overall_label_title.configure(text=self.t["overall_label"])
        self.footer_label.configure(text=self.t["footer"])

    def on_type_change(self, choice):
        if self.current_lang == "ar":
            if "صوت" in choice:
                self.quality_menu.configure(values=[self.t["qual_best_audio"], "192kbps", "128kbps"])
                self.quality_var.set(self.t["qual_best_audio"])
            else:
                self.quality_menu.configure(values=[self.t["qual_best_video"], "1080p", "720p", "480p", "360p"])
                self.quality_var.set(self.t["qual_best_video"])
        elif self.current_lang == "tr":
            if "Ses" in choice:
                self.quality_menu.configure(values=[self.t["qual_best_audio"], "192kbps", "128kbps"])
                self.quality_var.set(self.t["qual_best_audio"])
            else:
                self.quality_menu.configure(values=[self.t["qual_best_video"], "1080p", "720p", "480p", "360p"])
                self.quality_var.set(self.t["qual_best_video"])
        else:
            if "Audio" in choice:
                self.quality_menu.configure(values=[self.t["qual_best_audio"], "192kbps", "128kbps"])
                self.quality_var.set(self.t["qual_best_audio"])
            else:
                self.quality_menu.configure(values=[self.t["qual_best_video"], "1080p", "720p", "480p", "360p"])
                self.quality_var.set(self.t["qual_best_video"])

    def browse_path(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, dir_path)

    def log(self, message):
        self.msg_queue.put(("log", message))

    def set_curr_info(self, text):
        self.msg_queue.put(("curr_info", text))

    def set_curr_progress(self, val):
        self.msg_queue.put(("curr_prog", val))

    def set_overall_info(self, text):
        self.msg_queue.put(("overall_info", text))

    def set_overall_progress(self, val):
        self.msg_queue.put(("overall_prog", val))

    def stop_download(self):
        if self.ydl_instance:
            self.ydl_instance._should_stop = True
            self.log("Stop requested... stopping safely." if self.current_lang != "ar" else "تم إرسال طلب إيقاف التحميل... جاري التوقف الآمن.")
            self.set_curr_info(self.t["stopped"])
        self.stop_btn.configure(state="disabled")
        self.download_btn.configure(state="normal")

    def process_queue(self):
        try:
            while True:
                msg_type, data = self.msg_queue.get_nowait()
                if msg_type == "log":
                    self.log_box.insert(tk.END, data + "\n")
                    self.log_box.see(tk.END)
                elif msg_type == "curr_info":
                    self.curr_info_label.configure(text=data)
                elif msg_type == "curr_prog":
                    self.curr_bar.set(data)
                elif msg_type == "overall_info":
                    self.overall_info_label.configure(text=data)
                elif msg_type == "overall_prog":
                    self.overall_bar.set(data)
                elif msg_type == "enable":
                    state = "normal" if data else "disabled"
                    self.download_btn.configure(state=state)
                elif msg_type == "stop_enable":
                    state = "normal" if data else "disabled"
                    self.stop_btn.configure(state=state)
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def ytdl_hook(self, d):
        if d['status'] == 'downloading':
            p_str = d.get('_percent_str', '0%').strip()
            import re
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            p_str_clean = ansi_escape.sub('', p_str)
            
            try:
                percent = float(p_str_clean.replace('%', '')) / 100.0
                self.set_curr_progress(percent)
            except:
                pass
            
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            filename = os.path.basename(d.get('filename', ''))
            self.set_curr_info(f"{filename[:40]}... | {p_str_clean} | {self.t['speed']}: {speed} | {self.t['eta']}: {eta}")
            
        elif d['status'] == 'finished':
            filename = os.path.basename(d.get('filename', ''))
            self.log(f"Finished downloading and processing: {filename}")
            self.set_curr_info(self.t["processing"])
            self.set_curr_progress(1.0)

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror(self.t["error_title"], self.t["error_url"])
            return

        save_path = self.path_entry.get().strip()
        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except Exception as e:
                messagebox.showerror(self.t["error_title"], f"{self.t['error_path']}\n{e}")
                return

        self.download_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.curr_bar.set(0)
        self.overall_bar.set(0)
        self.log_box.delete("0.0", tk.END)

        download_type = self.type_var.get()
        quality = self.quality_var.get()
        mode = self.mode_var.get()
        speed_limit = self.speed_var.get()

        self.ydl_instance = None
        t = threading.Thread(target=self.run_download, args=(url, save_path, download_type, quality, mode, speed_limit))
        t.daemon = True
        t.start()

    def run_download(self, url, save_path, download_type, quality, mode, speed_limit):
        try:
            self.log(f"Connecting to URL: {url}")
            self.set_curr_info("Analyzing URL...")

            class YTDLLogger:
                def __init__(self, outer):
                    self.outer = outer
                def debug(self, msg):
                    if not msg.startswith('[debug]'):
                        self.outer.log(msg)
                def info(self, msg):
                    self.outer.log(msg)
                def warning(self, msg):
                    self.outer.log(f"Warning: {msg}")
                def error(self, msg):
                    self.outer.log(f"Error: {msg}")

            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(playlist_title)s/%(title)s.%(ext)s' if '%(playlist_title)s' else '%(title)s.%(ext)s'),
                'progress_hooks': [self.ytdl_hook],
                'logger': YTDLLogger(self),
                'ffmpeg_location': ffmpeg_path,
                'no_color': True,
                'merge_output_format': 'mp4',
                'download_archive': os.path.join(save_path, 'downloaded_archive.txt'),
            }

            if "Single" in mode or "فردي" in mode or "Tekli" in mode:
                ydl_opts['extract_flat'] = False
                ydl_opts['noplaylist'] = True
                self.log("Download mode: Single video")
            else:
                ydl_opts['noplaylist'] = False
                self.log("Download mode: Playlist / Batch")

            if "500 KB" in speed_limit:
                ydl_opts['ratelimit'] = 500 * 1024
            elif "1 MB" in speed_limit:
                ydl_opts['ratelimit'] = 1024 * 1024
            elif "2 MB" in speed_limit:
                ydl_opts['ratelimit'] = 2 * 1024 * 1024
            elif "5 MB" in speed_limit:
                ydl_opts['ratelimit'] = 5 * 1024 * 1024

            if "صوت" in download_type or "Audio" in download_type or "Ses" in download_type:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                self.log("Download settings: Audio only (MP3)")
            else:
                if "1080p" in quality:
                    ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best'
                elif "720p" in quality:
                    ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]/best'
                elif "480p" in quality:
                    ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]/best'
                elif "360p" in quality:
                    ydl_opts['format'] = 'bestvideo[height<=360]+bestaudio/best[height<=360]/best'
                else:
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                
                self.log(f"Download settings: Video quality {quality}")

            total_items = [0]
            downloaded_items = [0]

            orig_hook = self.ytdl_hook
            def combined_hook(d):
                if getattr(self.ydl_instance, '_should_stop', False):
                    raise Exception("Download stopped by user.")
                orig_hook(d)
                if d['status'] == 'finished':
                    downloaded_items[0] += 1
                    if total_items[0] > 0:
                        self.set_overall_progress(min(downloaded_items[0] / total_items[0], 1.0))
                        self.set_overall_info(f"{downloaded_items[0]} / {total_items[0]} {self.t['completed']}")

            ydl_opts['progress_hooks'] = [combined_hook]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.ydl_instance = ydl
                info = ydl.extract_info(url, download=False)
                if info:
                    if 'entries' in info:
                        total_items[0] = len(list(info['entries']))
                    else:
                        total_items[0] = 1
                    self.set_overall_info(f"0 / {total_items[0]} {self.t['completed']}")
                
                ydl.download([url])

            self.set_curr_info("Download completed successfully!")
            self.set_overall_progress(1.0)
            self.log("All files downloaded and saved to: " + save_path)
            messagebox.showinfo(self.t["success_title"], self.t["success_msg"])

        except Exception as e:
            self.set_curr_info(self.t["stopped"])
            self.log(f"Message: {str(e)}")
        finally:
            self.ydl_instance = None
            self.msg_queue.put(("enable", True))
            self.msg_queue.put(("stop_enable", False))

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
