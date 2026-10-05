# josefjosef — portfolio site

A personal portfolio for Josef Kučera's solo practice **josefjosef** (one word).
Architect, carpenter, builder. Prague. Site language: English.

The whole site is one idea: **an 8 × 5 modular grid, and nothing that isn't
derived from it.** Dieter Rams / Swiss design character — "bringing order to
complexity, not only removing things". Image-heavy, quiet, low-maintenance.

Josef is not a programmer and does not use a code editor. He must stay able to
understand and maintain this site himself. **Prefer the simple, explainable
solution over the clever one, every time.** Comment the code so he can read it.

---

## Hard rules — read before touching anything

1. **ALL CSS goes in `src/styles/global.css`.** Never write a `<style>` block
   inside an `.astro` component. Astro caches per-component styles and, because
   edits arrive over the Cowork device bridge, macOS never fires a file-change
   event, so Vite never invalidates its cache and serves *stale CSS* while the
   file on disk is correct. `vite.server.watch.usePolling` does not fix it.
   `global.css` updates live. This cost hours once; do not rediscover it.

2. **Never run git. Not even `git status`.** Every git command through the
   bridge creates `.git/index.lock` and then cannot delete it, which jams the
   next command Josef runs. `git log` is safe because it does not touch the
   index; `status`, `add`, `commit` and `diff` are not. Broken again 5 Oct by
   running `git status` to "just have a look" — it cost Josef a line of
   typing. To see what changed, read the files; to see what is untracked,
   `find`. Write every git command out for Josef and let him run it.

3. **No delete permission** on the connected folder. `rm` fails with
   "Operation not permitted". To remove something, `mv` it into `_to_delete/`
   and tell Josef to delete that folder himself. Never request broader folder
   access — he asked for `josefjosef-portfolio` only, and that stands.

4. **Verify, never assert.** Claiming work was done without looking has burned
   trust here twice. Check the real page in the browser with
   `getComputedStyle`, measure numbers, then report. "It should now be X" is
   not acceptable; "measured X, was Y" is.

5. **Preserve ICC colour profiles** when processing photos. PIL drops them
   silently, which flattens wide-gamut colour in the browser. Always pass
   `icc_profile=` on save, and `ImageOps.exif_transpose()` before anything.

6. **`npm run dev` / `npm run build` cannot run through the device bridge.**
   Cowork's shell (`device_bash`) is a separate Linux VM on Josef's Mac — a
   different machine from the one his own Terminal runs on. It has no route
   to the npm registry, and the arm64-linux native binary Vite's bundler
   (rolldown) needs was never installed there — only the darwin-arm64 one
   Josef's own `npm install` produced lives in `node_modules`. Don't try to
   fix this by reinstalling packages from the bridge; there's no network to
   do it with, and it isn't broken — it's just the wrong machine. To verify a
   change: ask Josef to run `npm run dev` in his own Terminal (or confirm
   it's already running), then check the real page with the browser tool,
   which reaches his machine directly, not the bridge's Linux VM.

7. **Astro 7's dev server is a BACKGROUND DAEMON. Ctrl+C does not stop it.**
   It is tracked by a lock file, keeps running after the terminal window is
   closed or interrupted, and a plain `npm run dev` then refuses to start
   with "Another astro dev server is already running". The consequence that
   cost an hour: a daemon started before a file existed keeps serving a
   stale config forever — a new `src/content.config.ts` is invisible to it,
   `getCollection()` returns nothing, and project routes 404 while the rest
   of the site looks perfectly fine. Symptom to recognise: the terminal says
   `The collection "..." does not exist or is empty`, and no
   `.astro/data-store.json` exists on disk. The fix, which both replaces the
   daemon and clears the content-layer cache:

   ```
   npm run dev -- --force
   ```

   If that alone doesn't take (the old process ignores the lock), kill it at
   the OS level first — this is what actually worked on 2 Sept:

   ```
   pkill -f "astro dev"
   npm run dev -- --force
   ```

   A good start prints `[content] Syncing content` / `[content] Synced
   content`. If those two lines are missing, the collection is not loaded and
   project pages will 404 no matter what the files say. **Any change to
   `content.config.ts`, and any new collection, needs this** — an ordinary
   restart is not enough.

---

## How Josef works (this method works — keep using it)

**Importing a project is one command, not a conversation.**
`python3 tools/import-project.py "<folder in _incoming>" [--section works]`.
It sizes the pictures, keeps colour profiles, flattens transparency onto the
page grey, converts film to muted MP4 with a poster, copies SVG untouched,
orders by the numbers in the filenames read AS numbers, and writes the `.md`.
Read the file — it is commented and explains every rule it follows. It
finishes by calling `tools/make-thumbs.py`, which writes the small copy the
section wall uses. If a wall picture ever changes — Josef reorders the
pictures and a different one lands first — run `python3 tools/make-thumbs.py
<slug>` and the wall catches up. Forgetting it is not fatal: the data layer
checks whether the thumbnail is there and quietly falls back to the full
picture.

**A picture's words live in its filename, nowhere else** (settled 3 Sept).
`NN words about it.jpg` — the number orders, the words become the caption and
the alt text. The folder's text file carries only the project's name, date,
role and description; if it also lists pictures by number, IGNORE that list
and say why. Josef tried it once and the numbers did not line up with the
pictures, which is the whole argument against a second place to store a name.

**Do not write captions by looking at the pictures.** Josef asked for this on
3 Sept: captions come from the filenames and he replaces them with real words
later. Inventing descriptions gives him more to check, not less, and there
are many projects still to come. Same for descriptions and role lines — leave
them as TODO unless he supplies the words.

**Illustrator `.svgz` can be far too heavy to serve as vector, and the right
fix is to ask Josef for a JPEG.** Ny-Ålesund's A0 sheets decompress to 45 MB
with **half a million `<line>` elements** each — seven times the sauna
floorplan, which was already the limit. Rasterising is unavoidable, and
**his own export beats anything we can render**: A0 at 300dpi (14032 × 9922)
downscaled to 2400 averages the hairlines into visible grey, where rendering
straight to 2400 drops them and the sheet goes faint. So: ask, don't render.

If you ever must render one yourself, know that the device VM has **no working
SVG renderer** — ImageMagick's built-in one silently returns a blank white
page (mean=255), and rsvg-convert, inkscape and cairosvg are all absent. Only
Chromium in the cloud container can do it (Playwright is installed there).

Two things make huge exports cheap to process, both already in the importer:
`Image.MAX_IMAGE_PIXELS = None` (PIL refuses >89 MP as a "decompression bomb";
A0 at 300dpi is 139 MP) and `im.draft()` before resizing, which lets libjpeg
decode at 1/4 size — 30 MB of A0 sheets processed in 2.6 seconds.

**White backgrounds on drawings are deliberate.** Matching a render to the
page grey (230,230,230) looks good and he knows how; it is time-consuming and
not always wanted. Stop offering it.

He draws a measured sketch in ArchiCAD and exports it as a **16:9 PDF with real
vector lines and real text**. Extract the exact geometry with `pdfplumber`,
build to those measurements, then verify in the browser. Do not eyeball it, and
do not guess a constant — measure it.

He works **incrementally** and reviews each stage. Ask before redesigning
something he already approved. If a change is worth making but he didn't ask
for it, make it and say so plainly so he can veto.

---

## The grid

8 columns × 5 rows of true squares.

```
gutter = square / 4          margin = gutter (one gutter all round)
across = 8 + 9/4  = 10.25 squares
down   = 5 + 6/4  =  6.5  squares
```

The grid keeps its proportion and scales to be as large as it fits, centred.
It is fitted as if the screen were **half a gutter smaller on every side**
(10.5 across, 6.75 down), which is where the outer breathing room comes from.

```css
--grid-square: min(calc(100vw / 10.5), calc(100vh / 6.75));
```

On a 16:9 screen the height runs out first, so **type size is governed by the
window height**. A short window makes everything small — this is why the type
scale has a floor.

### Type

Every size is a plain fraction of one square. Named in `:root`:

```css
--type-nav-ratio:  0.172
--type-body-ratio: calc(var(--type-nav-ratio) * 2 / 3)
--type-nav:  calc(var(--grid-square) * var(--type-nav-ratio))   /* nav labels */
--type-body: calc(var(--grid-square) * var(--type-body-ratio))  /* running text */
--type-note: calc(var(--grid-square) / 8)      /* thumbnail captions */
--type-meta: calc(var(--grid-square) / 6.9)    /* dates */
```

Running text — the CV, project descriptions, photo captions — is **two
thirds of the nav label**, at weight 300, and they are all one size and one
weight. Settled 2 Sept. It is written against the nav ratio rather than as
its own decimal so the relationship survives: change the nav and the running
text follows. There are **no px floors** on the type any more — a floor breaks
the fixed ratio. The grid floor below does that job instead.

**Type stays grid-derived. Do not pin it to a fixed pt or px size.** Tried on
2 Sept and reverted the same hour: with fixed type and a shrinking grid, text
outgrows its column, and the bio's longest CV row wrapped below a 1472 × 946
window — larger than the laptop it is written on.

### The floor, and scrolling

The page stops shrinking when the smallest text on the site — the running
text — would fall below **8pt**, and the window scrolls from there:

```css
--grid-square-min: calc(8pt / var(--type-body-ratio));   /* ≈ 93px */
--grid-square: max(var(--grid-square-min), min(100vw / 10.5, 100vh / 6.75));
```

93px of square is a window of roughly **977 × 628**. Measured at that square,
running text lands on exactly 8.00pt and the nav on 12pt.

Two things make the scrolling work, and both are load-bearing:

- `body` is `width: max-content; min-width: 100%` and `position: relative`,
  so the document is as wide as the grid when the grid outgrows the window.
- **`.site-header` is `position: absolute`, not `fixed`.** Fixed would pin the
  wordmark and nav to the window while the content scrolled away underneath,
  breaking the one rule the whole site rests on — that everything sits on the
  same grid. Verified by scrolling: content and wordmark move together, to
  the same pixel.

Font: **Helvetica LT Pro** via Adobe Fonts (Typekit kit `lhb7wgk`), loaded in
`Layout.astro`. Weights 300 / 400 / 700 plus italics. It contains **no arrow or
symbol glyphs** — verified by measuring glyph widths — which is why the viewer's
arrows and fullscreen marks are hand-drawn SVG cursors.

### Text sits on the line by its INK, not its baseline

Josef's grid lines are boundaries the ink must not cross. Every nav label
starts with `_`, which sits *below* the baseline (0.125em). Measured with
canvas `actualBoundingBoxDescent`: wordmark `j` 0.214em, tagline `p` 0.207em.
Alignment offsets are therefore negative. `--descender: 0.21em`,
`--ink-spill: 0.07em`.

### Colour

```
--bg: #e6e6e6      ~10% black
--fg: #3a3a3a      ~77% black, never pure black
--fg-muted: #767676
```

---

## Structure

```
src/layouts/Layout.astro       shell: head, wordmark, tagline, 6 nav lines, slot
src/styles/global.css          every rule on the site
src/components/ProjectIndex.astro   thumbnail wall, shared by 4 sections
src/content.config.ts          defines the "projects" content collection
src/content/projects/*.md      one file per project — the actual content
src/data/projects.ts           reads the collection, shapes it for the pages
src/pages/
  index.astro       /            wordmark + cover photo
  404.astro
  bio.astro         /bio/        own layout
  architecture/     index.astro + [slug].astro
  works/            index.astro + [slug].astro
  academic/         index.astro          ← [slug].astro still to write
  stock/            index.astro          (adds sold / availability)
  references/       index.astro          own layout, 3 scrolling columns
public/             served at the site root
```

Nav order: bio, architecture, works, academic, stock, references.

### The order projects appear in

`order:` in the frontmatter, a plain number — lower comes first. Projects
without one fall to the end of their section, alphabetically, so an unnumbered
project can never jump the queue. `bySection()` does the sorting; the section
index pages just render what it returns. The importer writes it from
`--order N`.

A number is a *position among the real projects*, not a tile on the wall: with
only `order: 2` present, that project sits in the first tile until an
`order: 1` arrives and displaces it.

**All four section walls (architecture, works, academic) read real projects**
now — `academic` and `works` were still hard-coded placeholder grids until
5 Sept.

### The data layer

Each project is one file: `src/content/projects/<slug>.md`. Frontmatter holds
the structured fields; the text below `---` is the description — one blank
line between paragraphs, since `.proj-about` renders it with
`white-space: pre-line`.

```yaml
---
section: architecture   # architecture | works | academic
name: RD Myšina
dates: 07/2021 - 08/2026
photos:
  - src: /projects/mysina/01-approach.jpg
    caption: "from the road, the old neighbour behind"
related: [some-other-slug]   # optional — named on one side only, see below
---
First paragraph of the description.

Second paragraph.
```

`src/content.config.ts` defines the schema (`section`, `name`, `dates`,
`photos`, `related`) — Astro validates every file against it, so a typo'd
field name fails the build instead of silently doing nothing.
`src/data/projects.ts` reads the whole collection once and exposes the same
`projects` array / `bySection()` / `relatedTo()` functions the page files
already import — so **adding a project is only ever adding one `.md` file.**
Nothing under `src/pages/` needs to change.

`relatedTo()` reads `related` **bidirectionally** — naming a project on one
side links both. Photos are numbered `01-`…`14-` so the filename carries the
viewing order. **Each caption is also the photo's alt text** — one string, two
jobs; write it as a plain description of what is in the frame.

### The right-hand column (measured from the 2 Sept sketch)

```
row 2-4   .proj-about    the project description, top-aligned
row 4     .proj-related  "see also", at the foot of the description
row 5     .proj-role     how Josef was involved — TOP of row 5
row 5     .proj-caption  the photo caption — BOTTOM of row 5
```

`.proj-about` and `.proj-role` are set out identically (line-height 1.35,
top-aligned, no transform); `.proj-caption` keeps line-height 1 and the
descender transform, because it sits its ink on the row's bottom line.
**Don't "unify" the caption's line-height with the other two** — extra leading
on a bottom-aligned single line pushes its baseline off the grid.

The three `[slug].astro` files (architecture, works, academic) are byte-for-byte
identical apart from the section name. Change one, change all three.

### The project page viewer

Three invisible `<button class="zone">` elements over the picture: left steps
back, right steps forward, the middle goes fullscreen. They are real buttons so
a keyboard can reach them; all default button styling is stripped, and the
focus ring is `:focus-visible` only, so a mouse never sees it. Arrow keys and
Escape also work. **Clicking the project's name returns you to the first
picture** — it is a real `<button>` with every default stripped, so it still
reads as plain text; `justify-self: start` keeps the hit area on the words
rather than the whole column. Photos are `object-fit: contain` anchored
`center bottom` — landscape and portrait, page and fullscreen alike.

A **film** is just another entry in `photos:` whose src ends `.mp4`; the
viewer swaps a `<video>` in for the `<img>`. It autoplays **muted** and loops,
because browsers will not autoplay audible media — so it reads as a moving
photograph. Its poster is the same filename with `.jpg`. Only the viewer you
are actually looking at plays; the other is paused.

---

## State (10 Sept 2026)

Design is **locked and approved**. Nothing is deployed yet; there is no live
site and no email on the domain.

**`ROADMAP.md` is the list of what remains — read it before planning
anything.** Do not keep a second copy of that list here; one place only.

Built and working:
- home, bio, 404
- the project page: viewer with keyboard and click zones, fullscreen, film
  support, the name as a button back to the first picture
- section walls for architecture, works and academic read real projects and
  sort on `order:`
- `tools/import-project.py` — one command per project
- `tools/make-thumbs.py` — the wall-sized copy of each project's first
  picture; the importer runs it, so it is normally never run by hand
- references and stock walls are still placeholder grids

Real content, five projects:
- `/architecture/mysina/` (14) — complete except a `role:` line
- `/architecture/sauna-in-caravan/` (21, includes a film) — **needs dates,
  role, description, and a decision: architecture or works?**
- `/architecture/sonas-apartment/` (17) — **needs dates, role, description**
- `/architecture/srdov-rural-dwelling/` (30) — text is Josef's; **25 of 30
  pictures have no caption** until their files are renamed
- `/academic/ny-alesund/` (11, `order: 2`) — complete

Known and measured, not yet fixed:
- **Section walls download full-size photographs for 254px thumbnails.**
  4.66 MB for four projects; about 16.3 MB per wall at fourteen. The importer
  should make thumbnails. Measured 10 Sept.
- The site sets **no cookies and uses no localStorage**; the only third-party
  request is Adobe Fonts. Measured 10 Sept. Worth protecting — it means no
  consent banner is needed.

---

## Running it

```
cd ~/Documents/josefjosef-portfolio
npm run dev        # http://localhost:4321
```

**Whenever Josef has to use the Terminal, spell it out** — which window, and
that commands go one line at a time with Enter after each. He asked for this
explicitly on 2 Sept. Never just paste a block of commands and assume the
mechanics are obvious.

Use a **second** Terminal window for everything else. Commands typed into the
window running the dev server are never executed — they sit in its input and
look like they worked. This wasted a whole cycle on 2 Sept: a
`rm -f .git/index.lock` typed there did nothing, and the lock jammed every
git command for hours afterwards.

## Saving work (Josef runs these; see hard rule 2)

Repo: `github.com/sepieoner-collab/josefjosef-portfolio`, branch `main`.

```
cd ~/Documents/josefjosef-portfolio
rm -f .git/index.lock     # only if git complains the lock exists
git add -A
git commit -m "what changed, in plain words"
git push origin main
```

The lock file keeps coming back because a Claude session tried to run git.
Deleting it is safe as long as no git command is genuinely running.
