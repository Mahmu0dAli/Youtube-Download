# Maintainer: Mahmoud Ali <mahmoud.ali@example.com>
pkgname=youtube-download-git
pkgver=1.0.0
pkgrel=1
pkgdesc="Advanced YouTube Downloader GUI with multi-language support, quality selector, and playlist download."
arch=('any')
url="https://github.com/Mahmu0dAli/Youtube-Download"
license=('MIT')
depends=('python' 'python-yt-dlp' 'python-imageio-ffmpeg')
makedepends=('git')
source=("$pkgname::git+$url.git")
sha256sums=('SKIP')

package() {
    cd "$srcdir/$pkgname"
    
    # Create application directory
    install -dm755 "$pkgdir/usr/share/youtube-download"
    install -m644 downloader.py "$pkgdir/usr/share/youtube-download/downloader.py"
    
    # Create executable wrapper
    install -dm755 "$pkgdir/usr/bin"
    cat << EOF > "$pkgdir/usr/bin/youtube-download"
#!/bin/bash
exec python /usr/share/youtube-download/downloader.py "\$@"
EOF
    chmod +x "$pkgdir/usr/bin/youtube-download"
    
    # Desktop entry
    install -Dm644 /dev/null "$pkgdir/usr/share/applications/youtube-download.desktop"
    cat << EOF > "$pkgdir/usr/share/applications/youtube-download.desktop"
[Desktop Entry]
Name=YouTube Download
Comment=Advanced YouTube Downloader GUI
Exec=youtube-download
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Video;Network;
EOF
}
