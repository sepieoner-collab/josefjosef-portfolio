#!/usr/bin/env python3
"""
Import one project from _incoming into the website.

    python3 tools/import-project.py "Log cabin in Srdov"
    python3 tools/import-project.py "Log cabin in Srdov" --section works
    python3 tools/import-project.py "Log cabin in Srdov" --dry-run

It reads  _incoming/<folder>/  and writes
    public/projects/<slug>/          the web-sized pictures
    src/content/projects/<slug>.md   the project file

Rules it follows, all of them deliberate:

* ORDER comes from the numbers in the filenames, read as numbers — so
  "drawing2" comes before "drawing10", which sorting by name would get wrong.
* CAPTIONS come from the filenames, tidied. They are placeholders; Josef
  rewrites them. This is why naming the files sensibly is worth ten seconds:
  "20 barn interior.jpg" gives a usable caption, "photo20.jpg" does not.
* PICTURES are capped at 2400px on the long edge, saved as JPEG, colour
  profile preserved (hard rule 5). Anything with transparency is flattened
  onto the page's own grey so no white box appears.
* FILM is re-encoded to MP4 at 720 wide and given a poster frame. It plays
  muted and looping on the site — browsers refuse to autoplay sound.
* SVG is copied untouched. Vector stays vector.
* THE WALL THUMBNAIL is made at the end, by tools/make-thumbs.py, so the
  section index does not download a 900kB photograph to draw it small.
* NOTHING IS DELETED. Re-running overwrites, it never removes.
"""

import argparse, os, re, shutil, subprocess, sys, unicodedata
from PIL import Image, ImageOps

# an A0 sheet at 300dpi is ~139 megapixels; PIL's default bomb guard is 89
Image.MAX_IMAGE_PIXELS = None

MAX = 2400
PAGE_GREY = (230, 230, 230)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PICTURES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}
FILMS = {".mov", ".mp4", ".m4v", ".avi"}


def slugify(text):
    """Soňa's apartment -> sonas-apartment"""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def order_of(name):
    """the first run of digits in the name, as a number; no number sorts last.
    The name itself breaks ties, so "01.jpg" beats "drawing1.png" rather than
    the two landing in whatever order the filesystem happened to hand over."""
    m = re.search(r"\d+", name)
    return (0, int(m.group()), name.lower()) if m else (1, 0, name.lower())


def caption_of(name):
    """drawing1.png -> 'drawing 1';  '05 barn interior.jpg' -> 'barn interior'"""
    stem = os.path.splitext(name)[0]
    stem = re.sub(r"^\d+", "", stem)                 # drop the leading index
    stem = re.sub(r"(?<=[a-zA-Z])(?=\d)", " ", stem)  # drawing1 -> drawing 1
    stem = re.sub(r"[_\-]+", " ", stem)
    return re.sub(r"\s+", " ", stem).strip() or "picture"



DOC_TYPES = {".txt", ".rtf", ".md"}
FIELDS = {"project name": "name", "name": "name",
          "date": "dates", "dates": "dates",
          "role": "role",
          "project description": "description", "description": "description"}


def strip_rtf(text):
    """crude but sufficient: drop RTF control words and braces.
    \'c5 style escapes are single bytes in the document's code page — RTF from
    TextEdit is cp1252 — so they must be decoded or accented letters arrive as
    literal backslash-c-5. Å is the obvious casualty here."""
    text = re.sub(r"\\'([0-9a-fA-F]{2})",
                  lambda m: bytes([int(m.group(1), 16)]).decode("cp1252", "replace"),
                  text)
    text = re.sub(r"\\\r?\n", "\n", text)
    text = re.sub(r"\\par[d]?\b", "\n", text)
    text = re.sub(r"\{\\\*?[^{}]*\}", "", text)
    text = re.sub(r"\\[a-zA-Z]+-?\d* ?", "", text)
    return text.replace("{", "").replace("}", "")


def read_project_doc(folder):
    """Read name / date / role / description out of the one text file in the
    folder, if there is one. A 'Picture description' section is IGNORED on
    purpose: a picture's words belong in its filename, so there is only ever
    one place to change them. See UPLOADING.md."""
    docs = [f for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() in DOC_TYPES and not f.startswith(".")]
    if not docs:
        return {}
    raw = open(os.path.join(folder, docs[0]), encoding="utf-8", errors="replace").read()
    if docs[0].lower().endswith(".rtf"):
        raw = strip_rtf(raw)
    found, key = {}, None
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        label = line.rstrip(":").strip().lower()
        if line.endswith(":") and label in FIELDS:
            key = FIELDS[label]
            found.setdefault(key, [])
            continue
        if line.endswith(":"):          # any other heading ends the field
            key = None
            continue
        if key:
            found[key].append(line)
    print(f"  read {docs[0]}")
    return {k: "\n".join(v).strip() for k, v in found.items() if v}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="folder name inside _incoming/")
    ap.add_argument("--section", default="architecture",
                    choices=["architecture", "works", "academic"])
    ap.add_argument("--order", type=int,
                    help="position on the section wall; lower comes first")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src_dir = os.path.join(ROOT, "_incoming", args.folder)
    if not os.path.isdir(src_dir):
        sys.exit(f"no such folder: {src_dir}")

    slug = slugify(args.folder)
    dst_dir = os.path.join(ROOT, "public", "projects", slug)
    files = sorted((f for f in os.listdir(src_dir)
                    if not f.startswith(".") and not f.startswith("_")),
                   key=order_of)
    if not args.dry_run:
        os.makedirs(dst_dir, exist_ok=True)

    entries, tin, tout = [], 0, 0
    for i, f in enumerate(files, 1):
        ext = os.path.splitext(f)[1].lower()
        src = os.path.join(src_dir, f)
        cap = caption_of(f)
        stem = f"{i:02d}-{slugify(cap) or 'picture'}"
        tin += os.path.getsize(src)

        if ext in PICTURES:
            out = os.path.join(dst_dir, stem + ".jpg")
            if not args.dry_run:
                im = Image.open(src)
                if ext in (".jpg", ".jpeg"):
                    im.draft("RGB", (MAX, MAX))   # cheap decode for huge scans
                im = ImageOps.exif_transpose(im)
                icc = im.info.get("icc_profile")
                if im.mode in ("RGBA", "P", "LA"):
                    bg = Image.new("RGB", im.size, PAGE_GREY)
                    bg.paste(im, mask=im.split()[-1] if im.mode in ("RGBA", "LA") else None)
                    im = bg
                elif im.mode != "RGB":
                    im = im.convert("RGB")
                if max(im.size) > MAX:
                    im.thumbnail((MAX, MAX), Image.LANCZOS)
                im.save(out, "JPEG", quality=85, optimize=True, progressive=True,
                        **({"icc_profile": icc} if icc else {}))
        elif ext == ".svg":
            out = os.path.join(dst_dir, stem + ".svg")
            if not args.dry_run:
                shutil.copy2(src, out)
        elif ext in FILMS:
            out = os.path.join(dst_dir, stem + ".mp4")
            if not args.dry_run:
                subprocess.run(["ffmpeg", "-v", "error", "-i", src,
                                "-map", "0:v:0", "-map", "0:a:0?", "-vf", "scale=720:-2",
                                "-c:v", "libx264", "-crf", "28", "-preset", "slow",
                                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
                                "-movflags", "+faststart", out, "-y"], check=True)
                subprocess.run(["ffmpeg", "-v", "error", "-i", out, "-vframes", "1",
                                out[:-4] + ".jpg", "-y"], check=True)
        else:
            print(f"  skipped (unknown type): {f}")
            continue

        if not args.dry_run:
            tout += os.path.getsize(out)
        entries.append((os.path.basename(out), cap))
        print(f"  {i:02d}  {f[:42]:44s} -> {os.path.basename(out)}")

    doc = read_project_doc(src_dir)
    md = ["---", f"section: {args.section}",
          f'name: {doc.get("name", args.folder)}',
          f'dates: {doc.get("dates", "TODO")}']
    if args.order is not None:
        md.append(f"order: {args.order}")
    if doc.get("role"):
        md.append(f'role: "{doc["role"]}"')
    md.append("photos:")
    for fname, cap in entries:
        md.append(f"  - src: /projects/{slug}/{fname}")
        md.append(f'    caption: "{cap}"')
    md += ["---", "", doc.get("description", "TODO")]
    md_path = os.path.join(ROOT, "src", "content", "projects", slug + ".md")
    if not args.dry_run:
        open(md_path, "w", encoding="utf-8").write("\n".join(md) + "\n")

    if not args.dry_run:
        subprocess.run([sys.executable,
                        os.path.join(ROOT, "tools", "make-thumbs.py"), slug],
                       check=True)

    print(f"\n{len(entries)} items -> {slug}")
    print(f"{tin/1048576:.1f}M in, {tout/1048576:.1f}M out" if tout else "(dry run)")
    print(f"page: /{args.section}/{slug}/")


if __name__ == "__main__":
    main()
