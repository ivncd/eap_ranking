// svelte.config.js
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

// This is the new, correct logic:
const building = process.argv.includes('build');
const preview = process.argv.includes('preview');
const base_path = building || preview ? '/eap_ranking' : ''; // <-- Make sure to set your repo name here

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({
			pages: '../dist',
			assets: '../dist',
			fallback: 'index.html',
			precompress: false,
			strict: true,
		}),
		paths: {
			// This will now be correct for all commands:
			base: base_path,
		},
	},
};

export default config;
