export type Grades = {
  A: number;
  AB: number;
  ABC: number;
  ABCD: number;
}

export type UserProblems = Record<string, number>;
export interface UserData {
  ranking: number;
  problems: UserProblems;
  grades: Grades;
}

export type ProblemRanking = Record<string, number>;
export interface ProblemData {
  contest_id: number;
  level: string;
  ranking: ProblemRanking;
}

export interface RankingsJSON {
  last_updated: string;
  user_data: Record<string, UserData>;
  problems_data: Record<string, ProblemData>;
}


