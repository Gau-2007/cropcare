import zipfile
from pathlib import Path

ZIP_PATH = Path.home() / "Downloads" / "archive.zip"
OUT = Path("dataset/selected")
CROPS = ("Tomato___", "Potato___")

if not ZIP_PATH.exists():
    raise SystemExit(f"Zip not found: {ZIP_PATH}")

count = 0
classes = set()
with zipfile.ZipFile(ZIP_PATH) as z:
    for info in z.infolist():
        if info.is_dir():
            continue
        parts = Path(info.filename).parts
        if "color" not in parts:
            continue
        idx = parts.index("color")
        if len(parts) < idx + 3:
            continue
        cls = parts[idx + 1]
        if not cls.startswith(CROPS):
            continue
        dest = OUT / cls
        dest.mkdir(parents=True, exist_ok=True)
        with z.open(info) as src, open(dest / parts[-1], "wb") as dst:
            dst.write(src.read())
        classes.add(cls)
        count += 1

print(f"Extracted {count} images in {len(classes)} classes")
for c in sorted(classes):
    print(" ", c)