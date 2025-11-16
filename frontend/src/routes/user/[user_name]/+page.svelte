<script lang="ts">
  import * as Table from "$lib/components/ui/table/index.ts";
  export let data;
  import {
    Card,
    CardHeader,
    CardContent,
    CardTitle,
  } from "$lib/components/ui/card";

  const { userName, rank, problemsList, problemRank, grades } = data;

  function getMax(grades: string): number {
    let max: number;

    switch (grades) {
      case "A":
        max = 5;
        break;
      case "AB":
        max = 7;
        break;
      case "ABC":
        max = 9;
        break;
      default:
        max = 10;
    }

    return max;
  }

  function gradeColor(value: number, grades: string) {
    const percent = getPercentage(value, grades);

    if (percent >= 90) return "bg-green-500";
    if (percent >= 70) return "bg-yellow-400";
    if (percent >= 50) return "bg-orange-400";

    return "bg-red-400";
  }

  function getPercentage(value: number, grades: string): number {
    let max: number = getMax(grades);
    const percent = (value / max) * 100;
    return percent;
  }
</script>

<div class="max-w-[1300px] mx-auto px-5 sm:px-8 lg:px-10 mt-10 mb-10">
  <div class="flex flex-row gap-2 justify-center items-baseline">
    <h2 class="text-4xl font-bold">{userName}</h2>
    <h3 class="text-xl text-amber-400 opacity-75">{rank}</h3>
  </div>

  <Card class="max-w-[1300px] mx-auto my-10 py-5">
    <CardContent>
      <div class="flex justify-around flex-wrap gap-4">
        {#each Object.entries(grades) as [gradeName, gradeValue]}
          <div class="flex flex-col items-center">
            <div class="w-24 h-6 bg-gray-300 rounded overflow-hidden relative">
              <div
                class={`h-6 rounded ${gradeColor(gradeValue, gradeName)}`}
                style={`width: ${getPercentage(gradeValue, gradeName)}%`}
              ></div>
              <!-- Span inside the bar -->
              <span
                class="absolute inset-0 flex items-center justify-center text-sm font-medium text-gray-800"
              >
                {gradeName}: {gradeValue}
              </span>
            </div>
          </div>
        {/each}
      </div>
    </CardContent>
  </Card>

  <div class="overflow-hidden rounded-lg border shadow-lg">
    <Table.Root>
      <Table.Header>
        <Table.Row class="bg-gray-100 dark:bg-gray-800">
          <Table.Head>Rank</Table.Head>
          <Table.Head>ID</Table.Head>
          <Table.Head>Contest</Table.Head>
          <Table.Head>Level</Table.Head>
          <Table.Head>Grade</Table.Head>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {#each problemsList as problem}
          <Table.Row class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <Table.Cell>{problemRank[problem.problem_id]}</Table.Cell>
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
</div>
