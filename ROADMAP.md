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

- [ ] **Commit and push.** A large batch is sitting uncommitted on the laptop
      only: two whole projects (Srdov, Ny-Ålesund), the ordering feature, the
      click-the-name behaviour, the importer, and all the documentation.
      Ask Claude for the exact commands; they go one line at a time.

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

- [ ] favicon
- [ ] meta description per page
- [ ] share preview picture (what appears when the link is pasted anywhere)
- [ ] `sitemap.xml` and `robots.txt` — so search engines can find it
- [ ] check every picture has alt text and the headings make sense

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
