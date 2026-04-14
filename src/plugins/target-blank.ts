// src/plugins/targetBlank.ts

import type { Element, Root } from "hast";
import { visit } from "unist-util-visit";

export const targetBlank = ({ domain = "" }: { domain?: string } = {}) => {
	return (tree: Root) => {
		visit(tree, "element", (e: Element) => {
			if (
				e.tagName === "a" &&
				e.properties?.href &&
				e.properties.href.toString().startsWith("http") &&
				!e.properties.href.toString().includes(domain)
			) {
				e.properties.target = "_blank";
				e.properties.rel = "noopener noreferrer";
			}
		});
	};
};
