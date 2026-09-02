import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// One project = one file in src/content/projects/<slug>.md.
// Frontmatter holds the structured fields; the body (below the ---) is the
// description, written as plain paragraphs separated by a blank line.
const projects = defineCollection({
	loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
	schema: z.object({
		section: z.enum(["architecture", "works", "academic"]),
		name: z.string(),
		dates: z.string(),
		photos: z.array(
			z.object({
				src: z.string(),
				caption: z.string().optional(),
			})
		),
		// slugs of connected projects, in any section. named on one side only —
		// see relatedTo() in src/data/projects.ts, which reads it both ways.
		related: z.array(z.string()).optional(),
	}),
});

export const collections = { projects };
