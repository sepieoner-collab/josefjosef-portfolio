# josefjosef.cz

Josef's architecture / carpentry / design portfolio. Built with
[Astro](https://astro.build) — a tool that turns simple content files into a
plain, fast, static website (no database, almost no client-side JavaScript).

## Working on this site

You'll need [Node.js](https://nodejs.org) installed once (LTS version).

```bash
# install the project's dependencies (only needed once, or after they change)
npm install

# start a local preview at http://localhost:4321 that updates as you edit
npm run dev

# build the final, deployable site into ./dist
npm run build
```

## Project structure

```
src/
  pages/       one file = one page (Astro's routing is file-based)
  layouts/     shared page "shells" (header, nav, footer) reused across pages
public/        files copied as-is (favicon, etc.) — not processed by Astro
```

This is stage 1 of the build (project setup). See the project notes for the
full staged plan.
