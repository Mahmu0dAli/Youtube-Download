import os
import sys
import subprocess
import json

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

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# Config file path
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".yt_downloader_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"save_path": os.path.join(os.path.expanduser("~"), "Downloads")}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except:
        pass

# --- Translations Dictionary ---
TRANSLATIONS = {
    "ar": {
        "title": "YouTube Downloader Pro | Enterprise Edition",
        "header_title": "مستكشف ومحمل يوتيوب الاحترافي",
        "header_subtitle": "تحميل الفيديوهات وقوائم التشغيل بأعلى كفاءة وجودة",
        "url_label": "رابط الفيديو أو قائمة التشغيل:",
        "url_placeholder": "https://www.youtube.com/watch?v=... أو رابط القائمة",
        "type_label": "نوع التحميل:",
        "type_video": "🎬 فيديو عالي الجودة (Video)",
        "type_audio": "🎵 صوت فقط نقي (MP3 Audio)",
        "quality_label": "الدقة المطلوبة:",
        "qual_best_video": "⭐ أفضل دقة متاحة (Best)",
        "qual_best_audio": "⭐ أفضل جودة صوت (192kbps)",
        "mode_label": "نمط التحميل:",
        "mode_playlist": "📚 قائمة تشغيل كاملة (Playlist)",
        "mode_single": "📄 فيديو فردي فقط (Single)",
        "speed_label": "تحديد سرعة النقل:",
        "speed_unlimited": "🚀 غير محدود (Unlimited)",
        "path_label": "مسار الحفظ المحلي:",
        "browse_btn": "تصفح...",
        "download_btn": "بدء التحميل الآن",
        "stop_btn": "إيقاف مؤقت / إلغاء",
        "curr_item_label": "الحالة الحالية:",
        "waiting": "في انتظار بدء المهمة...",
        "overall_label": "التقدم الكلي للقائمة:",
        "lang_label": "اللغة:",
        "settings_btn": "⚙️ الإعدادات",
        "settings_title": "إعدادات الأداة (Settings)",
        "settings_path_label": "المجلد الافتراضي لحفظ التحميلات:",
        "save_settings_btn": "حفظ الإعدادات",
        "success_title": "عملية ناجحة",
        "success_msg": "تم تحميل ومعالجة جميع الملفات بنجاح!",
        "settings_saved": "تم حفظ الإعدادات بنجاح!",
        "error_title": "تنبيه خطأ",
        "error_url": "الرجاء إدخال رابط صالح أولاً!",
        "error_path": "تعذر إنشاء أو الوصول لمجلد الحفظ:",
        "stopped": "تم إيقاف العملية بواسطة المستخدم.",
        "downloading": "جاري التحميل",
        "speed": "السرعة",
        "eta": "الوقت المتبقي",
        "processing": "جاري معالجة الدمج والتصدير عبر FFmpeg...",
        "completed": "مكتمل",
        "footer": "Designed & Developed by Mahmoud Ali • Enterprise Grade"
    },
    "en": {
        "title": "YouTube Downloader Pro | Enterprise Edition",
        "header_title": "YouTube Downloader Pro",
        "header_subtitle": "High-performance video & playlist extraction suite",
        "url_label": "Video or Playlist URL:",
        "url_placeholder": "https://www.youtube.com/watch?v=... or playlist link",
        "type_label": "Media Type:",
        "type_video": "🎬 High-Def Video",
        "type_audio": "🎵 Pure Audio (MP3)",
        "quality_label": "Resolution / Quality:",
        "qual_best_video": "⭐ Best Resolution",
        "qual_best_audio": "⭐ Best Audio (192kbps)",
        "mode_label": "Execution Mode:",
        "mode_playlist": "📚 Full Playlist / Batch",
        "mode_single": "📄 Single Video Only",
        "speed_label": "Bandwidth Limit:",
        "speed_unlimited": "🚀 Unlimited",
        "path_label": "Destination Directory:",
        "browse_btn": "Browse...",
        "download_btn": "Start Download",
        "stop_btn": "Pause / Cancel",
        "curr_item_label": "Current Task:",
        "waiting": "Waiting for task...",
        "overall_label": "Overall Progress:",
        "lang_label": "Language:",
        "settings_btn": "⚙️ Settings",
        "settings_title": "Application Settings",
        "settings_path_label": "Default Download Directory:",
        "save_settings_btn": "Save Settings",
        "success_title": "Success",
        "success_msg": "All files downloaded and processed successfully!",
        "settings_saved": "Settings saved successfully!",
        "error_title": "Error",
        "error_url": "Please enter a valid URL!",
        "error_path": "Could not create or access directory:",
        "stopped": "Operation stopped by user.",
        "downloading": "Downloading",
        "speed": "Speed",
        "eta": "ETA",
        "processing": "Processing & Merging via FFmpeg...",
        "completed": "completed",
        "footer": "Designed & Developed by Mahmoud Ali • Enterprise Grade"
    },
    "tr": {
        "title": "YouTube Downloader Pro | Enterprise Edition",
        "header_title": "YouTube Downloader Pro",
        "header_subtitle": "Yüksek performanslı video ve oynatma listesi indirme aracı",
        "url_label": "Video veya Oynatma Listesi URL:",
        "url_placeholder": "https://www.youtube.com/watch?v=... veya liste linki",
        "type_label": "Medya Türü:",
        "type_video": "🎬 Yüksek Kalite Video",
        "type_audio": "🎵 Saf Ses (MP3 Audio)",
        "quality_label": "Çözünürlük / Kalite:",
        "qual_best_video": "⭐ En İyi Çözünürlük",
        "qual_best_audio": "⭐ En İyi Ses (192kbps)",
        "mode_label": "İşlem Modu:",
        "mode_playlist": "📚 Tüm Liste / Toplu",
        "mode_single": "📄 Sadece Tekli Video",
        "speed_label": "Bant Genişliği Sınırı:",
        "speed_unlimited": "🚀 Sınırsız",
        "path_label": "Kayıt Klasörü:",
        "browse_btn": "Gözat...",
        "download_btn": "İndirmeyi Başlat",
        "stop_btn": "Duraklat / İptal",
        "curr_item_label": "Mevcut Durum:",
        "waiting": "Görev bekleniyor...",
        "overall_label": "Genel İlerleme:",
        "lang_label": "Dil:",
        "settings_btn": "⚙️ Ayarlar",
        "settings_title": "Uygulama Ayarları",
        "settings_path_label": "Varsayılan İndirme Klasörü:",
        "save_settings_btn": "Ayarları Kaydet",
        "success_title": "Başarılı",
        "success_msg": "Tüm dosyalar başarıyla indirildi ve işlendi!",
        "settings_saved": "Ayarlar başarıyla kaydedildi!",
        "error_title": "Hata",
        "error_url": "Lütfen geçerli bir URL girin!",
        "error_path": "Dizin oluşturulamadı veya erişilemedi:",
        "stopped": "İşlem kullanıcı tarafından durduruldu.",
        "downloading": "İndiriliyor",
        "speed": "Hız",
        "eta": "Kalan Süре",
        "processing": "FFmpeg ile işleniyor ve birleştiriliyor...",
        "completed": "tamamlandı",
        "footer": "Designed & Developed by Mahmoud Ali • Enterprise Grade"
    }
}

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config_data = load_config()
        self.current_lang = "ar"
        self.t = TRANSLATIONS[self.current_lang]

        self.title(self.t["title"])
        self.geometry("900x780")
        self.minsize(800, 720)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # --- Top Enterprise Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="#18181b", corner_radius=0, height=80)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)
        self.header_frame.grid_columnconfigure(2, weight=0)

        self.logo_title = ctk.CTkLabel(
            self.header_frame, 
            text="⚡ " + self.t["header_title"], 
            font=("Segoe UI", 20, "bold"), 
            text_color="#f43f5e"
        )
        self.logo_title.grid(row=0, column=0, padx=25, pady=(15, 0), sticky="w")

        self.logo_sub = ctk.CTkLabel(
            self.header_frame, 
            text=self.t["header_subtitle"], 
            font=("Segoe UI", 12), 
            text_color="#a1a1aa"
        )
        self.logo_sub.grid(row=1, column=0, padx=25, pady=(0, 15), sticky="w")

        # Settings Button
        self.settings_btn = ctk.CTkButton(
            self.header_frame,
            text=self.t["settings_btn"],
            width=110,
            height=35,
            fg_color="#27272a",
            hover_color="#3f3f46",
            command=self.open_settings_window
        )
        self.settings_btn.grid(row=0, column=1, rowspan=2, padx=(0, 15), sticky="e")

        # Language Switcher in Header
        self.lang_var = ctk.StringVar(value="العربية (AR)")
        self.lang_menu = ctk.CTkOptionMenu(
            self.header_frame,
            values=["العربية (AR)", "English (EN)", "Türkçe (TR)"],
            variable=self.lang_var,
            command=self.change_language,
            width=130,
            fg_color="#27272a",
            button_color="#3f3f46",
            button_hover_color="#52525b"
        )
        self.lang_menu.grid(row=0, column=2, rowspan=2, padx=25, sticky="e")

        # --- Main Card Container ---
        self.main_card = ctk.CTkFrame(self, fg_color="#202024", corner_radius=12)
        self.main_card.grid(row=1, column=0, padx=20, pady=15, sticky="ew")
        self.main_card.grid_columnconfigure(1, weight=1)

        # 1. URL Section
        self.url_label = ctk.CTkLabel(self.main_card, text=self.t["url_label"], font=("Segoe UI", 13, "bold"))
        self.url_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.url_entry = ctk.CTkEntry(
            self.main_card, 
            placeholder_text=self.t["url_placeholder"], 
            height=40,
            font=("Segoe UI", 12),
            fg_color="#18181b",
            border_color="#3f3f46"
        )
        self.url_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")
        self.url_entry.focus()

        # 2. Options Grid (Type & Quality)
        self.type_label = ctk.CTkLabel(self.main_card, text=self.t["type_label"], font=("Segoe UI", 12))
        self.type_label.grid(row=2, column=0, padx=20, pady=8, sticky="w")
        
        self.type_var = ctk.StringVar(value=self.t["type_video"])
        self.type_menu = ctk.CTkOptionMenu(
            self.main_card, 
            values=[self.t["type_video"], self.t["type_audio"]],
            variable=self.type_var,
            command=self.on_type_change,
            height=35,
            fg_color="#18181b",
            button_color="#3f3f46"
        )
        self.type_menu.grid(row=2, column=1, padx=20, pady=8, sticky="ew")

        self.quality_label = ctk.CTkLabel(self.main_card, text=self.t["quality_label"], font=("Segoe UI", 12))
        self.quality_label.grid(row=3, column=0, padx=20, pady=8, sticky="w")

        self.quality_var = ctk.StringVar(value=self.t["qual_best_video"])
        self.quality_menu = ctk.CTkOptionMenu(
            self.main_card,
            values=[self.t["qual_best_video"], "1080p Full HD", "720p HD", "480p", "360p"],
            variable=self.quality_var,
            height=35,
            fg_color="#18181b",
            button_color="#3f3f46"
        )
        self.quality_menu.grid(row=3, column=1, padx=20, pady=8, sticky="ew")

        # 3. Advanced Options (Mode & Speed)
        self.mode_label = ctk.CTkLabel(self.main_card, text=self.t["mode_label"], font=("Segoe UI", 12))
        self.mode_label.grid(row=4, column=0, padx=20, pady=8, sticky="w")

        self.mode_var = ctk.StringVar(value=self.t["mode_playlist"])
        self.mode_menu = ctk.CTkOptionMenu(
            self.main_card,
            values=[self.t["mode_playlist"], self.t["mode_single"]],
            variable=self.mode_var,
            height=35,
            fg_color="#18181b",
            button_color="#3f3f46"
        )
        self.mode_menu.grid(row=4, column=1, padx=20, pady=8, sticky="ew")

        self.speed_label = ctk.CTkLabel(self.main_card, text=self.t["speed_label"], font=("Segoe UI", 12))
        self.speed_label.grid(row=5, column=0, padx=20, pady=8, sticky="w")

        self.speed_var = ctk.StringVar(value=self.t["speed_unlimited"])
        self.speed_menu = ctk.CTkOptionMenu(
            self.main_card,
            values=[self.t["speed_unlimited"], "500 KB/s", "1 MB/s", "2 MB/s", "5 MB/s"],
            variable=self.speed_var,
            height=35,
            fg_color="#18181b",
            button_color="#3f3f46"
        )
        self.speed_menu.grid(row=5, column=1, padx=20, pady=8, sticky="ew")

        # 4. Save Path
        self.path_label = ctk.CTkLabel(self.main_card, text=self.t["path_label"], font=("Segoe UI", 12))
        self.path_label.grid(row=6, column=0, padx=20, pady=8, sticky="w")

        self.path_sub_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.path_sub_frame.grid(row=6, column=1, padx=20, pady=8, sticky="ew")
        self.path_sub_frame.grid_columnconfigure(0, weight=1)

        self.path_entry = ctk.CTkEntry(self.path_sub_frame, height=35, fg_color="#18181b", border_color="#3f3f46")
        self.path_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.path_entry.insert(0, self.config_data.get("save_path", os.path.join(os.path.expanduser("~"), "Downloads")))

        self.browse_btn = ctk.CTkButton(
            self.path_sub_frame, 
            text=self.t["browse_btn"], 
            width=100, 
            height=35,
            fg_color="#3f3f46", 
            hover_color="#52525b",
            command=self.browse_path
        )
        self.browse_btn.grid(row=0, column=1)

        spacer = ctk.CTkLabel(self.main_card, text="", height=5)
        spacer.grid(row=7, column=0)

        # --- Action Buttons ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.download_btn = ctk.CTkButton(
            self.btn_frame, 
            text=self.t["download_btn"], 
            font=("Segoe UI", 14, "bold"), 
            height=48,
            fg_color="#10b981", 
            hover_color="#059669",
            command=self.start_download_thread
        )
        self.download_btn.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.stop_btn = ctk.CTkButton(
            self.btn_frame, 
            text=self.t["stop_btn"], 
            font=("Segoe UI", 14, "bold"), 
            height=48,
            fg_color="#ef4444", 
            hover_color="#dc2626",
            state="disabled",
            command=self.stop_download
        )
        self.stop_btn.grid(row=0, column=1, padx=(8, 0), sticky="ew")

        # --- Progress Card ---
        self.prog_card = ctk.CTkFrame(self, fg_color="#202024", corner_radius=12)
        self.prog_card.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.prog_card.grid_columnconfigure(1, weight=1)

        self.curr_label_title = ctk.CTkLabel(self.prog_card, text=self.t["curr_item_label"], font=("Segoe UI", 11, "bold"))
        self.curr_label_title.grid(row=0, column=0, padx=15, pady=(12, 2), sticky="w")

        self.curr_info_label = ctk.CTkLabel(self.prog_card, text=self.t["waiting"], font=("Segoe UI", 11), text_color="#a1a1aa")
        self.curr_info_label.grid(row=0, column=1, padx=15, pady=(12, 2), sticky="w")

        self.curr_bar = ctk.CTkProgressBar(self.prog_card, progress_color="#10b981", fg_color="#18181b")
        self.curr_bar.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="ew")
        self.curr_bar.set(0)

        self.overall_label_title = ctk.CTkLabel(self.prog_card, text=self.t["overall_label"], font=("Segoe UI", 11, "bold"))
        self.overall_label_title.grid(row=2, column=0, padx=15, pady=(2, 2), sticky="w")

        self.overall_info_label = ctk.CTkLabel(self.prog_card, text="0 / 0", font=("Segoe UI", 11), text_color="#a1a1aa")
        self.overall_info_label.grid(row=2, column=1, padx=15, pady=(2, 2), sticky="w")

        self.overall_bar = ctk.CTkProgressBar(self.prog_card, progress_color="#3b82f6", fg_color="#18181b")
        self.overall_bar.grid(row=3, column=0, columnspan=2, padx=15, pady=(0, 12), sticky="ew")
        self.overall_bar.set(0)

        # --- Console Log & Footer ---
        self.console_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.console_frame.grid(row=4, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.console_frame.grid_columnconfigure(0, weight=1)
        self.console_frame.grid_rowconfigure(0, weight=1)

        self.log_box = ctk.CTkTextbox(self.console_frame, font=("Consolas", 11), fg_color="#18181b", text_color="#d4d4d8")
        self.log_box.grid(row=0, column=0, sticky="nsew", pady=(0, 5))

        self.footer_label = ctk.CTkLabel(
            self.console_frame, 
            text=self.t["footer"], 
            font=("Segoe UI", 10), 
            text_color="#71717a"
        )
        self.footer_label.grid(row=1, column=0, sticky="e")

        self.msg_queue = queue.Queue()
        self.after(100, self.process_queue)
        self.ydl_instance = None

    def open_settings_window(self):
        settings_win = ctk.CTkToplevel(self)
        settings_win.title(self.t["settings_title"])
        settings_win.geometry("500x250")
        settings_win.resizable(False, False)
        settings_win.grab_set() # Modal window

        # Center window
        settings_win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (500 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (250 // 2)
        settings_win.geometry(f"+{x}+{y}")

        lbl = ctk.CTkLabel(settings_win, text=self.t["settings_path_label"], font=("Segoe UI", 13, "bold"))
        lbl.pack(padx=25, pady=(30, 10), anchor="w")

        frame = ctk.CTkFrame(settings_win, fg_color="transparent")
        frame.pack(padx=25, pady=5, fill="x")
        frame.grid_columnconfigure(0, weight=1)

        path_e = ctk.CTkEntry(frame, height=38, fg_color="#18181b", border_color="#3f3f46")
        path_e.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        path_e.insert(0, self.path_entry.get())

        def browse_settings():
            d = filedialog.askdirectory(parent=settings_win)
            if d:
                path_e.delete(0, tk.END)
                path_e.insert(0, d)

        b_btn = ctk.CTkButton(frame, text=self.t["browse_btn"], width=100, height=38, fg_color="#3f3f46", hover_color="#52525b", command=browse_settings)
        b_btn.grid(row=0, column=1)

        def save_and_close():
            new_path = path_e.get().strip()
            if os.path.exists(new_path):
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, new_path)
                self.config_data["save_path"] = new_path
                save_config(self.config_data)
                messagebox.showinfo(self.t["success_title"], self.t["settings_saved"], parent=settings_win)
                settings_win.destroy()
            else:
                messagebox.showerror(self.t["error_title"], "المجلد غير موجود أو غير صالح!", parent=settings_win)

        save_btn = ctk.CTkButton(settings_win, text=self.t["save_settings_btn"], font=("Segoe UI", 13, "bold"), height=42, fg_color="#10b981", hover_color="#059669", command=save_and_close)
        save_btn.pack(padx=25, pady=(20, 20), fill="x")

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
        self.logo_title.configure(text="⚡ " + self.t["header_title"])
        self.logo_sub.configure(text=self.t["header_subtitle"])
        self.settings_btn.configure(text=self.t["settings_btn"])
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
        self.speed_menu.configure(values=[self.t["speed_unlimited"], "500 KB/s", "1 MB/s", "2 MB/s", "5 MB/s"], variable=self.speed_var)

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
                self.quality_menu.configure(values=[self.t["qual_best_video"], "1080p Full HD", "720p HD", "480p", "360p"])
                self.quality_var.set(self.t["qual_best_video"])
        elif self.current_lang == "tr":
            if "Ses" in choice:
                self.quality_menu.configure(values=[self.t["qual_best_audio"], "192kbps", "128kbps"])
                self.quality_var.set(self.t["qual_best_audio"])
            else:
                self.quality_menu.configure(values=[self.t["qual_best_video"], "1080p Full HD", "720p HD", "480p", "360p"])
                self.quality_var.set(self.t["qual_best_video"])
        else:
            if "Audio" in choice:
                self.quality_menu.configure(values=[self.t["qual_best_audio"], "192kbps", "128kbps"])
                self.quality_var.set(self.t["qual_best_audio"])
            else:
                self.quality_menu.configure(values=[self.t["qual_best_video"], "1080p Full HD", "720p HD", "480p", "360p"])
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
            self.set_curr_info(f"{filename[:35]}... | {p_str_clean} | {self.t['speed']}: {speed} | {self.t['eta']}: {eta}")
            
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
    app.mainLoop() if hasattr(app, "mainLoop") else app.mainloop()
