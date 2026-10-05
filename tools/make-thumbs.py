#!/usr/bin/env python3
"""
Make the small pictures the section walls use.

    python3 tools/make-thumbs.py            every project
    python3 tools/make-thumbs.py mysina     one project
    python3 tools/make-thumbs.py --force    rebuild even if up to date
    python3 tools/make-thumbs.py --all      every picture, not just the wall one

Why this exists: a wall of fourteen projects was downloading fourteen
full-size photographs (2000x1500, ~350kB each) to draw them at about 410
pixels square. That is roughly sixteen megabytes to show a page of
thumbnails. These are the same pictures at 800 on the SHORT edge, which is
still sharp on a retina screen at that size, and about a tenth of the weight.

    public/projects/<slug>/01-approach.jpg
    public/projects/<slug>/thumbs/01-approach.jpg     <- written here

Deliberate choices:

* SHORT edge, not long: the wall crops to a square (object-fit: cover), so
  it is the short edge that has to carry the detail. No cropping happens
  here - the crop stays in CSS, where it can still be changed.
* The long edge is capped as well, so a panorama cannot produce a monster.
* Colour profile preserved (hard rule 5).
* Same filename, always .jpg. src/data/projects.ts looks for the thumb and
  silently uses the full picture if it is not there, so a missing thumb
  costs bandwidth, never a broken image.
* ONLY THE WALL PICTURE, which is the first one in the project file. The
  other nineteen pictures in a project are never shown small anywhere, so a
  thumbnail of them would be weight in the repository doing nothing. Forty
  projects times twenty pictures would have been a hundred megabytes of
  files no page ever asks for. --all overrides this if that day comes.
* NOTHING IS DELETED. Re-running overwrites, it never removes.
"""

import argparse, os, re, sys
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

SHORT = 800          # the short edge of the thumbnail
LONG = 1600          # ...but never longer than this
QUALITY = 78
SOURCES = {".jpg", ".jpeg", ".png"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS = os.path.join(ROOT, "public", "projects")
CONTENT = os.path.join(ROOT, "src", "content", "projects")


def wall_picture(slug):
    """the first 'src:' in the project file - the one the section wall draws.
    Returns a bare filename, or None if there is no project file yet."""
    md = os.path.join(CONTENT, slug + ".md")
    if not os.path.exists(md):
        return None
    m = re.search(r"^\s*-\s*src:\s*(\S+)", open(md, encoding="utf-8").read(), re.M)
    return os.path.basename(m.group(1)) if m else None


def thumb_size(w, h):
    """scale so the short edge is SHORT, then pull back if the long edge
    overshoots LONG. Never scales a small picture up."""
    scale = SHORT / min(w, h)
    if max(w, h) * scale > LONG:
        scale = LONG / max(w, h)
    return (max(1, round(w * scale)), max(1, round(h * scale))) if scale < 1 else (w, h)


def make_one(src, dst, force=False):
    """returns (bytes_in, bytes_out) or None if there was nothing to do"""
    if not force and os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return None
    im = Image.open(src)
    if os.path.splitext(src)[1].lower() in (".jpg", ".jpeg"):
        im.draft("RGB", (LONG, LONG))
    im = ImageOps.exif_transpose(im)
    icc = im.info.get("icc_profile")
    if im.mode != "RGB":
        im = im.convert("RGB")
    size = thumb_size(*im.size)
    if size != im.size:
        im = im.resize(size, Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "JPEG", quality=QUALITY, optimize=True, progressive=True,
            **({"icc_profile": icc} if icc else {}))
    return os.path.getsize(src), os.path.getsize(dst)


def run(slugs=None, force=False, every=False):
    if not os.path.isdir(PROJECTS):
        sys.exit(f"no such folder: {PROJECTS}")
    todo = sorted(slugs) if slugs else sorted(
        d for d in os.listdir(PROJECTS) if os.path.isdir(os.path.join(PROJECTS, d)))
    made = skipped = tin = tout = 0
    for slug in todo:
        folder = os.path.join(PROJECTS, slug)
        if not os.path.isdir(folder):
            print(f"{slug}: no such project, skipped")
            continue
        wanted = None if every else wall_picture(slug)
        if not every and wanted is None:
            print(f"{slug}: no project file yet, skipped")
            continue
        print(slug)
        for f in sorted(os.listdir(folder)):
            if f.startswith(".") or os.path.splitext(f)[1].lower() not in SOURCES:
                continue
            if wanted is not None and f != wanted:
                continue
            src = os.path.join(folder, f)
            dst = os.path.join(folder, "thumbs", os.path.splitext(f)[0] + ".jpg")
            result = make_one(src, dst, force)
            if result is None:
                skipped += 1
                continue
            made += 1
            tin += result[0]
            tout += result[1]
            print(f"  {f[:40]:42s} {result[0]//1024:5d}kB -> {result[1]//1024:4d}kB")
    print(f"\n{made} made, {skipped} already up to date")
    if made:
        print(f"{tin/1048576:.1f}M -> {tout/1048576:.1f}M "
              f"({100 - tout * 100 // tin}% smaller)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*", help="project slugs; none means all of them")
    ap.add_argument("--force", action="store_true", help="rebuild up-to-date thumbnails")
    ap.add_argument("--all", action="store_true", dest="every",
                    help="every picture, not only the one on the wall")
    a = ap.parse_args()
    run(a.slugs or None, a.force, a.every)
