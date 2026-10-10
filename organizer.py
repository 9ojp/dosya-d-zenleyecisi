#!/usr/bin/env python3
"""Dosya Düzenleyici: bir klasördeki dosyaları türlerine göre alt klasörlere ayırır."""

import argparse
import shutil
from pathlib import Path

KATEGORILER = {
    "Resimler": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Videolar": {".mp4", ".mkv", ".avi", ".mov", ".wmv"},
    "Muzikler": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
    "Belgeler": {".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Arsivler": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Kodlar": {".py", ".java", ".cpp", ".c", ".cs", ".js", ".html", ".css", ".json"},
    "Programlar": {".exe", ".msi", ".apk", ".dmg"},
}


def kategori_bul(uzanti: str) -> str:
    for ad, uzantilar in KATEGORILER.items():
        if uzanti.lower() in uzantilar:
            return ad
    return "Diger"


def benzersiz_yol(hedef: Path) -> Path:
    """Aynı isimde dosya varsa sonuna (1), (2) ... ekler."""
    if not hedef.exists():
        return hedef
    sayac = 1
    while True:
        yeni = hedef.with_name(f"{hedef.stem} ({sayac}){hedef.suffix}")
        if not yeni.exists():
            return yeni
        sayac += 1


def duzenle(klasor: Path, deneme: bool = False) -> int:
    tasinan = 0
    for dosya in klasor.iterdir():
        if not dosya.is_file() or dosya.name.startswith("."):
            continue
        hedef_klasor = klasor / kategori_bul(dosya.suffix)
        hedef = benzersiz_yol(hedef_klasor / dosya.name)
        print(f"{'[DENEME] ' if deneme else ''}{dosya.name}  ->  {hedef_klasor.name}/")
        if not deneme:
            hedef_klasor.mkdir(exist_ok=True)
            shutil.move(str(dosya), str(hedef))
        tasinan += 1
    return tasinan


def main():
    parser = argparse.ArgumentParser(description="Klasördeki dosyaları türüne göre düzenler.")
    parser.add_argument("klasor", help="Düzenlenecek klasörün yolu")
    parser.add_argument("--deneme", action="store_true", help="Dosyaları taşımadan sadece ne olacağını göster")
    args = parser.parse_args()

    klasor = Path(args.klasor).expanduser()
    if not klasor.is_dir():
        raise SystemExit(f"Klasör bulunamadı: {klasor}")

    sayi = duzenle(klasor, args.deneme)
    print(f"\nToplam {sayi} dosya {'işlenecek' if args.deneme else 'taşındı'}.")


if __name__ == "__main__":
    main()
