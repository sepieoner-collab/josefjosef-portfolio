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
	    and read in both directions, so listing a work on a house also shows
	    the house on that work. */
	related?: string[];
}

const mysina = "/projects/mysina";

// Adding a project is adding an entry here.
export const projects: Project[] = [
	{
		slug: "mysina",
		section: "architecture",
		name: "RD Myšina",
		dates: "07/2021 - 08/2026",
		description: `Řešená parcela se nachází v přímém sousedství města Turnov, za jeho severovýchodním okrajem v lokalitě Myšina, spadající pod obec Mírová pod Kozákovem a katastrální území Bělá u Turnova.

Pozemek je výrazně svažitý směrem na severozápad, z jižní strany je ohraničen skupinou stromů a z ostatních stran sousedními parcelami. Veřejná komunikace se k pozemku přibližuje v jeho severozápadním cípu. Pozemkem prochází v jeho západní části severojižně orientovaná, částečně zatrubněná, vodoteč a nadzemní vedení elektrického proudu.

Návrh vychází především z požadavků investora a zároveň se snaží udržet v souladu s architektonickými limity staveb CHKO Český Ráj, kam parcela svojí příslušností spadá. Tyto limity výrazně ovlivnily výslednou podobu návrhu.

Usazení domu na pozemek vychází jednak z okolního urbanismu a také z tradičního přístupu stavění ve svahu, kdy je kladen důraz na eliminaci terénních úprav. Přibližně ve středu parcely, kde je dům navržen, je přirozeně rovnější část v jinak svažitém terénu.

Výsledkem návrhu je patrový dům se sedlovou střechou s přesahy a obytným podkrovím. Dům nebude podsklepen.

Vstup a vjezd na pozemek je navržen od veřejné komunikace v severozápadní části, kde se počítá se stavbou nadkrytých parkovacích stání spolu s dílenskou místností. Od vstupu na pozemek k domu mají vést dvě cesty. Jedna zpevněná, umožňující obsluhu i pro vozidlo, která je proto širší a delší aby měla průměrně menší sklon a jedna přímá v podobě kamenných pruhů vetknutých v rostlém terénu pouze pro pěší využití.

Vchodové dveře jsou navrženy na severozápadní fasádě. Vstupuje se do komunikačního prostoru chodby, která svírá jádro v podobě koupelny, technické místnosti a schodiště a je z ní možné vstoupit do dvou ložnic, obývacího pokoje nebo projít skrz na jihovýchodní terasu. Hlavním motivem domu je obývací pokoj s kuchyní s převýšeným prostorem. Obývací pokoj se může do exteriéru otevřít pomocí dvou velkých francouzských oken. V podkroví je ochoz, který je vizuálně propojený s obývacím pokojem, ten opticky zvětšuje a má plnit funkci domácí kanceláře např. pro home office, skladovacího prostoru, nebo neformálního prostoru pro odpočinek. Dále je v horním patře také druhá koupelna a velká ložnice s vestavěnou šatnou. Kolem domu je navržen prstenec terasy pro využití blízkého exteriéru za příhodného počasí a má zajistit propojení domu se zahradou.`,
		photos: [
			{ src: `${mysina}/01-approach.jpg`, caption: "from the road, the old neighbour behind" },
			{ src: `${mysina}/02-long-elevation.jpg`, caption: "the north-west elevation" },
			{ src: `${mysina}/03-gable.jpg`, caption: "the gable and its round window" },
			{ src: `${mysina}/04-from-the-garden.jpg`, caption: "from the garden" },
			{ src: `${mysina}/05-east-corner.jpg`, caption: "the eastern corner, from the drive" },
			{ src: `${mysina}/06-living-room.jpg`, caption: "living room and kitchen, the raised space" },
			{ src: `${mysina}/07-from-the-sofa.jpg`, caption: "looking through from the sofa" },
			{ src: `${mysina}/08-kitchen.jpg`, caption: "the kitchen, island and flue" },
			{ src: `${mysina}/09-range.jpg`, caption: "the range" },
			{ src: `${mysina}/10-mezzanine.jpg`, caption: "the mezzanine above the living room" },
			{ src: `${mysina}/11-bathroom.jpg`, caption: "the upstairs bathroom" },
			{ src: `${mysina}/12-outdoor-kitchen.jpg`, caption: "the outdoor kitchen — concrete top on a larch carcass" },
			{ src: `${mysina}/13-outdoor-kitchen-night.jpg`, caption: "the same, the night it was finished" },
			{ src: `${mysina}/14-wiring.jpg`, caption: "wiring the lighting on the concrete worktop" },
		],
	},
];

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
