import tailwindcss from "@tailwindcss/postcss";
import postcssImport from "postcss-import";
import postcssNesting from "postcss-nesting";

export default {
	plugins: [
		postcssImport, // to combine multiple css files
		postcssNesting, // enable CSS nesting
		tailwindcss, // Tailwind CSS
	],
};
