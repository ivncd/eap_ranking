import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	server: {
		allowedHosts: ['localhost', "nonterritorial-marguerite-nattily.ngrok-free.dev"]
	},
	plugins: [tailwindcss(), sveltekit()],

});
