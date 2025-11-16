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

type ProblemRanks = {
  [problemId: string]: {
    [username: string]: number;
  };
};

type RankingsJSON = {
  last_updated: string;
  data: Record<string, UserData>;
  problem_ranks: ProblemRanks;
}

const rawData: RankingsJSON = rawDataJson;
export const load: PageLoad = ({ params }) => {
  const userName: string = params.user_name;

  const userData: UserData | undefined = rawData.data[userName];
  if (!userData) {
    throw error(404, { message: `Usuario ${userName} no encontrado.` });
  }

  let rank: number = userData.ranking;
  let grades: Grades = userData.grades;
  let problemsList: Problem[] = userData.problems.sort((a, b) => b.contest_id - a.contest_id);

  const problemRank: Record<string, number> = {};

  for (const [problemId, users] of Object.entries(rawData.problem_ranks)) {
    if (users[userName] !== undefined) {
      problemRank[problemId] = users[userName];
    }
  }

  return {
    userName,
    rank,
    problemsList,
    problemRank,
    grades
  };
};
