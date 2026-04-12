import { defineCollection, z } from "astro:content";

const postsCollection = defineCollection({
	schema: ({ image }) => z.object({
		title: z.string(),
		published: z.date(),
		updated: z.date().optional(),
		draft: z.boolean().optional().default(false),
		description: z.string().optional().default(""),
		image: image().optional(),
		tags: z.array(z.string()).optional().default([]),
		category: z.string().optional().nullable().default(""),
		lang: z.string().optional().default(""),

		/* For internal use */
		prevTitle: z.string().default(""),
		prevSlug: z.string().default(""),
		nextTitle: z.string().default(""),
		nextSlug: z.string().default(""),
	}),
});
const specCollection = defineCollection({
	schema: ({ image }) => z.object({
		image: image().optional(),
	}),
});
export const collections: Record<string, ReturnType<typeof defineCollection>> = {
	posts: postsCollection,
	spec: specCollection,
};
