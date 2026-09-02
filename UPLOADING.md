# Putting content on the site

Who does what, how to name things, and how to prepare pictures.

## The short version

You put files in a folder and tell me the project is ready. I do the rest.
Choosing the pictures and their order is your job. Making them web-sized,
naming them, writing the data file — mine.

---

## Why there is no upload interface

A real upload page needs a server sitting there waiting to receive files.
This site has no server: it is a folder of finished files, which is why it is
fast, free to host and impossible to break. Adding a server to it would mean
a login, a database, and a few hundred lines of code that only I understand —
against every rule in `CLAUDE.md`.

You already have an interface, and you have used it for thirty years: the
Finder. Folders and files. The difference is that from now on the folders
have a shape we both agree on.

---

## The drop folder

```
josefjosef-portfolio/
  _incoming/
    mysina/                    ← folder name = the project's web address
      01 approach.jpg
      02 long elevation.jpg
      03 ground floor.pdf      ← drawings as PDF
      project.txt
```

`_incoming/` is ignored by git. Nothing in it reaches the website or GitHub
until I process it, and you can delete a project's folder once it is live.

### project.txt

Plain text. TextEdit is fine (Format → Make Plain Text).

```
name: RD Myšina
dates: 07/2021 - 08/2026
section: architecture

First paragraph of the description.

Second paragraph. Blank line between paragraphs, as normal.
```

`section:` is one of `architecture`, `works`, `academic`.

### Naming the pictures

`01 approach.jpg` — number first, then a few words about what is in it.

- The **number** is the order they are shown in. Nothing else sets it.
- The **words** are my starting point for the caption. Rough is fine.

---

## Preparing pictures — the honest answer: barely at all

**Photographs.** Export JPEG, long edge **2400px or larger**. Larger is fine,
I scale down; I cannot invent detail, so don't go below. Don't sharpen for
web, don't compress hard, don't rename cleverly. Leave the colour profile on.

> What I produce: JPEG, long edge 2400px, quality 82, colour profile
> preserved, roughly 400–800 KB each. That is sharp on a retina screen and
> loads in a blink.

**Technical drawings.** PDF straight out of ArchiCAD, real vector lines, as
you already export them. If ArchiCAD offers "convert text to outlines" or
"embed fonts", say yes.

> What I produce: SVG. Vector, so it stays perfectly sharp at any zoom, and
> usually under 300 KB — smaller *and* better than any photograph. If a
> drawing turns out to be heavy hatching or an embedded photo, SVG bloats;
> I'll fall back to PNG and tell you why.

Do not spend an evening editing photographs. If a picture needs actual work —
straightening, dust, exposure — do that once in Lightroom and export normally.
Everything mechanical is mine.

---

## Captions and alt text

One line per picture. It shows at the bottom right of the viewer and doubles
as the alt text — the description a blind visitor's screen reader speaks, and
what Google reads. One string, two jobs.

**I draft them by looking at the photographs; you correct them.** They should
say plainly what is in the frame: "the gable and its round window", not
"beautiful architectural composition".

---

## Where the pictures actually live

```
public/projects/mysina/01-approach.jpg
```

Inside this project folder, on your laptop, versioned in git, pushed to
GitHub, deployed with the site. No cloud service, no database, no account
that can expire.

**That folder is the backend.** Open it in the Finder whenever you like and
see exactly what is on the site. To swap a picture, drop a new file over the
old one with the same name.

Size: about 600 KB a photograph, so fourteen projects of fourteen pictures is
roughly 120 MB. GitHub is comfortable with that. Originals stay out — that is
what `_incoming/` being ignored is for.

---

## Changing something later

- **Wording** — open `src/content/projects/<slug>.md` in TextEdit, edit, save.
- **A picture** — replace the file, keep the name.
- **The order** — renumber the files and tell me to re-run it.

Then commit and push (`CLAUDE.md`, "Saving work"), or ask me to write out the
commands.

---

## References — the exception

References are inspiration: your own photographs of architecture, cities and
nature, screenshots, whatever graphic has stuck with you and shaped how you
work. No titles, no captions, no dates — the page shows pictures and nothing
else.

So references get **no text file at all. The filename is the whole record.**

```
_incoming/references/
    anything.jpg          ← drop them in under any name you like
```

I look at each one, rename it to what it actually shows, and that name becomes
its alt text — the description a screen reader speaks and a search engine
reads:

```
public/references/concrete-stair-barcelona.jpg   → "concrete stair, Barcelona"
public/references/birch-bark.jpg                 → "birch bark"
```

Adding one later is dropping a file in with a sensible name. Nothing else.
The column heights work themselves out: I measure each picture's proportions
when I process it, so the hand-written ratio table the placeholders needed
disappears.

## Index thumbnails

Automatic. Each project's `01-` picture is its thumbnail on the section wall.
Deliberately not random — the wall should look the same every time you visit
it. If a project wants a different thumbnail, say so and I'll add a `thumb:`
line to its file.

---

## Still to settle

- **stock** — items need a name, availability and sold state, and may not
  need a page each. Its own small collection when we get to it.
- **related projects** — the link between a house and the joinery inside it.
  Leave it until most of the content is in and the connections are obvious.
