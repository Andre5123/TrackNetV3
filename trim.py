import os
import sys
import cv2
from tqdm import tqdm

src, dst, start_s, dur_s = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
step = int(sys.argv[5]) if len(sys.argv) > 5 else 1  # keep every step-th frame (2: 60 fps -> 30 fps)
if os.path.abspath(src) == os.path.abspath(dst):
    sys.exit("Output name must differ from the input name.")

cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
if not cap.isOpened() or fps <= 0:
    sys.exit(f"Could not read {src}; the file may be corrupted or incomplete.")

out_w, out_h = 1280, 720
cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_s * fps))
out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps / step, (out_w, out_h))
written = 0
for i in tqdm(range(int(dur_s * fps)), unit='frame'):
    ok, frame = cap.read()
    if not ok:
        break
    if i % step:
        continue
    out.write(cv2.resize(frame, (out_w, out_h), interpolation=cv2.INTER_AREA))
    written += 1
cap.release()
out.release()
print(f"Saved {dst}: {written} frames at {fps / step:.1f} fps, {out_w}x{out_h}")