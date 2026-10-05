import type { APIRoute } from "astro";
import { projects } from "../data/projects";

// The list search engines read to find every page. Written by hand rather
// than with @astrojs/sitemap because installing anything needs npm, which
// Claude cannot run through the bridge - and this is twenty lines.
//
// Every page on the site must be in here. If a new section appears, add it
// to FIXED; project pages look after themselves.
const FIXED = [
	"/",
	"/bio/",
	"/architecture/",
	"/works/",
	"/academic/",
	"/stock/",
	"/references/",
];

export const GET: APIRoute = ({ site }) => {
	const paths = [
		...FIXED,
		...projects.map((p) => `/${p.section}/${p.slug}/`),
	];
	const body =
		'<?xml version="1.0" encoding="UTF-8"?>\n' +
		'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
		paths.map((path) => `\t<url><loc>${new URL(path, site)}</loc></url>`).join("\n") +
		"\n</urlset>\n";
	return new Response(body, { headers: { "Content-Type": "application/xml" } });
};
