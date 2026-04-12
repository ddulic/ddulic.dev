import postcssImport from 'postcss-import';
import postcssNesting from 'postcss-nesting';
import tailwindcss from '@tailwindcss/postcss';

export default {
    plugins: [
        postcssImport,          // to combine multiple css files
        postcssNesting,        // enable CSS nesting
        tailwindcss,           // Tailwind CSS
    ]
};
