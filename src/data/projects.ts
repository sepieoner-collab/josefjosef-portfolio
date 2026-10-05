import { getCollection } from "astro:content";
import { existsSync } from "node:fs";
import { join } from "node:path";

export interface Photo {
	src: string;
	/** shown bottom-right; changes with every picture */
	caption?: string;
}

export interface Project {
	slug: string;
	section: "architecture" | "works" | "academic";
	name: string;
	dates: string;
	/** stays put while you move through the pictures */
	description: string;
	/** how Josef was involved; also stays put. optional */
	role?: string;
	/** position on the section wall; unnumbered projects go last */
	order?: number;
	/** the first picture at wall size, for the section index. See thumbOf. */
	thumb: string;
	photos: Photo[];
	/** slugs of connected projects in any section. the link is declared once
	    (in either project's file) and read in both directions, so listing a
	    work on a house also shows the house on that work. */
	related?: string[];
}

/** The small copy of a picture that tools/make-thumbs.py writes beside it.
    If it is not there - the script has not been run since this project
    arrived - the full picture is used instead, so a forgotten thumbnail
    costs bandwidth and never shows a broken image. Checked here, at build
    time, because that is the only moment the files are on hand. */
const thumbOf = (src: string): string => {
	const cut = src.lastIndexOf("/");
	const stem = src.slice(cut + 1).replace(/\.[^.]+$/, "");
	const thumb = `${src.slice(0, cut)}/thumbs/${stem}.jpg`;
	return existsSync(join(process.cwd(), "public", thumb)) ? thumb : src;
};

// Adding a project is adding one file: src/content/projects/<slug>.md
// Frontmatter holds section / name / dates / photos / related; the text
// below the --- is the description, one blank line between paragraphs.
const entries = await getCollection("projects");

export const projects: Project[] = entries.map((entry) => ({
	slug: entry.id,
	section: entry.data.section,
	name: entry.data.name,
	dates: entry.data.dates,
	description: entry.body?.trim() ?? "",
	role: entry.data.role,
	order: entry.data.order,
	thumb: entry.data.photos.length ? thumbOf(entry.data.photos[0].src) : "/placeholder-thumb.svg",
	photos: entry.data.photos,
	related: entry.data.related,
}));

// numbered projects first, in their number's order; the rest alphabetically
// behind them, so an unnumbered project never jumps the queue
export const bySection = (section: Project["section"]) =>
	projects
		.filter((p) => p.section === section)
		.sort((a, b) =>
			(a.order ?? Infinity) - (b.order ?? Infinity) ||
			a.name.localeCompare(b.name)
		);

/** every project connected to this one, in either direction */
export const relatedTo = (project: Project) => {
	const named = new Set(project.related ?? []);
	return projects.filter(
		(p) =>
			p.slug !== project.slug &&
			(named.has(p.slug) || (p.related ?? []).includes(project.slug))
	);
};
