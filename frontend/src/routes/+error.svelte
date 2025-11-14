<script>
  import { page } from "$app/state";
  import Button from "$lib/components/ui/button/button.svelte";
</script>

<div class="px-5 text-center mt-[20vh] mb-[10vh]">
  <h1
    class="text-9xl font-extrabold text-gray-300 dark:text-gray-400 select-none mb-6"
  >
    {page.status}
  </h1>

  <h2 class="text-2xl sm:text-3xl font-semibold mb-6 mx-auto">
    {page.error?.message}
  </h2>

  <Button href="/">Volver al inicio</Button>
</div>
