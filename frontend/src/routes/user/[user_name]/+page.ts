import type { Grades } from '$lib/types';
import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';
import rawDataJson from '$lib/data.json';

type Problem = {
  problem_id: number;
  contest_id: number;
  problem_level: string;
  grade: number;
}

type UserData = {
  ranking: number;
  problems: Problem[];
  grades: Grades;
}

type RankingsJSON = {
  last_updated: string;
  data: Record<string, UserData>;
}

const rawData: RankingsJSON = rawDataJson;
export const load: PageLoad = ({ params }) => {
  const userName: string = params.user_name;
  let problemsList: Problem[] | null = null;
  let grades: Grades | null = null;
  let rank: number | null = null

  const userData: UserData | undefined = rawData.data[userName];
  const exists: boolean = userData ? true : false;
  if (!exists) {
    throw error(404, { message: `Usuario ${userName} no encontrado.` });
  }

  rank = userData.ranking;
  grades = userData.grades;
  problemsList = userData.problems.sort((a, b) => b.contest_id - a.contest_id);

  return {
    userName,
    rank,
    problemsList,
    grades
  };
};
