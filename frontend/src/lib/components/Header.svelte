<script lang="ts">
  import { Menu, X, Sun, Moon } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { resolve } from "$app/paths";

  import { toggleMode, mode } from "mode-watcher";

  let open = $state(false);
</script>

<header
  class="
		bg-card relative w-full p-4 border-b shadow-sm
		flex items-center justify-between
	"
>
  <a href={resolve("/")} class="no-underline">
    <h1 class="text-2xl font-bold cursor-pointer hover:opacity-80">
      El Arte de Programar
    </h1>
  </a>

  <!-- Desktop menu -->
  <div class="flex flex-row gap-6 items-center px-5">
    <nav class="hidden md:flex gap-6 ml-auto">
      <a href={resolve("/")} class="hover:opacity-80">Ranking</a>
    </nav>

    <div class="flex gap-2">
      <!-- Mobile burger -->
      <Button
        variant="outline"
        size="icon"
        class="md:hidden"
        onclick={() => (open = !open)}
      >
        {#if open}
          <X class="w-5 h-5" />
        {:else}
          <Menu class="w-5 h-5" />
        {/if}
      </Button>

      <!-- Mobile dropdown -->
      {#if open}
        <nav
          class="
				md:hidden absolute top-full left-0 w-full
				flex flex-col gap-2 py-3
				bg-card border-b shadow-lg
				z-50 inset-shadow-sm
			"
        >
          <!-- Add later border-b" -->
          <a href={resolve("/")} class="py-3 px-5 hover:bg-muted/30">Home</a>
        </nav>
      {/if}

      <!-- Dark mode button -->
      <Button variant="outline" size="icon" onclick={toggleMode}>
        {#if mode.current === "light"}
          <Moon class="h-[1.2rem] w-[1.2rem]" />
        {:else}
          <Sun class="h-[1.2rem] w-[1.2rem]" />
        {/if}
        <span class="sr-only">Toggle theme</span>
      </Button>
    </div>
  </div>
</header>
