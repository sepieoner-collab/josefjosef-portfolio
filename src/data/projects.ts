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
	photos: entry.data.photos,
	related: entry.data.related,
}));

export const bySection = (section: Project["section"]) =>
	projects.filter((p) => p.section === section);

/** every project connected to this one, in either direction */
export const relatedTo = (project: Project) => {
	const named = new Set(project.related ?? []);
	return projects.filter(
		(p) =>
			p.slug !== project.slug &&
			(named.has(p.slug) || (p.related ?? []).includes(project.slug))
	);
};
