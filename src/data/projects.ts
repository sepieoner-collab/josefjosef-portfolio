import { getCollection } from "astro:content";

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
	photos: Photo[];
	/** slugs of connected projects in any section. the link is declared once
	    (in either project's file) and read in both directions, so listing a
	    work on a house also shows the house on that work. */
	related?: string[];
}

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
