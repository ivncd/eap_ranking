import type { PageLoad } from './$types';
import type { Grades } from '$lib/types'
import rawData from '$lib/data.json';

type TableRow = {
  ranking: number,
  user: string,
  grades: Grades
}

export const load: PageLoad = () => {
  const rankings: TableRow[] = Object.entries(rawData.data).map(
    ([user, userData]) => ({
      user,
      ranking: userData.ranking,
      grades: userData.grades,
      problems: userData.problems,
    })
  );

  rankings.sort((a, b) => b.grades.ABCD - a.grades.ABCD);

  return {
    last_updated: rawData.last_updated,
    rankings,
  };
};

