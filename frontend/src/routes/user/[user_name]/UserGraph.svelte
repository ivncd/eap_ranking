<script lang="ts">
  import * as Chart from "$lib/components/ui/chart/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import { scaleBand } from "d3-scale";
  import { Arc, Text, PieChart, BarChart, Highlight } from "layerchart";

  let { problems } = $props<{
    problems: {
      problem_id: number;
      grade: number;
      contest_id: number;
      level: string;
    }[];
  }>();

  type Problem = {
    problem_id: string;
    grade: number;
    contest_id: number;
    level: string;
  };

  type ContestAggregated = {
    contest_id: number;
    A: number;
    B: number;
    C: number;
    D: number;
  };

  const contests: ContestAggregated[] = Object.values(
    problems.reduce(
      (acc: Record<number, ContestAggregated>, problem: Problem) => {
        const { contest_id, level, grade } = problem;

        if (!acc[contest_id]) {
          acc[contest_id] = {
            contest_id,
            A: 0,
            B: 0,
            C: 0,
            D: 0,
          };
        }

        if (level in acc[contest_id]) {
          acc[contest_id][
            level as keyof Omit<ContestAggregated, "contest_id">
          ] += grade;
        }

        return acc;
      },
      {} as Record<number, ContestAggregated>,
    ),
  );

  const problemsByLevel = $derived(
    Object.entries(
      problems.reduce(
        (acc: Record<string, number>, p: Problem) => {
          if (["A", "B", "C", "D"].includes(p.level)) {
            acc[p.level]++;
          }
          return acc;
        },
        { A: 0, B: 0, C: 0, D: 0 },
      ),
    )
      .map(([level, count]) => ({
        level,
        number: count,
      }))
      .filter((item) => item.number > 0),
  );

  const chartConfig = {
    A: {
      label: "Nivel A",
      color: "#10b981",
    },
    B: {
      label: "Nivel B",
      color: "#facc15",
    },
    C: {
      label: "Nivel C",
      color: "#ef4444",
    },
    D: {
      label: "Nivel D",
      color: "#8b5cf6",
    },
  } satisfies Chart.ChartConfig;

  const pieData = problemsByLevel.map((item) => ({
    ...item,
    color: chartConfig[item.level as "A" | "B" | "C" | "D"].color,
  }));
</script>

<div class="mt-10 grid w-full grid-cols-1 gap-4 md:grid-cols-2">
  <Card.Root class="w-full">
    <Card.Header class="-mb-3">
      <Card.Title class="text-center">Notas por concurso participado</Card.Title
      >
    </Card.Header>

    <Card.Content>
      <div class="overflow-x-auto pb-4">
        <Chart.Container config={chartConfig} class="h-[200px] w-full">
          <BarChart
            data={contests}
            x="contest_id"
            xScale={scaleBand().padding(0.25)}
            axis="x"
            seriesLayout="stack"
            series={[
              {
                key: "A",
                label: chartConfig.A.label,
                color: chartConfig.A.color,
              },
              {
                key: "B",
                label: chartConfig.B.label,
                color: chartConfig.B.color,
              },
              {
                key: "C",
                label: chartConfig.C.label,
                color: chartConfig.C.color,
              },
              {
                key: "D",
                label: chartConfig.D.label,
                color: chartConfig.D.color,
              },
            ]}
          >
            {#snippet belowMarks()}
              <Highlight area />
            {/snippet}

            {#snippet tooltip()}
              <Chart.Tooltip />
            {/snippet}
          </BarChart>
        </Chart.Container>
      </div>
    </Card.Content>
  </Card.Root>

  <Card.Root class="flex flex-col">
    <Card.Header class="-mb-3">
      <Card.Title class="text-center">Problemas realizados por nivel</Card.Title
      >
    </Card.Header>

    <Card.Content class="flex-1 pb-0">
      <Chart.Container
        config={chartConfig}
        class="mx-auto aspect-square max-h-[250px]"
      >
        <PieChart
          data={pieData}
          key="level"
          value="number"
          c="color"
          cRange={pieData.map((d) => d.color)}
          props={{
            pie: {
              padAngle: 0,
              motion: "tween",
            },
          }}
        >
          {#snippet tooltip()}
            <Chart.Tooltip hideLabel />
          {/snippet}

          {#snippet arc({ props, visibleData, index })}
            {@const level = visibleData[index].level}

            <Arc {...props}>
              {#snippet children({ getArcTextProps })}
                <Text
                  value={level}
                  {...getArcTextProps("centroid")}
                  font-size="16"
                  class="fill-white font-bold capitalize"
                />
              {/snippet}
            </Arc>
          {/snippet}
        </PieChart>
      </Chart.Container>
    </Card.Content>
  </Card.Root>
</div>
