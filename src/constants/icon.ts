import type { Favicon } from "@/types/config.ts";

export const defaultFavicons: Favicon[] = [
	{
		src: "/favicon/favicon-light.ico",
		theme: "light",
	},
	{
		src: "/favicon/favicon-light-16x16.png",
		theme: "light",
		sizes: "16x16",
	},
	{
		src: "/favicon/favicon-light-32x32.png",
		theme: "light",
		sizes: "32x32",
	},
	{
		src: "/favicon/android-chrome-light-192x192.png",
		theme: "light",
		sizes: "192x192",
	},
	{
		src: "/favicon/favicon-dark.ico",
		theme: "dark",
	},
	{
		src: "/favicon/favicon-dark-16x16.png",
		theme: "dark",
		sizes: "16x16",
	},
	{
		src: "/favicon/favicon-dark-32x32.png",
		theme: "dark",
		sizes: "32x32",
	},
	{
		src: "/favicon/android-chrome-dark-192x192.png",
		theme: "dark",
		sizes: "192x192",
	},
];
