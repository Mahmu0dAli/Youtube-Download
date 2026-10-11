<div align="center">

# 🎬 Advanced YouTube Downloader (GUI)

<p align="center">
  <b>A powerful, modern, and lightning-fast desktop application to download videos and playlists from YouTube with custom resolution, audio extraction, rate limiting, and real-time progress tracking.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/CustomTkinter-Modern%20UI-green?style=for-the-badge" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/yt--dlp-Downloader-red?style=for-the-badge&logo=youtube" alt="yt-dlp">
  <img src="https://img.shields.io/badge/Arch%20Linux-yay%20%2F%20AUR-blueviolet?style=for-the-badge&logo=archlinux&logoColor=white" alt="Arch Linux yay">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<p align="center">
  🌐 <b>Multi-Language Support:</b> English 🇺🇸 | العربية 🇸🇦 | Türkçe 🇹🇷
  <br>
  🐧 <b>Arch Linux Ready:</b> Fully compatible with <code>yay</code> & AUR!
</p>

</div>

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🎨 **Modern & Adaptive GUI** | Sleek interface built with CustomTkinter supporting system Light/Dark mode. |
| 🌍 **Multi-Language UI** | Switch instantly between **English**, **Arabic**, and **Turkish** on the fly. |
| 📥 **Single & Playlist Modes** | Download standalone videos or entire playlists with auto-folder organization. |
| 🎚️ **Resolution & Quality Selector** | Choose video quality (Best, 1080p, 720p, 480p, 360p) or convert directly to **MP3**. |
| ⚡ **Bandwidth Rate Limiting** | Restrict download speeds (500 KB/s up to 5 MB/s) to save network bandwidth. |
| ⏸️ **Pause / Cancel & Resume** | Safe stop button with built-in archive logging (`downloaded_archive.txt`) to skip downloaded files when resuming. |
| 📊 **Dual Progress Bars** | Real-time tracking for the **current file** (percentage, speed, ETA) and **overall playlist progress**. |
| 📦 **Auto-Dependency Installer** | Automatically verifies and installs required packages (`yt-dlp`, `customtkinter`, `imageio-ffmpeg`) on first startup. |
| 🔄 **Seamless FFmpeg Integration** | Automatically merges high-definition video and audio streams into `.mp4` containers. |

---

## 🐧 Arch Linux (`yay` / AUR) Installation

If you are using Arch Linux or an AUR helper like `yay`, you can install this tool directly using the provided `PKGBUILD`:

```bash
git clone https://github.com/Mahmu0dAli/Youtube-Download.git
cd Youtube-Download
makepkg -si
```
Or via AUR (once published):
```bash
yay -S youtube-download-git
```

### Prerequisites
* Ensure [Python 3.8 or higher](https://www.python.org/) is installed on your system.

### Installation & Running
1. Clone the repository or download the source files:
   ```bash
   git clone https://github.com/Mahmu0dAli/Youtube-Download.git
   cd Youtube-Download
   ```
2. Run the application:
   ```bash
   python downloader.py
   ```
   > 💡 *Note: On the first launch, the app will automatically check and install all necessary dependencies.*

---

## 📸 User Interface Overview

```text
+--------------------------------------------------------------------------+
| Language: [ العربية (AR) ▾ ]                                             |
| URL / Playlist: [ Paste YouTube link here...                         ]   |
| Type: [ Video (Video) ▾ ]           Quality: [ Best Quality (Best) ▾ ]   |
| Mode: [ Playlist / Batch ▾ ]        Speed Limit: [ Unlimited (Unlim.) ▾] |
| Save Path: [ C:/Users/.../Downloads               ] [ Browse... ]        |
|                                                                          |
| [ Start Download ]                  [ Pause / Cancel ]                   |
|                                                                          |
| Current Item: [ File name... | 45% | Speed: 2.5 MB/s | ETA: 00:12 ]      |
| [========================>               ]                               |
| Overall Progress: [ 3 / 7 completed ]                                    |
| [===========================>            ]                               |
|                                                                          |
| [ Log console output & real-time yt-dlp details...                     ] |
+--------------------------------------------------------------------------+
```

---

## 🛠️ Built With

* **[Python](https://www.python.org/)** - Core programming language.
* **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern, dark-mode compatible UI framework.
* **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Feature-rich command-line audio/video downloader.
* **[imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg)** - Standalone FFmpeg binaries wrapper.

---

## 👨‍💻 Author

**Mahmoud Ali**
* GitHub: [@Mahmu0dAli](https://github.com/Mahmu0dAli)

---

## 🏷️ Hashtags
#YouTubeDownloader #ArchLinux #AUR #yay #Python #CustomTkinter #OpenSource #VideoDownloader #FFmpeg

---

## ⭐️ Show your support

Give a ⭐️ if this project helped you!
