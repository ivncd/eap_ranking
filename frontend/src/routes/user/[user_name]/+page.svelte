<script lang="ts">
  import * as Table from "$lib/components/ui/table/index.ts";
  import { error } from "@sveltejs/kit";
  export let data;

  const { exists, userName, problemsList, grades } = data;

  function gradeColor(value: number, max: number) {
    const percent = (value / max) * 100;
    if (percent >= 90) return "bg-green-500";
    if (percent >= 70) return "bg-yellow-400";
    if (percent >= 50) return "bg-orange-400";

    return "bg-red-400";
  }
</script>

<div class="max-w-[1300px] mx-auto px-5 sm:px-8 lg:px-10 mt-10 mb-10">
  <h2 class="text-3xl font-bold text-center mb-6">{userName}</h2>

  <div class="flex justify-around mb-10 flex-wrap gap-4">
    {#each Object.entries(grades) as [gradeName, gradeValue]}
      <div class="flex flex-col items-center">
        <div class="w-24 h-6 bg-gray-200 rounded overflow-hidden">
          <div
            class={`h-6 rounded ${gradeColor(gradeValue, gradeName === "A" ? 5 : gradeName === "AB" ? 7 : gradeName === "ABC" ? 9 : 10)}`}
            style="width: {(gradeValue /
              (gradeName === 'A'
                ? 5
                : gradeName === 'AB'
                  ? 7
                  : gradeName === 'ABC'
                    ? 9
                    : 10)) *
              100}%"
          ></div>
        </div>
        <span class="mt-1 font-medium">{gradeName}: {gradeValue}</span>
      </div>
    {/each}
  </div>

  <Table.Root class="border rounded-lg overflow-hidden shadow-lg">
    <Table.Header>
      <Table.Row class="bg-gray-100 dark:bg-gray-800">
        <Table.Head>ID</Table.Head>
        <Table.Head>Contest</Table.Head>
        <Table.Head>Level</Table.Head>
        <Table.Head>Grade</Table.Head>
      </Table.Row>
    </Table.Header>
    <Table.Body>
      {#each problemsList as problem}
        <Table.Row class="hover:bg-gray-50 dark:hover:bg-gray-700">
          <Table.Cell class="font-medium">
            <a
              href="https://aceptaelreto.com/problem/statement.php?id={problem.problem_id}"
              class="text-blue-600 hover:text-blue-800 hover:underline transition-colors"
              target="_blank"
            >
              {problem.problem_id}
            </a>
          </Table.Cell>
          <Table.Cell>{problem.contest_id}</Table.Cell>
          <Table.Cell>{problem.problem_level}</Table.Cell>
          <Table.Cell>{problem.grade}</Table.Cell>
        </Table.Row>
      {/each}
    </Table.Body>
  </Table.Root>
</div>
