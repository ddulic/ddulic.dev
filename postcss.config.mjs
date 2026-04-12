import postcssImport from 'postcss-import';
import postcssNesting from 'postcss-nesting';
import tailwindcss from '@tailwindcss/postcss';

export default {
    plugins: {
        'postcss-import': postcssImport,          // to combine multiple css files
        'postcss-nesting': postcssNesting,
        tailwindcss: tailwindcss,
    }
};
