<script lang="ts">
  import * as Table from "$lib/components/ui/table/index.ts";

  export let data;
  const { last_updated, rankings } = data;
</script>

<div
  class="max-w-[1300px] overflow-x-auto px-5 sm:px-8 lg:px-10 mt-8 mb-10 mx-auto"
>
  <p class="text-center text-sm text-gray-500 italic">
    Última actualización: {last_updated}
  </p>
  <Table.Root class="mt-5">
    <Table.Header>
      <Table.Row>
        <Table.Head class="w-20 text-left">Ranking</Table.Head>
        <Table.Head class="text-left">Usuario</Table.Head>
        <Table.Head class="text-center">Nota A /5</Table.Head>
        <Table.Head class="text-center">Nota A+B /7</Table.Head>
        <Table.Head class="text-center">Nota A+B+C /9</Table.Head>
        <Table.Head class="text-center">Nota A+B+C+D /10</Table.Head>
      </Table.Row>
    </Table.Header>

    <Table.Body>
      {#each rankings as row}
        <Table.Row>
          <Table.Cell class="font-medium">{row.ranking}</Table.Cell>
          <Table.Cell>
            <a
              href={`/user/${row.user}`}
              class="text-blue-600 hover:text-blue-800 hover:underline transition-colors"
            >
              {row.user}
            </a>
          </Table.Cell>
          <Table.Cell class="text-center">{row.grades.A}</Table.Cell>
          <Table.Cell class="text-center">{row.grades.AB}</Table.Cell>
          <Table.Cell class="text-center">{row.grades.ABC}</Table.Cell>
          <Table.Cell class="text-center">{row.grades.ABCD}</Table.Cell>
        </Table.Row>
      {/each}
    </Table.Body>
  </Table.Root>
</div>
