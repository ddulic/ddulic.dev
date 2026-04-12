import { getCollection } from "astro:content";
import I18nKey from "@i18n/i18nKey";
import { i18n } from "@i18n/translation";
import { getCategoryUrl } from "@utils/url-utils.ts";

// // Retrieve posts and sort them by publication date
async function getRawSortedPosts() {
	const allBlogPosts = await getCollection("posts", (post) => {
		const data = post.data as PostData;
		return import.meta.env.PROD ? data.draft !== true : true;
	});

	const sorted = allBlogPosts.sort((a, b) => {
		const dataA = a.data as PostData;
		const dataB = b.data as PostData;
		const dateA = new Date(dataA.published);
		const dateB = new Date(dataB.published);
		return dateA > dateB ? -1 : 1;
	});
	return sorted;
}

export async function getSortedPosts() {
	const sorted = await getRawSortedPosts();

	for (let i = 1; i < sorted.length; i++) {
		const currentData = sorted[i].data as PostData;
		const prevData = sorted[i - 1].data as PostData;
		currentData.nextSlug = sorted[i - 1].id;
		currentData.nextTitle = prevData.title;
	}
	for (let i = 0; i < sorted.length - 1; i++) {
		const currentData = sorted[i].data as PostData;
		const nextData = sorted[i + 1].data as PostData;
		currentData.prevSlug = sorted[i + 1].id;
		currentData.prevTitle = nextData.title;
	}

	return sorted;
}
export type PostForList = {
	slug: string;
	data: {
		title: string;
		tags: string[];
		category?: string | null;
		published: Date;
	};
};
export async function getSortedPostsList(): Promise<PostForList[]> {
	const sortedFullPosts = await getRawSortedPosts();

	// delete post.body
	const sortedPostsList = sortedFullPosts.map((post) => {
		const postData = post.data as PostData;
		return {
			slug: post.id,
			data: {
				title: postData.title,
				tags: postData.tags || [],
				category: postData.category || null,
				published: postData.published,
			},
		};
	});

	return sortedPostsList;
}
export type Tag = {
	name: string;
	count: number;
};

export async function getTagList(): Promise<Tag[]> {
	const allBlogPosts = await getCollection<"posts">("posts", ({ data }) => {
		const postData = data as PostData;
		return import.meta.env.PROD ? postData.draft !== true : true;
	});

	const countMap: { [key: string]: number } = {};
	allBlogPosts.forEach((post) => {
		const postData = post.data as PostData;
		postData.tags.forEach((tag: string) => {
			if (!countMap[tag]) countMap[tag] = 0;
			countMap[tag]++;
		});
	});

	// sort tags by count descending, then alphabetically
	const keys: string[] = Object.keys(countMap).sort((a, b) => {
		const diff = countMap[b] - countMap[a];
		return diff !== 0 ? diff : a.toLowerCase().localeCompare(b.toLowerCase());
	});

	return keys.map((key) => ({ name: key, count: countMap[key] }));
}

export type Category = {
	name: string;
	count: number;
	url: string;
};

export async function getCategoryList(): Promise<Category[]> {
	const allBlogPosts = await getCollection<"posts">("posts", ({ data }) => {
		const postData = data as PostData;
		return import.meta.env.PROD ? postData.draft !== true : true;
	});
	const count: { [key: string]: number } = {};
	allBlogPosts.forEach((post) => {
		const postData = post.data as PostData;
		if (!postData.category) {
			const ucKey = i18n(I18nKey.uncategorized);
			count[ucKey] = count[ucKey] ? count[ucKey] + 1 : 1;
			return;
		}

		const categoryName =
			typeof postData.category === "string"
				? postData.category.trim()
				: String(postData.category).trim();

		count[categoryName] = count[categoryName] ? count[categoryName] + 1 : 1;
	});

	const lst = Object.keys(count).sort((a, b) => {
		const diff = count[b] - count[a];
		return diff !== 0 ? diff : a.toLowerCase().localeCompare(b.toLowerCase());
	});

	const ret: Category[] = [];
	for (const c of lst) {
		ret.push({
			name: c,
			count: count[c],
			url: getCategoryUrl(c),
		});
	}
	return ret;
}
