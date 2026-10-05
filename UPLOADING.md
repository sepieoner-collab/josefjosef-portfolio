# Putting content on the site

Who does what, how to name things, and how to prepare pictures.

## The short version

You put files in a folder and tell me the project is ready. I do the rest.
Choosing the pictures and their order is your job; everything mechanical is
mine.

It is now one command, so a project takes about a minute:

```
cd ~/Documents/josefjosef-portfolio
python3 tools/import-project.py "Log cabin in Srdov"
```

Add `--section works` or `--section academic` if it isn't architecture. Add
`--dry-run` to see what it would do without doing it. It never deletes
anything — running it twice just overwrites.

You can run that yourself, or just tell me the folder is there and I'll run
it. Either way the pictures, the order, the sizes and the project file all
come out of that one line.

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

### The project's text file

One text file in the folder, any name, `.txt` or `.rtf`. Four headings, each
on its own line ending in a colon:

```
Project name:
Srdov rural dwelling

Date:
06/2025

Role:
documentation

Project description:
Just as-built documentation, but worth sharing.
```

That is the whole file. **Do not list the pictures in it.** A picture's words
belong in that picture's filename — see below — so there is only ever one
place to change them, and no numbering to keep in step.

### Naming the pictures — the template

```
NN words describing the picture.jpg
```

- **`NN`** — two digits. Sets the order and nothing else.
- **everything after the first space** — becomes the caption, and the alt text,
  exactly as you typed it.

```
01 barn at sunrise.jpg
02 log cabin cross section.jpg
07 barn eastern elevation.jpg
22 workflow.jpg
29 bedroom in the log cabin with greens.jpg
```

Leave the words off and you get a picture with no caption, which is fine —
`14.jpg` just shows nothing until you rename it.

**Why this and not a list in the text file.** A list means a picture's name
lives in two places: the file, and a line in a document. The moment you
reorder, insert, or delete a picture the two drift apart, and nothing warns
you — a caption quietly describes the wrong photograph. Renaming a file
changes its caption. Renumbering a file changes its place. The Finder shows
you exactly what the site will say. Nothing to keep in sync.

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

**Film.** Drop it in the numbered sequence like a picture — `21 sauna in
use.MOV` straight off the phone is fine. I convert it to MP4 and pull a still
out of the first frame for the moment before it starts.

> A film plays by itself, on a loop, **with the sound off**. That is not a
> choice: browsers refuse to autoplay anything audible. Treat it as a moving
> photograph rather than a video with a soundtrack.

Do not spend an evening editing photographs. If a picture needs actual work —
straightening, dust, exposure — do that once in Lightroom and export normally.
Everything mechanical is mine.

---

## Captions come from the filenames

One line per picture, shown at the bottom right of the viewer, doubling as the
alt text a screen reader speaks.

**They are made from the filename, not written by me.** You will replace them
with real words when you have time; until then they are placeholders and the
site works regardless.

Which means naming a file well is worth the ten seconds:

```
20 barn interior.jpg   ->  "barn interior"      useful
photo20.jpg            ->  "photo 20"           useless but harmless
01.jpg                 ->  "picture"            no information at all
```

Numbers still set the order and can be as rough as you like — the importer
reads them as numbers, so `drawing2` correctly comes before `drawing10`.

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
