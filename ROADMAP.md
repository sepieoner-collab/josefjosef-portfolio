# What is left, in order

`CLAUDE.md` holds the house rules and how the site is built.
`UPLOADING.md` holds how to add a project.
**This file is the only list of what still has to happen.** Keep it here, not
in a chat you would have to find again.

Phases run roughly in order, but 1 and 2 can happen in any order and at any
pace. Nothing before phase 5 can break anything that is already live, because
nothing is live yet.

---

## 0. First thing, before anything else

- [x] **Committed, 5 Oct.** Two commits: `fd05633` (Srdov, Ny-Ålesund,
      ordering, the importer, the roadmap) and `7c9e589` (wall thumbnails).
- [ ] **PUSH IS STUCK.** GitHub is still on `2951b93`; both commits are on
      the laptop only. Three attempts on 5 Oct over a hotspot, all the same
      shape: the 27 MiB pack uploads, then the connection dies waiting for
      GitHub to answer (`RPC failed; HTTP 408`, then `curl 52 Recv failure`).
      Already set, and they did not save it: `http.version HTTP/1.1`,
      `http.postBuffer 524288000`, `http.lowSpeedLimit 0`,
      `http.lowSpeedTime 999999`.
      **First thing to try: the same push from a proper wifi connection.**
      It is a transport problem, not a repository problem — nothing is
      damaged and nothing is lost.
      If good wifi does not fix it, switch the remote from HTTPS to SSH,
      which does not have this failure mode. That is a ten-minute job:
      generate a key, paste the public half into GitHub, change the remote
      URL. Do it once and the problem is gone for good.

- [ ] **Get the photographs out of git — this is now urgent, not Phase 5.**
      Five projects already make a 27 MiB push impossible on a weak line.
      Forty will make it roughly 400 MB, which is unworkable for pushing,
      cloning and for Cloudflare Pages' build limits. The options to weigh,
      in rough order of sanity: keep only the web-sized pictures in git and
      the originals outside it (already the case — `_incoming/` is ignored);
      Git LFS; or an image host the site points at. Decide before project
      ten, not project forty.

---

## 1. Finish the projects already uploaded

- [ ] **sauna-in-caravan** — dates, role, description still say TODO
- [ ] **sauna-in-caravan** — decide: does it belong in *architecture* or
      *works*? It is as much carpentry as architecture. One word to change.
- [ ] **sonas-apartment** — dates, role, description still say TODO
- [ ] **srdov-rural-dwelling** — 25 of its 30 pictures have no caption.
      Rename the picture files and they get one (see UPLOADING.md).
- [ ] **mysina** — has no `role:` line
- [ ] Decide the `order:` numbers for the architecture wall

## 2. The remaining projects (about 35)

- [ ] Upload them — one command each, see UPLOADING.md
- [ ] **works** — nothing real in it yet
- [ ] **academic** — Ny-Ålesund is number 2; number 1 does not exist yet
- [ ] **references** — drop the pictures in; the filename becomes the alt
      text and the column heights are measured automatically. No text file.
- [ ] **stock — NOT BUILT YET.** It needs a different shape from a project:
      an item name, availability, and a sold state, and probably no page of
      its own. Decide what it should do, then it has to be built.

## 3. Performance, before going live

- [x] **Thumbnails. Done 5 Oct.** The walls were downloading full-size
      photographs to draw them at about 410 pixels: 4.66 MB for four
      projects, 16.3 MB per wall at fourteen. `tools/make-thumbs.py` now
      writes an 800px copy of each project's FIRST picture into
      `public/projects/<slug>/thumbs/`, the importer runs it, and the wall
      uses it. Four projects now weigh **0.6 MB instead of 4.66** — about
      **2.1 MB per wall at fourteen**, an 87% cut. Only the wall picture gets
      a thumbnail: forty projects times twenty would have been 100 MB of
      files no page ever asks for. The wall images are lazy-loaded too.
- [ ] Check what a project page weighs on a phone connection

## 4. The missing furniture

Josef asked to be reminded of these before launch, and they are all small.

All five done 5 Oct.

- [x] **favicon** — `public/favicon.svg`, page grey square, ink grey `jj`
      filling 88% of it. The letters are outlined paths, not `<text>`, so the
      shape does not depend on the viewer having Helvetica. Set in Liberation
      Sans Bold, which carries Helvetica's proportions.
      `public/apple-touch-icon.png` is the same at 180px, because iOS ignores
      SVG icons.
- [x] **meta description per page** — a `description` prop on `Layout.astro`
      with a site-wide default. Every page passes its own; project pages
      build theirs from the project's own name, dates and description, cut at
      a sentence end near 155 characters. **Josef has not read these yet —
      they are Claude's drafts and he should check the wording.**
- [x] **share preview** — `public/share.jpg`, 1200×630: the Myšina exterior
      with the wordmark on a page-grey band across the bottom. A project page
      uses its own wall picture instead. Set through `og:` and `twitter:`
      tags plus a canonical link.
- [x] **`sitemap.xml` and `robots.txt`** — `src/pages/sitemap.xml.ts` writes
      the sitemap from the page list plus every project, so new projects
      appear in it by themselves. Written by hand rather than with
      `@astrojs/sitemap`, which would need an npm install Claude cannot run.
      A new SECTION, though, has to be added to its `FIXED` list.
- [x] **alt text** — checked every `<img>` in the source. The wall uses the
      project name, the viewer and the fullscreen view both take the caption
      and keep it in step as the pictures change, the portrait names Josef.
      The reference pictures have empty alt, which is right while they are
      placeholders and must be revisited when real ones arrive.
      One to confirm: the home page's cover photograph says "The workshop".
      Is that what it is?

## 5. Going live

Order matters here. Each step is checkable on its own, and **nothing before
step 3 can break email.**

- [ ] **Email first.** Decide: Forpsi mailbox (~175 Kč/year) or Google
      Workspace (~1,800–2,100 Kč/year, gives `josef@josefjosef.cz` as a real
      Gmail account). Set it up. **Send and receive a test message.**
- [ ] **Cloudflare Pages.** Connect the GitHub repository. It deploys to a
      free `josefjosef.pages.dev` address and rebuilds on every push. Open it
      on a phone.
- [ ] **Move DNS to Cloudflare.** Cloudflare imports the existing records
      automatically, but **verify mail still arrives the same day** — a
      missing MX record fails silently, with no bounce and no error.
- [ ] Point `josefjosef.cz` at the site
- [ ] **Cloudflare Web Analytics** — free, cookieless, needs no consent banner
- [ ] **Google Search Console**, and submit the sitemap

## 6. Mobile layout

Deliberately last. It has to react to real pictures and real text, not to
placeholders. Doing it earlier means doing it twice.

---

## Found on 5 Oct, small, not yet decided

- [ ] **The site says it is in English; some of it is Czech.** `<html lang="en">`
      is set for every page, but the project descriptions are Josef's own and
      are in Czech — which now also ends up in the `og:description` a search
      engine reads. Options: set `lang="cs"` on project pages only, make the
      whole site Czech, or leave it. Costs five minutes once decided; worth
      deciding before Google indexes anything.
- [ ] The reference pictures have empty alt text, correct while they are
      placeholders, wrong once they are real.

---

## Open questions — Josef to answer

- [ ] Project description line-height: keep it at 1.35, or back to solid?
      (Changed without being asked on 2 Sept; still unanswered.)
- [ ] `order:` — is a number a position *among the real projects*, or a fixed
      tile that leaves a gap until its neighbour arrives? Currently the first.
- [ ] Git history: shrink it at some point, or leave it? (See below.)

## Decisions already made — do not reopen without a reason

- Hosting: **Cloudflare Pages**, free. Not Forpsi.
- CDN: included with it. Nothing to buy, nothing to configure.
- Analytics: **Cloudflare Web Analytics**. Google Analytics would legally
  require a cookie banner in the EU *and* would still miss about half the
  visitors, because roughly half decline.
- Cookies: the site sets **none** today, measured. Keep it that way and no
  banner is ever needed.
- A picture's words live in its **filename**, never in a second list.
- White backgrounds on drawings are deliberate.
- Type is two thirds of the nav label, with an 8pt floor and scrolling below.
