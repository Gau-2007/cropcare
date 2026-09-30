from pathlib import Path
import random
import matplotlib.pyplot as plt
from PIL import Image

SRC = Path("dataset/selected")
EXT = {".jpg", ".jpeg", ".png"}

classes = sorted(d for d in SRC.iterdir() if d.is_dir())
files = {c.name: [p for p in c.iterdir() if p.suffix.lower() in EXT] for c in classes}

print(f"Total classes: {len(classes)}")
for name, imgs in files.items():
    print(f"{name:50s} {len(imgs)}")
print("Total images:", sum(len(v) for v in files.values()))

# Bar chart: images per class
plt.figure(figsize=(11, 6))
plt.barh(list(files.keys()), [len(v) for v in files.values()])
plt.xlabel("Number of images")
plt.title("Images per class")
plt.tight_layout()
plt.savefig("ml/class_counts.png")

# One random sample image per class
fig, axes = plt.subplots(3, 5, figsize=(14, 9))
for ax in axes.flat:
    ax.axis("off")
for ax, (name, imgs) in zip(axes.flat, files.items()):
    ax.imshow(Image.open(random.choice(imgs)))
    ax.set_title(name.replace("___", "\n")[:30], fontsize=8)
plt.tight_layout()
plt.savefig("ml/samples.png")
plt.show()