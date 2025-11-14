<script lang="ts">
	import "../app.css";
	import favicon from "$lib/assets/favicon.svg";

	import { Button } from "$lib/components/ui/button/index.js";
	import { ModeWatcher, toggleMode, mode } from "mode-watcher";
	import { Sun, Moon } from "lucide-svelte";
	import { resolve } from "$app/paths";

	export const prerender = false;

	let { children } = $props();
</script>

<ModeWatcher />

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header class="w-full p-4 border-b flex items-center justify-center relative">
	<!-- Title -->
	<a
		href={resolve("/")}
		class="no-underline absolute left-1/2 -translate-x-1/2"
	>
		<h1 class="text-2xl font-bold cursor-pointer hover:opacity-80">
			El Arte de Programar
		</h1>
	</a>

	<!-- Dark mode button -->
	<Button variant="outline" size="icon" class="ml-auto" onclick={toggleMode}>
		{#if mode.current === "light"}
			<Moon class="h-[1.2rem] w-[1.2rem]" />
		{:else}
			<Sun class="h-[1.2rem] w-[1.2rem]" />
		{/if}
		<span class="sr-only">Toggle theme</span>
	</Button>
</header>

{@render children()}

<footer></footer>
