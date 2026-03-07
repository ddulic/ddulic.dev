import type { Element, Root } from "hast";
import { visit } from "unist-util-visit";

export const rehypeOptimizeImages = () => {
	return (tree: Root) => {
		visit(tree, "element", (node: Element) => {
			if (node.tagName !== "img") return;
			if (!node.properties.loading) {
				node.properties.loading = "lazy";
			}
			if (!node.properties.decoding) {
				node.properties.decoding = "async";
			}
		});
	};
};
