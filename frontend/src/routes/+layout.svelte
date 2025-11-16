<script lang="ts">
	import "../app.css";
	import favicon from "$lib/assets/favicon.svg";

	import { ModeWatcher } from "mode-watcher";
	import Header from "$lib/components/Header.svelte";
	// export const prerender = false;

	let { children } = $props();
</script>

<ModeWatcher />

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<Header></Header>

<main class="mt-4">
	{@render children()}
</main>

<footer class="mt-10"></footer>
