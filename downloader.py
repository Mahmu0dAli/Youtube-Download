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

# Config file path
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".yt_downloader_config.json")

def load_config():
    default_config = {
        "save_path": os.path.join(os.path.expanduser("~"), "Downloads"),
        "audio_codec": "mp3",
        "audio_bitrate": "192",
        "embed_meta": True,
        "embed_thumb": True,
        "download_subs": False,
        "concurrent_frags": "4",
        "theme_color": "green",
        "appearance": "Dark"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                default_config.update(data)
        except:
            pass
    return default_config

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except:
        pass

config_data = load_config()
ctk.set_appearance_mode(config_data.get("appearance", "Dark"))
ctk.set_default_color_theme(config_data.get("theme_color", "green"))

# --- Translations Dictionary ---
TRANSLATIONS = {
    "ar": {
        "title": "YouTube Downloader Pro | Enterprise Edition",
        "header_title": "مستكشف ومحمل يوتيوب الاحترافي",
        "header_subtitle": "تحميل الفيديوهات وقوائم التشغيل بأعلى كفاءة وجودة",
        "url_label": "رابط الفيديو أو قائمة التشغيل:",
        "url_placeholder": "https://www.youtube.com/watch?v=... أو رابط القائمة",
        "type_label": "النوع:",
        "type_video": "🎬 فيديو (Video)",
        "type_audio": "🎵 صوت (MP3)",
        "quality_label": "الدقة:",
        "qual_best_video": "⭐ أفضل دقة",
        "qual_best_audio": "⭐ أفضل صوت",
        "mode_label": "النمط:",
        "mode_playlist": "📚 قائمة (Playlist)",
        "mode_single": "📄 فردي (Single)",
        "speed_label": "السرعة:",
        "speed_unlimited": "🚀 غير محدود",
        "browse_btn": "تصفح...",
        "download_btn": "بدء التحميل الآن",
        "stop_btn": "إيقاف مؤقت / إلغاء",
        "curr_item_label": "الحالة الحالية:",
        "waiting": "في انتظار بدء المهمة...",
        "overall_label": "التقدم الكلي للقائمة:",
        "lang_label": "اللغة:",
        "settings_btn": "⚙️ الإعدادات المتقدمة",
        "settings_title": "الإعدادات المتقدمة (Pro Settings)",
        "settings_path_label": "المجلد الافتراضي لحفظ التحميلات:",
        "audio_codec_label": "صيغة الصوت المفضلة:",
        "audio_bitrate_label": "جودة/معدل بت الصوت:",
        "meta_thumb_label": "البيانات والملصقات:",
        "embed_meta_chk": "تضمين البيانات التعريفية (Metadata)",
        "embed_thumb_chk": "تضمين صورة الغلاف والـ Thumbnail",
        "subs_label": "الترجمة (Subtitles):",
        "download_subs_chk": "تحميل وتضمين الترجمة تلقائياً (العربية/الإنجليزية)",
        "frags_label": "التسريع متعدد المسارات (Concurrent Fragments):",
        "theme_label": "المظهر والثيم:",
        "save_settings_btn": "حفظ جميع الإعدادات",
        "success_title": "عملية ناجحة",
        "success_msg": "تم تحميل ومعالجة جميع الملفات بنجاح!",
        "settings_saved": "تم حفظ الإعدادات بنجاح! (بعض التغييرات تتطلب إعادة تشغيل الأداة)",
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
        "type_label": "Type:",
        "type_video": "🎬 Video",
        "type_audio": "🎵 Audio (MP3)",
        "quality_label": "Quality:",
        "qual_best_video": "⭐ Best",
        "qual_best_audio": "⭐ Best Audio",
        "mode_label": "Mode:",
        "mode_playlist": "📚 Playlist",
        "mode_single": "📄 Single",
        "speed_label": "Speed:",
        "speed_unlimited": "🚀 Unlimited",
        "browse_btn": "Browse...",
        "download_btn": "Start Download",
        "stop_btn": "Pause / Cancel",
        "curr_item_label": "Current Task:",
        "waiting": "Waiting for task...",
        "overall_label": "Overall Progress:",
        "lang_label": "Language:",
        "settings_btn": "⚙️ Pro Settings",
        "settings_title": "Advanced Pro Settings",
        "settings_path_label": "Default Download Directory:",
        "audio_codec_label": "Preferred Audio Format:",
        "audio_bitrate_label": "Audio Bitrate/Quality:",
        "meta_thumb_label": "Metadata & Thumbnails:",
        "embed_meta_chk": "Embed Metadata",
        "embed_thumb_chk": "Embed Thumbnail",
        "subs_label": "Subtitles:",
        "download_subs_chk": "Download and embed subtitles automatically",
        "frags_label": "Concurrent Fragments (Multi-thread speed):",
        "theme_label": "Theme & Appearance:",
        "save_settings_btn": "Save All Settings",
        "success_title": "Success",
        "success_msg": "All files downloaded and processed successfully!",
        "settings_saved": "Settings saved successfully! (Some changes require app restart)",
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
        "type_label": "Tür:",
        "type_video": "🎬 Video",
        "type_audio": "🎵 Ses (MP3)",
        "quality_label": "Kalite:",
        "qual_best_video": "⭐ En İyi",
        "qual_best_audio": "⭐ En İyi Ses",
        "mode_label": "Mod:",
        "mode_playlist": "📚 Liste",
        "mode_single": "📄 Tekli",
        "speed_label": "Hız:",
        "speed_unlimited": "🚀 Sınırsız",
        "browse_btn": "Gözat...",
        "download_btn": "İndirmeyi Başlat",
        "stop_btn": "Duraklat / İptal",
        "curr_item_label": "Mevcut Durum:",
        "waiting": "Görev bekleniyor...",
        "overall_label": "Genel İlerleme:",
        "lang_label": "Dil:",
        "settings_btn": "⚙️ Pro Ayarlar",
        "settings_title": "Gelişmiş Pro Ayarlar",
        "settings_path_label": "Varsayılan İndirme Klasörü:",
        "audio_codec_label": "Tercih Edilen Ses Formatı:",
        "audio_bitrate_label": "Ses Bitrate Kalitesi:",
        "meta_thumb_label": "Meta Veriler ve Küçük Resim:",
        "embed_meta_chk": "Meta Verileri Göm (Metadata)",
        "embed_thumb_chk": "Küçük Resmi Göm (Thumbnail)",
        "subs_label": "Altyazılar (Subtitles):",
        "download_subs_chk": "Altyazıları otomatik indir ve göm",
        "frags_label": "Eşzamanlı Parçalar (Hızlandırma):",
        "theme_label": "Tema ve Görünüm:",
        "save_settings_btn": "Tüm Ayarları Kaydet",
        "success_title": "Başarılı",
        "success_msg": "Tüm dosyalar başarıyla indirildi ve işlendi!",
        "settings_saved": "Ayarlar kaydedildi! (Bazı değişiklikler yeniden başlatma gerektirir)",
        "error_title": "Hata",
        "error_url": "Lütfen geçerli bir URL girin!",
        "error_path": "Dizin oluşturulamadı veya erişilemedi:",
        "stopped": "İşlem kullanıcı tarafından durduruldu.",
        "downloading": "İndiriliyor",
        "speed": "Hız",
        "eta": "Kalan Süre",
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
        self.geometry("850x720")
        self.minsize(750, 670)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

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
            width=140,
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
        self.main_card.grid(row=1, column=0, padx=20, pady=12, sticky="ew")
        self.main_card.grid_columnconfigure(0, weight=1)

        # 1. URL Section
        self.url_label = ctk.CTkLabel(self.main_card, text=self.t["url_label"], font=("Segoe UI", 13, "bold"))
        self.url_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.url_entry = ctk.CTkEntry(
            self.main_card, 
            placeholder_text=self.t["url_placeholder"], 
            height=38,
            font=("Segoe UI", 12),
            fg_color="#18181b",
            border_color="#3f3f46"
        )
        self.url_entry.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        self.url_entry.focus()

        # 2. Compact Options Grid (Type, Quality, Mode, Speed side-by-side)
        self.options_grid = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.options_grid.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        self.options_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Type
        self.type_label = ctk.CTkLabel(self.options_grid, text=self.t["type_label"], font=("Segoe UI", 11, "bold"))
        self.type_label.grid(row=0, column=0, padx=(0, 5), pady=(0, 2), sticky="w")
        
        self.type_var = ctk.StringVar(value=self.t["type_video"])
        self.type_menu = ctk.CTkOptionMenu(
            self.options_grid, 
            values=[self.t["type_video"], self.t["type_audio"]],
            variable=self.type_var,
            command=self.on_type_change,
            height=32,
            fg_color="#18181b",
            button_color="#3f3f46"
        )
        self.type_menu.grid(row=1, column=0, padx=(0, 8), sticky="ew")

        # Quality
        self.quality_label = ctk.CTkLabel(self.options_grid, text=self.t["quality_label"], font=("Segoe UI", 11, "bold"))
        self.quality_label.grid(row=0, column=1, padx=(5, 5), pady=(0, 2), sticky="w")

        self.quality_var = ctk.StringVar(value=self.t["qual_best_video"])
        self.quality_menu = ctk.CTkOptionMenu(
            self.options_grid,
            values=[self.t["qual_best_video"], "1080p", "720p", "480p", "360p"],
            variable=self.quality_var,
            height=32,
            fg_color="#18181b",
            button_color="#3f3f46"
        )
        self.quality_menu.grid(row=1, column=1, padx=(0, 8), sticky="ew")

        # Mode
        self.mode_label = ctk.CTkLabel(self.options_grid, text=self.t["mode_label"], font=("Segoe UI", 11, "bold"))
        self.mode_label.grid(row=0, column=2, padx=(5, 5), pady=(0, 2), sticky="w")

        self.mode_var = ctk.StringVar(value=self.t["mode_playlist"])
        self.mode_menu = ctk.CTkOptionMenu(
            self.options_grid,
            values=[self.t["mode_playlist"], self.t["mode_single"]],
            variable=self.mode_var,
            height=32,
            fg_color="#18181b",
            button_color="#3f3f46"
        )
        self.mode_menu.grid(row=1, column=2, padx=(0, 8), sticky="ew")

        # Speed
        self.speed_label = ctk.CTkLabel(self.options_grid, text=self.t["speed_label"], font=("Segoe UI", 11, "bold"))
        self.speed_label.grid(row=0, column=3, padx=(5, 0), pady=(0, 2), sticky="w")

        self.speed_var = ctk.StringVar(value=self.t["speed_unlimited"])
        self.speed_menu = ctk.CTkOptionMenu(
            self.options_grid,
            values=[self.t["speed_unlimited"], "500 KB/s", "1 MB/s", "2 MB/s", "5 MB/s"],
            variable=self.speed_var,
            height=32,
            fg_color="#18181b",
            button_color="#3f3f46"
        )
        self.speed_menu.grid(row=1, column=3, padx=(0, 0), sticky="ew")

        # --- Action Buttons ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.download_btn = ctk.CTkButton(
            self.btn_frame, 
            text=self.t["download_btn"], 
            font=("Segoe UI", 14, "bold"), 
            height=45,
            fg_color="#10b981", 
            hover_color="#059669",
            command=self.start_download_thread
        )
        self.download_btn.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.stop_btn = ctk.CTkButton(
            self.btn_frame, 
            text=self.t["stop_btn"], 
            font=("Segoe UI", 14, "bold"), 
            height=45,
            fg_color="#ef4444", 
            hover_color="#dc2626",
            state="disabled",
            command=self.stop_download
        )
        self.stop_btn.grid(row=0, column=1, padx=(8, 0), sticky="ew")

        # --- Progress Card ---
        self.prog_card = ctk.CTkFrame(self, fg_color="#202024", corner_radius=12)
        self.prog_card.grid(row=3, column=0, padx=20, pady=8, sticky="ew")
        self.prog_card.grid_columnconfigure(1, weight=1)

        self.curr_label_title = ctk.CTkLabel(self.prog_card, text=self.t["curr_item_label"], font=("Segoe UI", 11, "bold"))
        self.curr_label_title.grid(row=0, column=0, padx=15, pady=(10, 2), sticky="w")

        self.curr_info_label = ctk.CTkLabel(self.prog_card, text=self.t["waiting"], font=("Segoe UI", 11), text_color="#a1a1aa")
        self.curr_info_label.grid(row=0, column=1, padx=15, pady=(10, 2), sticky="w")

        self.curr_bar = ctk.CTkProgressBar(self.prog_card, progress_color="#10b981", fg_color="#18181b")
        self.curr_bar.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 8), sticky="ew")
        self.curr_bar.set(0)

        self.overall_label_title = ctk.CTkLabel(self.prog_card, text=self.t["overall_label"], font=("Segoe UI", 11, "bold"))
        self.overall_label_title.grid(row=2, column=0, padx=15, pady=(2, 2), sticky="w")

        self.overall_info_label = ctk.CTkLabel(self.prog_card, text="0 / 0", font=("Segoe UI", 11), text_color="#a1a1aa")
        self.overall_info_label.grid(row=2, column=1, padx=15, pady=(2, 2), sticky="w")

        self.overall_bar = ctk.CTkProgressBar(self.prog_card, progress_color="#3b82f6", fg_color="#18181b")
        self.overall_bar.grid(row=3, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="ew")
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
        settings_win.geometry("560x520")
        settings_win.resizable(False, False)
        settings_win.grab_set()

        settings_win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (560 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (520 // 2)
        settings_win.geometry(f"+{x}+{y}")

        # Scrollable frame inside settings
        scroll_frame = ctk.CTkScrollableFrame(settings_win, fg_color="transparent", width=520, height=430)
        scroll_frame.pack(padx=20, pady=15, fill="both", expand=True)

        # 1. Save Path
        lbl_path = ctk.CTkLabel(scroll_frame, text=self.t["settings_path_label"], font=("Segoe UI", 12, "bold"))
        lbl_path.pack(anchor="w", pady=(5, 5))

        path_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=(0, 15))
        path_frame.grid_columnconfigure(0, weight=1)

        path_e = ctk.CTkEntry(path_frame, height=35, fg_color="#18181b", border_color="#3f3f46")
        path_e.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        path_e.insert(0, self.config_data.get("save_path", os.path.join(os.path.expanduser("~"), "Downloads")))

        def browse_settings():
            d = filedialog.askdirectory(parent=settings_win)
            if d:
                path_e.delete(0, tk.END)
                path_e.insert(0, d)

        b_btn = ctk.CTkButton(path_frame, text=self.t["browse_btn"], width=90, height=35, fg_color="#3f3f46", hover_color="#52525b", command=browse_settings)
        b_btn.grid(row=0, column=1)

        # 2. Audio Codec & Bitrate
        audio_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        audio_frame.pack(fill="x", pady=(0, 15))
        audio_frame.grid_columnconfigure((0, 1), weight=1)

        lbl_codec = ctk.CTkLabel(audio_frame, text=self.t["audio_codec_label"], font=("Segoe UI", 12, "bold"))
        lbl_codec.grid(row=0, column=0, padx=(0, 5), sticky="w")
        codec_menu = ctk.CTkOptionMenu(audio_frame, values=["mp3", "m4a", "wav", "flac"], height=32, fg_color="#18181b", button_color="#3f3f46")
        codec_menu.grid(row=1, column=0, padx=(0, 5), pady=(5, 0), sticky="ew")
        codec_menu.set(self.config_data.get("audio_codec", "mp3"))

        lbl_bitrate = ctk.CTkLabel(audio_frame, text=self.t["audio_bitrate_label"], font=("Segoe UI", 12, "bold"))
        lbl_bitrate.grid(row=0, column=1, padx=(5, 0), sticky="w")
        bitrate_menu = ctk.CTkOptionMenu(audio_frame, values=["320", "256", "192", "128"], height=32, fg_color="#18181b", button_color="#3f3f46")
        bitrate_menu.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="ew")
        bitrate_menu.set(self.config_data.get("audio_bitrate", "192"))

        # 3. Metadata & Thumbnails
        lbl_meta = ctk.CTkLabel(scroll_frame, text=self.t["meta_thumb_label"], font=("Segoe UI", 12, "bold"))
        lbl_meta.pack(anchor="w", pady=(5, 5))

        meta_chk = ctk.CTkCheckBox(scroll_frame, text=self.t["embed_meta_chk"], font=("Segoe UI", 11))
        meta_chk.pack(anchor="w", pady=2)
        if self.config_data.get("embed_meta", True):
            meta_chk.select()

        thumb_chk = ctk.CTkCheckBox(scroll_frame, text=self.t["embed_thumb_chk"], font=("Segoe UI", 11))
        thumb_chk.pack(anchor="w", pady=(2, 15))
        if self.config_data.get("embed_thumb", True):
            thumb_chk.select()

        # 4. Subtitles
        lbl_subs = ctk.CTkLabel(scroll_frame, text=self.t["subs_label"], font=("Segoe UI", 12, "bold"))
        lbl_subs.pack(anchor="w", pady=(5, 5))

        subs_chk = ctk.CTkCheckBox(scroll_frame, text=self.t["download_subs_chk"], font=("Segoe UI", 11))
        subs_chk.pack(anchor="w", pady=(2, 15))
        if self.config_data.get("download_subs", False):
            subs_chk.select()

        # 5. Concurrent Fragments & Theme
        adv_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        adv_frame.pack(fill="x", pady=(0, 15))
        adv_frame.grid_columnconfigure((0, 1), weight=1)

        lbl_frags = ctk.CTkLabel(adv_frame, text=self.t["frags_label"], font=("Segoe UI", 12, "bold"))
        lbl_frags.grid(row=0, column=0, padx=(0, 5), sticky="w")
        frags_menu = ctk.CTkOptionMenu(adv_frame, values=["1", "2", "4", "8", "16"], height=32, fg_color="#18181b", button_color="#3f3f46")
        frags_menu.grid(row=1, column=0, padx=(0, 5), pady=(5, 0), sticky="ew")
        frags_menu.set(str(self.config_data.get("concurrent_frags", "4")))

        lbl_theme = ctk.CTkLabel(adv_frame, text=self.t["theme_label"], font=("Segoe UI", 12, "bold"))
        lbl_theme.grid(row=0, column=1, padx=(5, 0), sticky="w")
        theme_menu = ctk.CTkOptionMenu(adv_frame, values=["green", "blue", "dark-blue"], height=32, fg_color="#18181b", button_color="#3f3f46")
        theme_menu.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="ew")
        theme_menu.set(self.config_data.get("theme_color", "green"))

        def save_and_close():
            new_path = path_e.get().strip()
            if os.path.exists(new_path):
                self.config_data["save_path"] = new_path
                self.config_data["audio_codec"] = codec_menu.get()
                self.config_data["audio_bitrate"] = bitrate_menu.get()
                self.config_data["embed_meta"] = bool(meta_chk.get())
                self.config_data["embed_thumb"] = bool(thumb_chk.get())
                self.config_data["download_subs"] = bool(subs_chk.get())
                self.config_data["concurrent_frags"] = frags_menu.get()
                self.config_data["theme_color"] = theme_menu.get()
                
                save_config(self.config_data)
                messagebox.showinfo(self.t["success_title"], self.t["settings_saved"], parent=settings_win)
                settings_win.destroy()
            else:
                messagebox.showerror(self.t["error_title"], "المجلد غير موجود أو غير صالح!", parent=settings_win)

        save_btn = ctk.CTkButton(settings_win, text=self.t["save_settings_btn"], font=("Segoe UI", 13, "bold"), height=42, fg_color="#10b981", hover_color="#059669", command=save_and_close)
        save_btn.pack(padx=20, pady=(0, 15), fill="x")

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
        self.speed_menu.configure(values=[self.t["speed_unlimited"], "500 KB/s", "1 MB/s", "2 MB/s", "5 MB/s"])
        self.speed_var.set(self.t["speed_unlimited"])

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

        save_path = self.config_data.get("save_path", os.path.join(os.path.expanduser("~"), "Downloads"))
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
                'concurrent_fragment_downloads': int(self.config_data.get("concurrent_frags", 4)),
            }

            # Subtitles
            if self.config_data.get("download_subs", False):
                ydl_opts['writesubtitles'] = True
                ydl_opts['writeautomaticsub'] = True
                ydl_opts['subtitleslangs'] = ['ar', 'en']
                ydl_opts['embedsubtitles'] = True

            # Mode
            if "Single" in mode or "فردي" in mode or "Tekli" in mode:
                ydl_opts['extract_flat'] = False
                ydl_opts['noplaylist'] = True
                self.log("Download mode: Single video")
            else:
                ydl_opts['noplaylist'] = False
                self.log("Download mode: Playlist / Batch")

            # Speed limit
            if "500 KB" in speed_limit:
                ydl_opts['ratelimit'] = 500 * 1024
            elif "1 MB" in speed_limit:
                ydl_opts['ratelimit'] = 1024 * 1024
            elif "2 MB" in speed_limit:
                ydl_opts['ratelimit'] = 2 * 1024 * 1024
            elif "5 MB" in speed_limit:
                ydl_opts['ratelimit'] = 5 * 1024 * 1024

            # Type & Quality
            audio_codec = self.config_data.get("audio_codec", "mp3")
            audio_bitrate = self.config_data.get("audio_bitrate", "192")

            if "صوت" in download_type or "Audio" in download_type or "Ses" in download_type:
                ydl_opts['format'] = 'bestaudio/best'
                postproc = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_codec,
                    'preferredquality': audio_bitrate,
                }]
                if self.config_data.get("embed_meta", True):
                    postproc.append({'key': 'FFmpegMetadata'})
                if self.config_data.get("embed_thumb", True):
                    ydl_opts['writethumbnail'] = True
                    postproc.append({'key': 'EmbedThumbnail'})
                
                ydl_opts['postprocessors'] = postproc
                self.log(f"Download settings: Audio only ({audio_codec} @ {audio_bitrate}kbps)")
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
                
                v_postproc = []
                if self.config_data.get("embed_meta", True):
                    v_postproc.append({'key': 'FFmpegMetadata'})
                if v_postproc:
                    ydl_opts['postprocessors'] = v_postproc

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
