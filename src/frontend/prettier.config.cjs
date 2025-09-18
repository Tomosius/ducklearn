module.exports = {
	plugins: ['prettier-plugin-svelte', 'prettier-plugin-tailwindcss'],
	printWidth: 100,
	singleQuote: false,
	trailingComma: 'all',
	overrides: [{ files: '*.svelte', options: { parser: 'svelte' } }]
};
