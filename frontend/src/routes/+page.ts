import type { PageLoad } from './$types';
import type { RankingsJSON, Grades } from '$lib/types'

import rawDataJson from '$lib/data.json';

type TableRow = {
  ranking: number,
  user: string,
  grades: Grades
}


const rawData: RankingsJSON = rawDataJson;
export const load: PageLoad = () => {
  const rankings: TableRow[] = Object.entries(rawData.user_data).map(
    ([user, userData]) => ({
      user,
      ranking: userData.ranking,
      grades: userData.grades,
    })
  );

  rankings.sort((a, b) => b.grades.ABCD - a.grades.ABCD);

  return {
    last_updated: rawData.last_updated,
    rankings,
  };
};

