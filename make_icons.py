# Runs inside the GitHub Action after `cap add android`: puts the Khuraak logo into the Android project.
import glob, os, shutil
from PIL import Image, ImageDraw

RES = "android/app/src/main/res"
src = Image.open("icon-512.png").convert("RGBA")

# launcher icon: plain PNGs on every Android version
shutil.rmtree(f"{RES}/mipmap-anydpi-v26", ignore_errors=True)
for d, s in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
    p = f"{RES}/mipmap-{d}"
    os.makedirs(p, exist_ok=True)
    im = src.resize((s, s), Image.LANCZOS)
    im.save(f"{p}/ic_launcher.png")
    im.save(f"{p}/ic_launcher_round.png")

# splash screen: plain black (default is the Capacitor logo)
black = Image.new("RGB", (64, 64), (0, 0, 0))
for f in glob.glob(f"{RES}/drawable*/splash.png"):
    black.save(f)

# white-on-transparent notification icon: the K
os.makedirs(f"{RES}/drawable", exist_ok=True)
n = 96
ic = Image.new("RGBA", (n, n), (0, 0, 0, 0))
d = ImageDraw.Draw(ic)
W = (255, 255, 255, 255)
d.rectangle([24, 12, 38, 84], fill=W)
d.line([(38, 52), (68, 14)], fill=W, width=14)
d.line([(44, 46), (72, 84)], fill=W, width=14)
ic.save(f"{RES}/drawable/ic_stat_khuraak.png")
print("icons ok")
