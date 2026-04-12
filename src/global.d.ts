import type { AstroIntegration } from "@swup/astro";

declare global {
	interface SearchResult {
		url: string;
		meta: {
			title: string;
		};
		excerpt: string;
		content?: string;
		word_count?: number;
		filters?: Record<string, unknown>;
		anchors?: Array<{
			element: string;
			id: string;
			text: string;
			location: number;
		}>;
		weighted_locations?: Array<{
			weight: number;
			balanced_score: number;
			location: number;
		}>;
		locations?: number[];
		raw_content?: string;
		raw_url?: string;
		sub_results?: SearchResult[];
	}

	interface Window {
		// type from '@swup/astro' is incorrect
		swup: AstroIntegration;
		pagefind: {
			search: (query: string) => Promise<{
				results: Array<{
					data: () => Promise<SearchResult>;
				}>;
			}>;
		};
	}

	interface PostData {
		title: string;
		published: Date;
		updated?: Date;
		draft?: boolean;
		description?: string;
		image?: { src: string } | null;
		tags: string[];
		category: string | null;
		lang?: string;
		prevTitle?: string;
		prevSlug?: string;
		nextTitle?: string;
		nextSlug?: string;
	}
}
