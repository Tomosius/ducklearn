// src/frontend/eslint.config.js
import prettier from 'eslint-config-prettier';
import { fileURLToPath } from 'node:url';
import { includeIgnoreFile } from '@eslint/compat';
import js from '@eslint/js';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import tseslint from 'typescript-eslint';
import svelteConfig from './svelte.config.js';

const gitignorePath = fileURLToPath(new URL('./.gitignore', import.meta.url));

export default [
	includeIgnoreFile(gitignorePath),

	// Svelte flat config
	...svelte.configs['flat/recommended'],

	// JS + TS recommended (fast, non type-aware)
	js.configs.recommended,
	...tseslint.configs.recommended,

	// Turn off stylistic rules that clash with Prettier
	prettier,
	...svelte.configs.prettier,

	// Global rules
	{
		languageOptions: {
			globals: { ...globals.browser, ...globals.node }
		},
		rules: {
			'no-undef': 'off' // TS projects shouldn't use this
		}
	},

	// Svelte files: enable TS parser inside <script lang="ts">
	{
		files: ['**/*.svelte', '**/*.svelte.ts', '**/*.svelte.js'],
		languageOptions: {
			parserOptions: {
				projectService: true,
				extraFileExtensions: ['.svelte'],
				parser: tseslint.parser,
				svelteConfig
			}
		}
	}
];
