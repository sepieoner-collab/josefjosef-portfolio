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

2. **Never run git.** Every git command through the bridge creates
   `.git/index.lock` and then cannot delete it, which jams the next command.
   Write the commands out for Josef and let him run them in Terminal.

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
--type-body: max(11.5px, calc(var(--grid-square) / 10))   /* running text, captions */
--type-note: max(13px,   calc(var(--grid-square) / 8))    /* thumbnail captions */
--type-meta: max(14px,   calc(var(--grid-square) / 6.9))  /* dates, bio lines */
```

The `max()` is a readability floor that only engages on a very short window.
To resize all body text, change one number: `/ 10`. Bigger = smaller divisor
(`/ 9`, `/ 8`); smaller = larger divisor. Josef chose `/ 10` on 2 Sept, down
from `/ 9`.

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

### The project page viewer

Three invisible `<button class="zone">` elements over the picture: left steps
back, right steps forward, the middle goes fullscreen. They are real buttons so
a keyboard can reach them; all default button styling is stripped, and the
focus ring is `:focus-visible` only, so a mouse never sees it. Arrow keys and
Escape also work. Photos are `object-fit: contain` anchored
`center bottom` — landscape and portrait, page and fullscreen alike.

---

## State (2 Sept 2026)

Design is **locked and approved**. Content is mostly not uploaded.

**Carried over from the 1 Sept handover note, not yet done — do these before
anything else, they affect whether today's work is even safe:**
- Stale `.git/index.lock` may still be sitting in the repo from a jammed git
  command. Josef needs to run, in his own Terminal: `rm -f .git/index.lock`
- `_to_delete/` still has five old files parked in it (grid overlay
  component, unused placeholder graphic, three orphaned Myšina photos from
  before the numbering changed). Nothing on the site references them —
  Josef can delete that whole folder once he's glanced in it.
- The repo was **6 commits ahead of GitHub, never pushed** as of 1 Sept —
  confirm current count and push. This is the only backup of finished work
  off Josef's laptop; don't let it sit unpushed for long.
- Body text size: **answered 2 Sept** — Josef went smaller, `/ 9` → `/ 10`.
- Still open: the project description's line-height was opened from solid to
  1.35 without being asked — keep it, or put it back?

- Real: home, bio, `/architecture/mysina/` (14 photos)
- Placeholders: 13 more architecture slots, all of works / academic / stock,
  27 references
- Data layer moved from a single `projects.ts` array to one `.md` file per
  project under `src/content/projects/` (Astro content collections) — see
  "The data layer" above. Only `mysina.md` exists so far, carried over with
  no content change. **Verified in the browser 2 Sept**: 14 photos in order,
  description 2382 chars (byte-identical to the old array), 7 paragraphs,
  `white-space: pre-line` intact, body text 18.27px.
- Missing: `academic/[slug].astro` (copy `works/[slug].astro`, change one word)
- Not started: mobile layout, favicon design, meta description, share preview,
  domain `josefjosef.cz`, deployment

Deliberately deferred until all content is real: **mobile layout** (it must
react to real material) and **favicon / meta / share preview** (Josef asked to
be reminded before the site goes live).

Next: confirm the content-collections migration renders correctly, then the
upload script, then content section by section in nav order.

---

## Running it

```
cd ~/Documents/josefjosef-portfolio
npm run dev        # http://localhost:4321
```
