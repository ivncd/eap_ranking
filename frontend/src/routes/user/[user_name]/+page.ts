import type { Grades } from '$lib/types';
import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';
import rawDataJson from '$lib/data.json';

type UserProblems = Record<string, number>;
interface UserData {
  ranking: number;
  problems: UserProblems;
  grades: Grades;
}

type ProblemRanking = Record<string, number>;
interface ProblemData {
  contest_id: number;
  level: string;
  ranking: ProblemRanking;
}

interface RankingsJSON {
  last_updated: string;
  user_data: Record<string, UserData>;
  problems_data: Record<string, ProblemData>;
}

const rawData: RankingsJSON = rawDataJson;
export const load: PageLoad = ({ params }) => {
  const userName: string = params.user_name;
  const userData = rawData.user_data[userName];
  if (!userData) {
    throw error(404, { message: `Usuario ${userName} no encontrado.` });
  }

  const rank = userData.ranking;
  const grades = userData.grades;

  const problemsList = Object.entries(userData.problems)
    .map(([problemId, grade]) => {
      const pdata = rawData.problems_data[problemId];
      return {
        problem_id: problemId,
        grade,
        contest_id: pdata.contest_id,
        level: pdata.level
      };
    }).sort((a, b) => b.contest_id - a.contest_id);

  const problemRank: ProblemRanking = {};
  for (const [problemId, pdata] of Object.entries(rawData.problems_data)) {
    if (pdata.ranking[userName] !== undefined) {
      problemRank[problemId] = pdata.ranking[userName];
    }
  }

  return {
    userName,
    rank,
    grades,
    problemsList,
    problemRank
  };
};
