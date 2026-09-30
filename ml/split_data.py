from pathlib import Path
import random
import shutil

SRC = Path("dataset/selected")
OUT = Path("dataset/split")
EXT = {".jpg", ".jpeg", ".png"}
random.seed(42)

if OUT.exists():
    shutil.rmtree(OUT)

for cls in sorted(d for d in SRC.iterdir() if d.is_dir()):
    imgs = [p for p in cls.iterdir() if p.suffix.lower() in EXT]
    random.shuffle(imgs)
    n = len(imgs)
    n_train = int(n * 0.70)
    n_val = int(n * 0.15)
    parts = {
        "train": imgs[:n_train],
        "val": imgs[n_train:n_train + n_val],
        "test": imgs[n_train + n_val:],
    }
    for split, items in parts.items():
        dest = OUT / split / cls.name
        dest.mkdir(parents=True, exist_ok=True)
        for p in items:
            shutil.copy(p, dest / p.name)
    print(cls.name, {k: len(v) for k, v in parts.items()})

print("Done. Split saved in", OUT)