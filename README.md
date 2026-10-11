# Advanced YouTube Downloader (GUI)

An advanced and user-friendly GUI application built with Python and CustomTkinter to download videos and playlists from YouTube in various resolutions, or convert them directly to high-quality MP3 audio.

---

## 🛠️ Key Features:
1. **Modern GUI:** Clean, responsive user interface supporting automatic Light/Dark mode via CustomTkinter.
2. **Flexible Download Modes:** Download single videos or entire playlists with automatic directory organization.
3. **Resolution & Quality Selector:** Choose your preferred video resolution (Best, 1080p, 720p, 480p, 360p) or extract audio as **MP3**.
4. **Download Rate Limiting:** Optional speed limits (from 500 KB/s up to 5 MB/s) to manage your bandwidth.
5. **Pause & Resume Support:** Safe stop/cancel button combined with automatic archive logging (`downloaded_archive.txt`) to skip already downloaded files when resuming later.
6. **Dual Progress Bars:** Real-time progress bar for the current item (speed, percentage, ETA) plus an overall playlist progress tracker.
7. **Auto-Dependency Installer:** Automatically checks and installs all required packages (`yt-dlp`, `customtkinter`, `imageio-ffmpeg`) on first launch.
8. **Automatic FFmpeg Merging:** Automatically handles video and audio stream merging into high-compatibility `.mp4` files.

---

## 🚀 How to Run:
1. Ensure [Python 3.8+](https://www.python.org/) is installed on your system.
2. Run the application script:
   ```bash
   python downloader.py
   ```
   *(On first run, the tool will automatically check and install any missing dependencies).*

---

## 🔄 Auto-Sync to GitHub:
To easily commit and push any future updates to your GitHub repository with confirmation, run:
```bash
python update_git.py
```

---

## 👨‍💻 Developed by
**Mahmoud Ali**  
GitHub: [github.com/Mahmu0dAli](https://github.com/Mahmu0dAli)
