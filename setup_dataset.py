"""Copy the Shuttlecock Trajectory Dataset into the folder layout TrackNetV3 expects.

    TrackNetV2/Professional/matchN -> data/train/matchN
    TrackNetV2/Amateur/matchN      -> data/train/match(N+23)
    TrackNetV2/Test/matchN         -> data/test/matchN

Copies, never moves: TrackNetV2/ stays as the untouched original.

Usage:
    python setup_dataset.py                 # train and test
    python setup_dataset.py --splits test   # test only (enough for evaluation)
"""
import argparse
import shutil
from pathlib import Path

SRC = Path('TrackNetV2')
DST = Path('data')
NUM_PROFESSIONAL = 23  # Amateur matches are renumbered to follow the 23 professional ones


def copy_match(src, dst):
    if dst.exists():
        print(f'skip   {dst} (already exists)')
        return
    shutil.copytree(src, dst)
    print(f'copied {src} -> {dst}')


parser = argparse.ArgumentParser()
parser.add_argument('--splits', nargs='+', choices=['train', 'test'], default=['train', 'test'])
args = parser.parse_args()

if 'train' in args.splits:
    for match in sorted((SRC / 'Professional').iterdir()):
        copy_match(match, DST / 'train' / match.name)
    for match in sorted((SRC / 'Amateur').iterdir()):
        n = int(match.name.removeprefix('match'))
        copy_match(match, DST / 'train' / f'match{n + NUM_PROFESSIONAL}')

if 'test' in args.splits:
    for match in sorted((SRC / 'Test').iterdir()):
        copy_match(match, DST / 'test' / match.name)

# preprocess.py expects train/, test/ and val/ to exist. An existing val/ also stops it from
# building its own validation set from the last rally of each training match, which leaks
# rallies from the same match into validation. We fill val/ ourselves, by whole matches.
for split in ['train', 'test', 'val']:
    (DST / split).mkdir(parents=True, exist_ok=True)
